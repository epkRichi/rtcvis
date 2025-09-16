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

async function main() {
  // get references to the plot and slider DOM elements
  const plot = document.querySelector("#plot");
  const slider = document.querySelector("#slider");
  const input_a = document.querySelector("#plf_a");
  const input_b = document.querySelector("#plf_b");
  const conv_type_container = document.querySelector("#conv_type_container");
  const delta_sign = document.querySelector("#delta-sign");
  const delta_value = document.querySelector("#delta-value");
  const legend = document.querySelector("#legend");
  const title = document.querySelector("#title");

  // load and initialize pyodide
  let pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip");
  const micropip = pyodide.pyimport("micropip");
  await micropip.install("dist/rtcvis-0.3.0-py3-none-any.whl");
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

  // render the delta sign
  katexRender("\\Delta", delta_sign);

  // create the PLFs to plot (static for now)
  let plf_a = PLF.from_rtctoolbox_str(input_a.value);
  let plf_b = PLF.from_rtctoolbox_str(input_b.value);
  let conv_type = ConvType(0);

  // add the title
  katexRender(`${conv_type.operator_desc} = ${conv_type.full_desc}`, title);
  title.innerHTML = String(conv_type) + ": " + title.innerHTML;

  // add radio buttons for selecting the conv type
  for (let ctype of ConvType) {
    const inputDiv = document.createElement("div");
    inputDiv.classList.add("form-check");
    inputDiv.classList.add("form-check-inline");

    const input = document.createElement("input");
    input.classList.add("form-check-input");
    input.type = "radio";
    input.name = "conv_type_radio";
    input.id = "conv_type_radio_" + ctype.value;
    input.value = ctype.value;
    input.checked = ctype.value == conv_type.value;

    const label = document.createElement("label");
    label.classList.add("form-check-label");
    label.for = input.id;
    katexRender(ctype.operator_desc, label);
    label.innerHTML = String(ctype) + ": " + label.innerHTML;

    inputDiv.appendChild(input);
    inputDiv.appendChild(label);
    conv_type_container.appendChild(inputDiv);

    input.addEventListener("change", update_conv_type);
  }

  // compute the convolution
  let conv_properties = ConvProperties(plf_a, plf_b, conv_type);
  let current_x = conv_properties.slider_min;
  let conv_result = conv_at_x(plf_a, plf_b, current_x, conv_type);

  // configure the slider
  slider.min = conv_properties.slider_min;
  slider.max = conv_properties.slider_max;
  slider.value = current_x;

  // number of decimal places for the delta_value
  const decimals = 2;

  // create the traces to plot
  let trace_a = {
    x: toJsSafe(plf_a.x),
    y: toJsSafe(plf_a.y),
    mode: "lines",
    name: conv_type.a_desc,
    visible: "legendonly",
  };

  let trace_transformed_a = {
    x: toJsSafe(conv_result.transformed_a.x),
    y: toJsSafe(conv_result.transformed_a.y),
    mode: "lines",
    name: conv_type.a_trans_desc,
  };

  let trace_b = {
    x: toJsSafe(plf_b.x),
    y: toJsSafe(plf_b.y),
    mode: "lines",
    name: conv_type.b_desc,
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

  // Compute the axis ranges
  let plot_ranges = computePlotRanges(
    conv_properties.min_x,
    conv_properties.max_x,
    conv_properties.min_y,
    conv_properties.max_y
  );

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
      xaxis: { range: plot_ranges.x },
      yaxis: {
        range: plot_ranges.y,
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

  /**
   * Updates the plot and the delta_value to a new current_x value.
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
    delta_value.innerText = String(current_x.toFixed(decimals)).padStart(
      padLength,
      " "
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

    // Set new title
    katexRender(`${conv_type.operator_desc} = ${conv_type.full_desc}`, title);
    title.innerHTML = String(conv_type) + ": " + title.innerHTML;

    // Recompute the plot ranges
    plot_ranges = computePlotRanges(
      conv_properties.min_x,
      conv_properties.max_x,
      conv_properties.min_y,
      conv_properties.max_y
    );

    // Compute padding for the delta_value
    padLength = Math.max(
      String(Number(slider.min).toFixed(decimals)).length,
      String(Number(slider.max).toFixed(decimals)).length
    );

    // Recompute all traces that aren't touched by current_x_changed
    trace_a = {
      x: toJsSafe(plf_a.x),
      y: toJsSafe(plf_a.y),
      name: conv_type.a_desc,
    };

    trace_transformed_a = {
      x: undefined,
      y: undefined,
      name: conv_type.a_trans_desc,
    };

    trace_b = {
      x: toJsSafe(plf_b.x),
      y: toJsSafe(plf_b.y),
      name: conv_type.b_desc,
    };

    trace_sum = {
      x: undefined,
      y: undefined,
      name: conv_type.sum_desc,
    };

    trace_result = {
      x: toJsSafe(conv_properties.result.x),
      y: toJsSafe(conv_properties.result.y),
      name: conv_type.operator_desc,
    };

    // build the legend
    buildLegend();

    // Update the plot, inlcuding the axis limits
    Plotly.update(
      plot,
      {
        x: [
          trace_a.x,
          trace_transformed_a.x,
          trace_b.x,
          trace_sum.x,
          trace_result.x,
        ],
        y: [
          trace_a.y,
          trace_transformed_a.y,
          trace_b.y,
          trace_sum.y,
          trace_result.y,
        ],
        name: [
          trace_a.name,
          trace_transformed_a.name,
          trace_b.name,
          trace_sum.name,
          trace_result.name,
        ],
      },
      {
        xaxis: { range: plot_ranges.x },
        yaxis: { range: plot_ranges.y },
      },
      [0, 1, 2, 3, 5]
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

      // Render LaTeX using KaTeX
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

  // Redraw to display the correct value in the delta_value
  // FIXME this is ugly
  redraw_plot();
}

main();
