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
  let plf_b = PLF.from_rtctoolbox([[0, 0, 0], [1, 0, 1]], 5);

  Plotly.newPlot(
    plot,
    [
      {
        x: [],
        y: [],
      },
    ],
    {
      margin: { t: 0 },
    }
  );

  let conv_result = null;
  function restyle(value) {
    conv_result = conv_at_x(plf_a, plf_b, value, ConvType.MIN_PLUS_CONV);
    Plotly.restyle(
      plot,
      {
        x: [toJsSafe(conv_result.transformed_a.x)],
        y: [toJsSafe(conv_result.transformed_a.y)],
      }
    );
  }

  input.addEventListener("input", (event) => {
    restyle(Number(event.target.value));
  });

  restyle(0);

  console.log("main finished");
}

main();
