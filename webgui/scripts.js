// get references to the plot and slider DOM elements
const plot = document.querySelector("#plot");
const slider = document.querySelector("#slider");
const inputA = document.querySelector("#plf-a");
const inputB = document.querySelector("#plf-b");
const convTypeContainer = document.querySelector("#conv-type-container");
const deltaSign = document.querySelector("#delta-sign");
const deltaValue = document.querySelector("#delta-value");
const legend = document.querySelector("#legend");
const title = document.querySelector("#title");
const exportButton = document.querySelector("#export-button");

// python function and classes
let conv_at_x;
let ConvType;
let PLF;
let ConvProperties;

// initial values
let initialPLFAStr = "[(0, 0, 0), (1, 1, 0), (2, 2, 0), (3, 3, 0)], 5";
let initialPLFBStr = "[(0, 0, 0), (1, 0, 1)], 4";

// number of decimal places for the delta_value
const decimals = 2;

// the indices to use for the plot traces
const traceIndices = {
  a: 0,
  transformedA: 1,
  b: 2,
  sum: 3,
  sumMarker: 4,
  result: 5,
  resultMarker: 6,
};

// the current state
const state = {};

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

/**
 * Use katex to render text. Uses the throwOnError option and removes dollar signs.
 * @param {String} text Text to be rendered.
 * @param {Element} element DOM element to render into.
 */
function katexRender(text, element) {
  katex.render(text.replace(/\$/g, ""), element, { throwOnError: false });
}

/**
 * Computes the ranges for the plot such that the given coordinates are visible.
 * @param {Number} xmin Minimum x that must be visible.
 * @param {Number} xmax Maximum x that must be visible.
 * @param {Number} ymin Minimum y that must be visible.
 * @param {Number} ymax Maximum y that must be visible.
 * @returns An object with x and y properties that are the ranges for Plotly.
 */
function computePlotRanges(xmin, xmax, ymin, ymax) {
  const xrange = xmax - xmin;
  const yrange = ymax - ymin;
  const aspectRatio = plot.offsetWidth / plot.offsetHeight;

  // Target for y if we keep the xrange
  const targetY = xrange / aspectRatio;
  // Target for x if we keep the yrange
  const targetX = yrange * aspectRatio;

  if (targetY > yrange) {
    // Not enough vertical space -> pad in y direction
    const pad = (targetY - yrange) / 2;
    return {
      x: [xmin, xmax],
      y: [ymin - pad, ymax + pad],
    };
  } else {
    // Not enough horizontal space -> pad in x direction
    const pad = (targetX - xrange) / 2;
    return {
      x: [xmin - pad, xmax + pad],
      y: [ymin, ymax],
    };
  }
}

/**
 * Looks for a parameter in the URL. If the parameter exists,
 * a function will be applied to it to convert it to the desired type.
 * If the parameter doesn't exist, could not be decoded or applying the
 * function resulted in an error, the default value will be returned.
 *
 * @param {String} name Name of the Parameter.
 * @param {any} defaultValue Default value.
 * @param {Function} fn Function to be applied to the parameter. Defaults to identity.
 * @returns The converted parameter or the default value.
 */
function getParameter(name, defaultValue, fn = (x) => x) {
  const url = new URL(location);
  const value = url.searchParams.get(name);
  if (value !== null) {
    try {
      const decodedValue = decodeURIComponent(value);
      try {
        return fn(decodedValue);
      } catch (e) {
        console.warn(
          `parameter ${name} exists and was decoded to '${decodedValue},` +
            ` but loading it resulted in an error. Reverting to default value '${defaultValue}`
        );
        return defaultValue;
      }
    } catch (e) {
      console.warn(
        `parameter ${name} exists and is set to '${value}' but could not be decoded.` +
          ` Reverting to default value '${defaultValue}'`
      );
      return defaultValue;
    }
  } else {
    return defaultValue;
  }
}

/**
 * Loads pyodide, installs the needed packages and assigns some names to JS variables.
 */
async function initializePyodide() {
  let pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip");
  const micropip = pyodide.pyimport("micropip");
  await micropip.install("dist/rtcvis-0.3.0-py3-none-any.whl");
  pyodide.runPython(
    "from rtcvis import PLF, conv_at_x, ConvType, ConvProperties"
  );
  conv_at_x = pyodide.globals.get("conv_at_x");
  ConvType = pyodide.globals.get("ConvType");
  PLF = pyodide.globals.get("PLF");
  ConvProperties = pyodide.globals.get("ConvProperties");
}

/**
 * Initializes some RTCVis values in the state.
 */
function initializeRTCVis() {
  // load defaults
  initialPLFAStr = getParameter("plfA", initialPLFAStr);
  initialPLFBStr = getParameter("plfB", initialPLFBStr);
  state.plfA = PLF.from_rtctoolbox_str(initialPLFAStr);
  state.plfB = PLF.from_rtctoolbox_str(initialPLFBStr);
  state.convType = getParameter("convType", ConvType(0), (x) =>
    ConvType(Number(x))
  );
  state.currentX = getParameter("currentX", 0, Number);
}

