# CAS-598-Timeseries
Interactive Visualization of Classic Complex Timeseries

# Logistic Map

The logistic map is a classic example of determinstic chaos. You can find out more about the map, on [Wikipedia](https://en.wikipedia.org/wiki/Logistic_map)

The map is an iterative dynamical system, that has the following update rule: $x_{i+1} = r x_{i} *(1-x_{i})$, where its common to only apply this to $ x \in (0,1)$

Despite it's elegent description, it contains a many diverse unfoldings. Depending on the value of $r$, successive iterations of this map can lead to fix points, limit cycles, and chaotic timeseries.

To play around with this, use the interactive visualization in `ts_interactive/logistic.py`

To launch the Bokeh serve do the following:
1) setup a virtual enviroment `python -m venv logistic`
2) activate the virtual environment using `source logistic/bin/activate`
3) install the dependencies `pip install -r requirements.txt`
4) run `bokeh serve --show ts_interactive/logistic.py `

You can play around with different values of `r` and `K` to see what the return map, timeseries, and ordinal distributions look like. 