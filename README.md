# rtcvis

rtcvis is an educational tool that can create interactive visualizations for convolution operations in the min-plus algebra, such as needed for real time calculus (RTC). RTC is a method for performance analysis of real time systems. Note that rtcvis cannot be used for performance analysis however, since it only supports finite curves - for this purpose, you can use the [RTC toolbox from ETH Zurich](https://www.mpa.ethz.ch/). Please note that I'm in no way affiliated with and that this project is in no way endorsed by ETH Zurich.

You can try it out here: https://epkrichi.github.io/rtcvis/

## Curve Syntax

Curves can be specified using a syntax similar to the one from [RTC toolbox](https://www.mpa.ethz.ch/):

```python
[(x, y, m), ...], l
```

- The first argument is a list of points: `x` and `y` are the coordinates of this points and `m` is the slope of the line section starting at this point.
- `l` is the length of the curve, or, in other words, the x coordinate at which the curve ends. Only finite curves are supported, which is why this parameter is mandatory.

Note that Curves are allowed to have discontinuities.

## Development

rtcvis is a python package and the web based frontend runs it using [pyodide](https://pyodide.org/en/stable/).

To install the package for development, clone it first and then run

```shell
pip install -e .\[dev,plot\]
pre-commit install
```

To build the package, you can use the build script:

```shell
./build.sh
```

Note that there is also code for a python (matplotlib) based frontend, but performance was poor, which is why I then created the web based frontend.
