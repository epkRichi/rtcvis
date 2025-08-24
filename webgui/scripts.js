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

TESTER = document.getElementById("tester");
Plotly.newPlot(
  TESTER,
  [
    {
      x: [1, 2, 3, 4, 5],
      y: [1, 2, 4, 8, 16],
    },
  ],
  {
    margin: { t: 0 },
  }
);
const input = document.querySelector("#slider");
input.addEventListener("input", (event) => {
  let dx = Number(event.target.value);
  Plotly.restyle(
    TESTER,

    {
      x: [[1 + dx, 2 + dx, 3 + dx, 4 + dx, 5 + dx]],
      y: [[1, 2, 4, 8, 16]],
    }
  );
});
let plf_a, plf_b;

async function main() {
  let pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip");
  const micropip = pyodide.pyimport("micropip");
  await micropip.install("../dist/rtcvis-0.2.0-py3-none-any.whl");
  pyodide.runPython(`
        from rtcvis import PLF, conv_at_x, ConvType
      `);
  // let conv_at_x = pyodide.globals.get("conv_at_x");
  // let ConvType = pyodide.globals.get("ConvType");
  let plf_a_points = [
    [0, 0, 0],
    [1, 1, 0],
    [2, 2, 0],
    [3, 3, 0],
  ];
  let plf_a_length = 5;
  // let plf_b_str = "[(0, 0, 0), (1, 0, 1)], 5";
  let PLF = pyodide.globals.get("PLF");
  let plf_a = PLF.from_rtctoolbox(plf_a_points, plf_a_length);
  // let plf_a = pyodide.runPython("PLF.from_rtctoolbox(" + plf_a_str + ")");
  // let plf_b = pyodide.runPython("PLF.from_rtctoolbox(" + plf_b_str + ")");
  // let conv_result = conv_at_x(plf_a, plf_b, 0, ConvType.MIN_PLUS_CONVOLUION);

  Plotly.restyle(TESTER, {
    x: [toJsSafe(plf_a.x)],
    y: [toJsSafe(plf_a.y)],
  });
  console.log("main finished");
}
main();