/**
 * Setup some elements in the DOM.
 */
function setupDOM() {
  // put default values into the textfields
  inputA.value = initialPLFAStr;
  inputB.value = initialPLFBStr;

  // render the delta sign
  katexRender("\\Delta", deltaSign);

  // add radio buttons for selecting the conv type
  for (let convType of ConvType) {
    const button = document.createElement("button");
    button.value = convType.value;
    button.type = "button";
    button.classList.add("conv-type-button");
    katexRender(convType.operator_desc, button);
    button.innerHTML = String(convType) + ": " + button.innerHTML;

    convTypeContainer.appendChild(button);

    // input.addEventListener("change", updateConvType);
    button.addEventListener("click", updateConvType);
  }

  // Add listener to input elements
  slider.addEventListener("input", updateCurrentX);
  inputA.addEventListener("input", updatePLF);
  inputB.addEventListener("input", updatePLF);
  exportButton.addEventListener("click", exportConfiguration);
}

function setupPlot() {
  // create the traces to plot
  let traceA = {
    mode: "lines",
  };

  let traceTransformedA = {
    mode: "lines",
  };

  let traceB = {
    mode: "lines",
  };

  let traceSum = {
    mode: "lines",
    legendgroup: "group_sum",
    showlegend: true,
  };

  let traceSumMarker = {
    mode: "markers",
    legendgroup: "group_sum",
    showlegend: false,
  };

  let traceResult = {
    mode: "lines",
    legendgroup: "group_result",
    showlegend: true,
  };

  let traceResultMarker = {
    mode: "markers",
    legendgroup: "group_result",
    showlegend: false,
  };

  let traces = [
    traceA,
    traceTransformedA,
    traceB,
    traceSum,
    traceSumMarker,
    traceResult,
    traceResultMarker,
  ];

  // Set the correct visibilities
  const visibilities = getParameter("visibilities", "0111111");
  for (const [i, trace] of traces.entries()) {
    trace.visible =  visibilities.charAt(i) == "1" ? true : "legendonly";
  }

  // Create the plot
  Plotly.newPlot(
    plot,
    traces,
    {
      margin: { t: 0 },
      yaxis: {
        scaleanchor: "x",
        scaleratio: 1,
      },
      // The Latex in the legend gets rerendered in every restyle, which is too slow and the legend is thus disabled
      showlegend: false,
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
    },
    { responsive: true }
  );
}

/**
 * Updates the plot and the delta_value to a new current_x value.
 */
function currentXChanged() {
  // compute the next convAtXResult
  state.convAtXResult = conv_at_x(
    state.plfA,
    state.plfB,
    state.currentX,
    state.convType
  );

  // update the plot
  let x = [];
  let y = [];
  let updateIndices = [];

  x.push(toJsSafe(state.convAtXResult.transformed_a.x));
  y.push(toJsSafe(state.convAtXResult.transformed_a.y));
  updateIndices.push(traceIndices.transformedA);

  x.push(toJsSafe(state.convAtXResult.sum.x));
  y.push(toJsSafe(state.convAtXResult.sum.y));
  updateIndices.push(traceIndices.sum);

  x.push([state.convAtXResult.result.x]);
  y.push([state.convAtXResult.result.y]);
  updateIndices.push(traceIndices.sumMarker);

  x.push([state.currentX]);
  y.push([state.convProperties.result(state.currentX)]);
  updateIndices.push(traceIndices.resultMarker);

  Plotly.restyle(
    plot,
    {
      x: x,
      y: y,
    },
    updateIndices
  );

  // update the delta value
  deltaValue.innerText = String(state.currentX.toFixed(decimals)).padStart(
    state.padLength,
    " "
  );
}

/**
 * Redraws the entire plot. Should be used when the PLFs or the convolution type
 * change. Will also update the slider and and axis limits. Internally calls the
 * currentXChanged function but also updates the other traces.
 */
