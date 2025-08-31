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
  const input_a = document.querySelector("#plf_a");
  const input_b = document.querySelector("#plf_b");
  const conv_type_container = document.querySelector("#conv_type_container");

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

  // put default values into the textfields
  input_a.value = "[(0, 0, 0), (1, 1, 0), (2, 2, 0), (3, 3, 0)], 5";
  input_b.value = "[(0, 0, 0), (1, 0, 1)], 4";

  // create the PLFs to plot (static for now)
  let plf_a = PLF.from_rtctoolbox_str(input_a.value);
  let plf_b = PLF.from_rtctoolbox_str(input_b.value);
  let conv_type = ConvType(0);

  // add radio buttons for selecting the conv type
  for (let ctype of ConvType) {
    const label = document.createElement("label");
    const input = document.createElement("input");

    input.type = "radio";
    input.name = "conv_type";
    input.value = ctype.value;
    if (ctype.value == conv_type.value) {
      input.checked = "True";
    }

    input.addEventListener("change", update_conv_type);

    label.appendChild(input);
    label.insertAdjacentHTML("beforeend", ctype.operator_desc);
    conv_type_container.appendChild(label);
  }

  // Render the LaTeX equations in the radio buttons
  if (window.MathJax) {
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, conv_type_container]);
  }

  // compute the convolution
  let conv_properties = ConvProperties(plf_a, plf_b, conv_type);
  let current_x = conv_properties.slider_min;
  let conv_result = conv_at_x(plf_a, plf_b, current_x, conv_type);

  // configure the slider
  slider.min = conv_properties.slider_min;
  slider.max = conv_properties.slider_max;
  slider.value = current_x;

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
    legendgroup: "group_sum",
    showlegend: true,
  };

  let trace_sum_marker = {
    x: [conv_result.result.x],
    y: [conv_result.result.y],
    mode: "markers",
    legendgroup: "group_sum",
    showlegend: false,
  };

  let trace_result = {
    x: toJsSafe(conv_properties.result.x),
    y: toJsSafe(conv_properties.result.y),
    mode: "lines",
    name: conv_type.operator_desc,
    legendgroup: "group_result",
    showlegend: true,
  };

  let trace_result_marker = {
    x: [current_x],
    y: [conv_properties.result(current_x)],
    mode: "markers",
    legendgroup: "group_result",
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
   * Updates the plot to a new current_x value.
   */
  function current_x_changed() {
    conv_result = conv_at_x(plf_a, plf_b, current_x, conv_type);

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
      x: [current_x],
      y: [conv_properties.result(current_x)],
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

  /**
   * Redraws the entire plot. Should be used when the PLFs or the convolution type
   * change. Will also update the slider and and axis limits. Internally calls the
   * current_x_changed function but also updates the other traces.
   */
  function redraw_plot() {
    // Recompute the convolution
    conv_properties = ConvProperties(plf_a, plf_b, conv_type);
    current_x = Math.min(
      conv_properties.slider_max,
      Math.max(conv_properties.slider_min, current_x)
    );

    // Reset slider limits
    slider.min = conv_properties.slider_min;
    slider.max = conv_properties.slider_max;
    slider.value = current_x;

    // Recompute all traces that aren't touched by current_x_changed
    trace_a = {
      x: toJsSafe(plf_a.x),
      y: toJsSafe(plf_a.y),
    };

    trace_b = {
      x: toJsSafe(plf_b.x),
      y: toJsSafe(plf_b.y),
    };

    trace_result = {
      x: toJsSafe(conv_properties.result.x),
      y: toJsSafe(conv_properties.result.y),
    };

    // Update the plot, inlcuding the axis limits
    Plotly.update(
      plot,
      {
        x: [trace_a.x, trace_b.x, trace_result.x],
        y: [trace_a.y, trace_b.y, trace_result.y],
      },
      {
        xaxis: { range: [conv_properties.min_x, conv_properties.max_x] },
        yaxis: { range: [conv_properties.min_y, conv_properties.max_y] },
      },
      [0, 2, 5]
    );

    // Update all remaining traces
    current_x_changed();
  }

  /**
   * Updates the current_x value and redraws the affected traces.
   * @param {Event} event Event from a range type input.
   */
  function update_current_x(event) {
    current_x = Number(event.target.value);
    current_x_changed();
  }

  /**
   * Updates the corresponding PLF and redraws the entire plot.
   * @param {InputEvent} event Event from a text type input.
   */
  function update_plf(event) {
    try {
      let new_plf = PLF.from_rtctoolbox_str(event.target.value);
      if (event.target.id == "plf_a") {
        plf_a = new_plf;
      } else if (event.target.id == "plf_b") {
        plf_b = new_plf;
      }
      redraw_plot();
      event.target.classList.remove("error");
    } catch (error) {
      event.target.classList.add("error");
    }
  }

  /**
   * Updates the conv_type value and redraws the entire plot.
   * @param {Event} event Event from a radio type input.
   */
  function update_conv_type(event) {
    conv_type = ConvType(Number(event.target.value));
    redraw_plot();
  }

  // Add listener to input elements
  slider.addEventListener("input", update_current_x);
  input_a.addEventListener("input", update_plf);
  input_b.addEventListener("input", update_plf);

  console.log("main finished");
}

main();
