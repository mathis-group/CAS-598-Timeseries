import numpy as np
from scipy.integrate import odeint

from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, RangeTool, Range1d
from bokeh.plotting import figure
from bokeh.sampledata.stocks import AAPL



# Lorenz system parameters
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

def lorenz_system(state, t):
    """Compute the derivatives for the Lorenz system."""
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

def lorenz_ts(initial_state, tmax, data_points):
    # Time points where we want the solution
    t = np.linspace(0, tmax, data_points)

    # Numerically integrate the Lorenz system
    solution = odeint(lorenz_system, initial_state, t)

    # Unpack the solution for x, y, z
    x, y, z = solution.T

    return x,y,z,t

def my_func(attr, old, new):
    # time.sleep(0.5) # some time consuming function
    print(range_tool.x_range.start, range_tool.x_range.end)

initial_state = [1.0, 1.0, 1.0]
TOOLS = "box_select,xbox_select,help"
x,y,z,t = lorenz_ts(initial_state, 30, 5000)
source = ColumnDataSource(data={
    'x': x,
    'y': y,
    'z': z,
    't': t
})
# Plotting the Lorenz attractor
# Create Bokeh figures
BASE_SIZE = 200
SCATTER_SIZE = 1
t1 = figure(title="X(t)", tools=TOOLS, background_fill_color="#fafafa",  width=3*BASE_SIZE, height=BASE_SIZE)
t1.scatter(x='t', y='x', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

t2 = figure(title="Y(t)", x_range=t1.x_range, tools=TOOLS, background_fill_color="#fafafa", width=3*BASE_SIZE, height=BASE_SIZE)
t2.scatter(x='t', y='y', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

t3 = figure(title="Z(t)", x_range=t1.x_range, tools=TOOLS, background_fill_color="#fafafa", width=3*BASE_SIZE, height=BASE_SIZE)
t3.scatter(x='t', y='z', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

p1 = figure(title="X-Y Plane", tools=TOOLS, background_fill_color="#fafafa",  width=BASE_SIZE, height=BASE_SIZE)
p1.scatter(x='x', y='y', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

p2 = figure(title="X-Z Plane", tools=TOOLS, background_fill_color="#fafafa", width=BASE_SIZE, height=BASE_SIZE)
p2.scatter(x='x', y='z', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

p3 = figure(title="Y-Z Plane", tools=TOOLS, background_fill_color="#fafafa", width=BASE_SIZE, height=BASE_SIZE)
p3.scatter(x='y', y='z', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=800, y_range=t1.y_range,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=t1.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

#Is there a way to "throttle" or only get a call when cursor is released
range_tool.x_range.on_change('start', my_func)

select.line('t', 'x', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)

# Create a grid layout
grid = layout([[p1, p2, p3],
               [select],
               [t1],[t2],[t3]])

# Add the layout to the current document (Bokeh server)
curdoc().add_root(grid)


# dates = np.array(AAPL['date'], dtype=np.datetime64)
# source = ColumnDataSource(data=dict(date=dates, close=AAPL['adj_close']))
# p = figure(height=300, width=800, tools="xpan", toolbar_location=None,
#            x_axis_type="datetime", x_axis_location="above",
#            background_fill_color="#efefef", x_range=(dates[1500], dates[2500]))
# p.line('date', 'close', source=source)
# p.yaxis.axis_label = 'Price'



# select = figure(title="Drag the middle and edges of the selection box to change the range above",
#                 height=130, width=800, y_range=p.y_range,
#                 x_axis_type="datetime", y_axis_type=None,
#                 tools="", toolbar_location=None, background_fill_color="#efefef")

# range_tool = RangeTool(x_range=p.x_range)
# range_tool.overlay.fill_color = "navy"
# range_tool.overlay.fill_alpha = 0.2

# #Is there a way to "throttle" or only get a call when cursor is released
# range_tool.x_range.on_change('start', my_func)

# select.line('date', 'close', source=source)
# select.ygrid.grid_line_color = None
# select.add_tools(range_tool)
# #select.toolbar.active_multi = range_tool

# #show(column(p, select))
# curdoc().add_root(column(p,select))