function redrawPlot() {
  // Recompute the convolution
  state.convProperties = ConvProperties(state.plfA, state.plfB, state.convType);
  state.currentX = Math.min(
    state.convProperties.slider_max,
    Math.max(state.convProperties.slider_min, state.currentX)
  );

  // Reset slider limits
  slider.min = state.convProperties.slider_min;
  slider.max = state.convProperties.slider_max;
  slider.value = state.currentX;

  // Set new title
  katexRender(
    `${state.convType.operator_desc} = ${state.convType.full_desc}`,
    title
  );
  title.innerHTML = String(state.convType) + ": " + title.innerHTML;

  // Compute padding for the delta_value
  state.padLength = Math.max(
    String(state.convProperties.slider_min.toFixed(decimals)).length,
    String(state.convProperties.slider_max.toFixed(decimals)).length
  );

  // Update the plot
  state.plotRanges = computePlotRanges(
    state.convProperties.min_x,
    state.convProperties.max_x,
    state.convProperties.min_y,
    state.convProperties.max_y
  );

  let x = [];
  let y = [];
  let names = [];
  let updateIndices = [];

  x.push(toJsSafe(state.plfA.x));
  y.push(toJsSafe(state.plfA.y));
  names.push(state.convType.a_desc);
  updateIndices.push(traceIndices.a);

  x.push(undefined);
  y.push(undefined);
  names.push(state.convType.a_trans_desc);
  updateIndices.push(traceIndices.transformedA);

  x.push(toJsSafe(state.plfB.x));
  y.push(toJsSafe(state.plfB.y));
  names.push(state.convType.b_desc);
  updateIndices.push(traceIndices.b);

  x.push(undefined);
  y.push(undefined);
  names.push(state.convType.sum_desc);
  updateIndices.push(traceIndices.sum);

  x.push(toJsSafe(state.convProperties.result.x));
  y.push(toJsSafe(state.convProperties.result.y));
  names.push(state.convType.operator_desc);
  updateIndices.push(traceIndices.result);

  Plotly.update(
    plot,
    {
      x: x,
      y: y,
      name: names,
    },
    {
      xaxis: { range: state.plotRanges.x },
      yaxis: { range: state.plotRanges.y },
    },
    updateIndices
  );

  // Update all remaining traces of the plot
  currentXChanged();

  // build the legend (some names may have changed)
  buildLegend();
}

/**
 * Build a custom legend.
 *
 * The PlotlyJS legend gets rerendered every time the plot gets updated,
 * which is very slow when using LaTeX names. We thus build our own
 * legend that also allows toggling the visibility of individual traces.
 */
function buildLegend() {
  legend.innerHTML = "";

  // Collect information about all traces
  let groups = {};
  plot.data.forEach((trace, idx) => {
    let key = trace.legendgroup !== undefined ? trace.legendgroup : idx;
    let color =
      plot._fullData[idx].line?.color || plot._fullData[idx].marker?.color;
    if (!groups[key]) {
      groups[key] = {
        name: trace.name,
        color: color,
        indices: [],
      };
    }
    groups[key].indices.push(idx);
  });

  // Create the legend entries
  for (const [group, info] of Object.entries(groups)) {
    let item = document.createElement("div");
    item.style.display = "flex";
    item.style.alignItems = "center";
    item.style.cursor = "pointer";
    item.style.marginBottom = "4px";

    let swatch = document.createElement("div");
    swatch.style.width = "12px";
    swatch.style.height = "12px";
    swatch.style.background = info.color || "black";
    swatch.style.marginRight = "6px";
    swatch.style.border = "1px solid #333";
    item.appendChild(swatch);

    let label = document.createElement("span");
    item.appendChild(label);

    katexRender(info.name, label);

    function updateLabelColor() {
      let hidden = plot.data[info.indices[0]].visible === "legendonly";
      label.style.color = hidden ? "#888" : "#000";
    }

    updateLabelColor();

    item.onclick = function () {
      let vis = plot.data[info.indices[0]].visible;
      let newVis = vis === true || vis === undefined ? "legendonly" : true;
      Plotly.restyle(plot, { visible: newVis }, info.indices);
      updateLabelColor();
    };

    legend.appendChild(item);
  }
  Plotly.Plots.resize(plot);
}

/**
 * Updates the currentX value and redraws the affected traces.
 * @param {Event} event Event from a range type input.
 */
function updateCurrentX(event) {
  state.currentX = Number(event.currentTarget.value);
  currentXChanged();
}

/**
 * Updates the corresponding PLF and redraws the entire plot.
 * @param {InputEvent} event Event from a text type input.
 */
function updatePLF(event) {
  const target = event.currentTarget;
  try {
    let newPLF = PLF.from_rtctoolbox_str(target.value);
    if (target.id == "plf-a") {
      state.plfA = newPLF;
    } else if (target.id == "plf-b") {
      state.plfB = newPLF;
    }
    redrawPlot();
    target.classList.remove("error");
  } catch (error) {
    target.classList.add("error");
  }
}

/**
 * Encodes all important settings the user made and adds them as encoded parameters to the URL.
 */
function exportConfiguration() {
  const settings = {
    plfA: inputA.value,
    plfB: inputB.value,
    convType: state.convType.value,
    currentX: state.currentX,
    visibilities: "",
  };
  for (const trace of plot.data) {
    const isVisible = trace.visible === true || trace.visible === undefined;
    settings.visibilities += isVisible ? "1" : "0";
  }

  const url = new URL(location);
  for (const [key, value] of Object.entries(settings)) {
    url.searchParams.set(key, encodeURIComponent(value));
  }
  window.history.pushState({}, "", url);
  navigator.clipboard.writeText(url.href);
}

/**
 * Updates the convType value and redraws the entire plot.
 * @param {Event} event Event from a radio type input.
 */
function updateConvType(event) {
  state.convType = ConvType(Number(event.currentTarget.value));
  redrawPlot();
}

async function main() {
  await initializePyodide();
  initializeRTCVis();
  setupDOM();
  setupPlot();
  redrawPlot();
}

main();
