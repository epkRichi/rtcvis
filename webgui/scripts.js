/**
 * Converts the given proxy to a js object that is not linked to the original
 * python object anymore. Destroys all intermediary proxies and the given proxy
 * to prevent memory leaks.
 *
 * @param {PyProxy} proxy The proxy to be converted.
 * @returns {any} The converted proxy.
 */
function toJsSafe(proxy) {
  if (proxy === null || typeof proxy === "undefined") {
    return null;
  }
  let pyproxies = [];
  const convertedProxy = proxy.toJs({ pyproxies });
  for (let px of pyproxies) {
    px.destroy();
  }
  proxy.destroy();
  return convertedProxy;
}

async function main() {
  // get references to the plot and slider DOM elements
  const plot = document.querySelector("#plot");
  const slider = document.querySelector("#slider");

  // load and initialize pyodide
  let pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip");
  const micropip = pyodide.pyimport("micropip");
  await micropip.install("../dist/rtcvis-0.2.0-py3-none-any.whl");
  pyodide.runPython(
    "from rtcvis import PLF, conv_at_x, ConvType, ConvProperties"
  );
  let conv_at_x = pyodide.globals.get("conv_at_x");
  let ConvType = pyodide.globals.get("ConvType");
  let PLF = pyodide.globals.get("PLF");
  let ConvProperties = pyodide.globals.get("ConvProperties");

  // create the PLFs to plot (static for now)
  let plf_a = PLF.from_rtctoolbox(
    [
      [0, 0, 0],
      [1, 1, 0],
      [2, 2, 0],
      [3, 3, 0],
    ],
    5
  );
  let plf_b = PLF.from_rtctoolbox(
    [
      [0, 0, 0],
      [1, 0, 1],
    ],
    5
  );
  let conv_type = ConvType.MIN_PLUS_CONV;

  // compute the convolution
  let conv_result = conv_at_x(plf_a, plf_b, 0, conv_type);
  let conv_properties = ConvProperties(plf_a, plf_b, conv_type);

  // configure the slider
  slider.min = conv_properties.slider_min;
  slider.max = conv_properties.slider_max;
  slider.value = conv_properties.slider_min;

  // create the traces to plot
  let trace_a = {
    x: toJsSafe(plf_a.x),
    y: toJsSafe(plf_a.y),
    mode: "lines",
    name: "$a(\\lambda)$",
    visible: "legendonly",
  };

  let trace_transformed_a = {
    x: toJsSafe(conv_result.transformed_a.x),
    y: toJsSafe(conv_result.transformed_a.y),
    mode: "lines",
    name: "$a(\\Delta - \\lambda)$",
  };

  let trace_b = {
    x: toJsSafe(plf_b.x),
    y: toJsSafe(plf_b.y),
    mode: "lines",
    name: "$b(\\lambda)$",
  };

  let trace_sum = {
    x: toJsSafe(conv_result.sum.x),
    y: toJsSafe(conv_result.sum.y),
    mode: "lines",
    name: conv_type.sum_desc,
  };

  let trace_sum_marker = {
    x: [conv_result.result.x],
    y: [conv_result.result.y],
    mode: "markers",
    showlegend: false,
  };

  let trace_result = {
    x: toJsSafe(conv_properties.result.x),
    y: toJsSafe(conv_properties.result.y),
    mode: "lines",
    name: conv_type.operator_desc,
  };

  let trace_result_marker = {
    x: [Number(slider.value)],
    y: [conv_properties.result(Number(slider.value))],
    mode: "markers",
    showlegend: false,
  };

  // Create the plot
  Plotly.newPlot(
    plot,
    [
      trace_a,
      trace_transformed_a,
      trace_b,
      trace_sum,
      trace_sum_marker,
      trace_result,
      trace_result_marker,
    ],
    {
      margin: { t: 0 },
      xaxis: { range: [conv_properties.min_x, conv_properties.max_x] },
      yaxis: { range: [conv_properties.min_y, conv_properties.max_y] },
      legend: { x: 1, y: 0.5 },
      colorway: [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#d62728",
        "#9467bd",
        "#9467bd",
      ],
    }
  );

  /**
   * Updates the plot to a new delta value.
   *
   * @param {Number} value The new delta (x) value.
   */
  function restyle(value) {
    conv_result = conv_at_x(plf_a, plf_b, value, conv_type);

    trace_transformed_a = {
      x: toJsSafe(conv_result.transformed_a.x),
      y: toJsSafe(conv_result.transformed_a.y),
    };

    trace_sum = {
      x: toJsSafe(conv_result.sum.x),
      y: toJsSafe(conv_result.sum.y),
    };

    trace_sum_marker = {
      x: [conv_result.result.x],
      y: [conv_result.result.y],
    };

    trace_result_marker = {
      x: [value],
      y: [conv_properties.result(value)],
    };

    Plotly.restyle(
      plot,
      {
        x: [
          trace_transformed_a.x,
          trace_sum.x,
          trace_sum_marker.x,
          trace_result_marker.x,
        ],
        y: [
          trace_transformed_a.y,
          trace_sum.y,
          trace_sum_marker.y,
          trace_result_marker.y,
        ],
      },
      [1, 3, 4, 6]
    );
  }

  // Add a listener to the slider
  slider.addEventListener("input", (event) => {
    restyle(Number(event.target.value));
  });

  console.log("main finished");
}

main();
