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
  const plot = document.querySelector("#plot");
  const input = document.querySelector("#slider");

  let pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip");
  const micropip = pyodide.pyimport("micropip");
  await micropip.install("../dist/rtcvis-0.2.0-py3-none-any.whl");
  pyodide.runPython("from rtcvis import PLF, conv_at_x, ConvType");

  let conv_at_x = pyodide.globals.get("conv_at_x");
  let ConvType = pyodide.globals.get("ConvType");
  let PLF = pyodide.globals.get("PLF");

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

  let conv_result = conv_at_x(plf_a, plf_b, 0, ConvType.MIN_PLUS_CONV);

  let trace_a = {
    x: [toJsSafe(plf_a.x)],
    y: [toJsSafe(plf_a.y)],
  };

  let trace_b = {
    x: [toJsSafe(plf_b.x)],
    y: [toJsSafe(plf_b.y)],
  };

  let trace_transformed_a = {
    x: [toJsSafe(conv_result.transformed_a.x)],
    y: [toJsSafe(conv_result.transformed_a.y)],
  };

  let trace_sum = {
    x: [toJsSafe(conv_result.sum.x)],
    y: [toJsSafe(conv_result.sum.y)],
  };

  // let trace_result = {
  //   x: [toJsSafe(conv_result.result.x)],
  //   y: [toJsSafe(conv_result.result.y)],
  // };

  Plotly.newPlot(
    plot,
    [trace_a, trace_b, trace_transformed_a, trace_sum],
    {
      margin: { t: 0 },
    }
  );

  function restyle(value) {
    conv_result = conv_at_x(plf_a, plf_b, value, ConvType.MIN_PLUS_CONV);

    trace_transformed_a = {
      x: [toJsSafe(conv_result.transformed_a.x)],
      y: [toJsSafe(conv_result.transformed_a.y)],
    };

    trace_sum = {
      x: [toJsSafe(conv_result.sum.x)],
      y: [toJsSafe(conv_result.sum.y)],
    };

    // trace_result = {
    //   x: [toJsSafe(conv_result.result.x)],
    //   y: [toJsSafe(conv_result.result.y)],
    // };

    Plotly.restyle(
      plot,
      {
        x: [trace_transformed_a.x, trace_sum.x],
        y: [trace_transformed_a.y, trace_sum.y],
      },
      [2, 3]
    );
  }

  input.addEventListener("input", (event) => {
    restyle(Number(event.target.value));
  });

  console.log("main finished");
}

main();
