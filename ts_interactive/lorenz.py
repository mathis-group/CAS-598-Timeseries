import numpy as np
from scipy.integrate import odeint
from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import gridplot, layout
from bokeh.models import ColumnDataSource, HoverTool, Range1d

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



#if __name__ == "__main__":

# Initial state (x0, y0, z0)
initial_state = [1.0, 1.0, 1.0]
TOOLS = "box_select,lasso_select,help"
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

t2 = figure(title="Y(t)", tools=TOOLS, background_fill_color="#fafafa", width=3*BASE_SIZE, height=BASE_SIZE)
t2.scatter(x='t', y='y', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

t3 = figure(title="Z(t)", tools=TOOLS, background_fill_color="#fafafa", width=3*BASE_SIZE, height=BASE_SIZE)
t3.scatter(x='t', y='z', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

p1 = figure(title="X-Y Plane", tools=TOOLS, background_fill_color="#fafafa",  width=BASE_SIZE, height=BASE_SIZE)
p1.scatter(x='x', y='y', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

p2 = figure(title="X-Z Plane", tools=TOOLS, background_fill_color="#fafafa", width=BASE_SIZE, height=BASE_SIZE)
p2.scatter(x='x', y='z', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

p3 = figure(title="Y-Z Plane", tools=TOOLS, background_fill_color="#fafafa", width=BASE_SIZE, height=BASE_SIZE)
p3.scatter(x='y', y='z', source=source, size=SCATTER_SIZE)#, line_width=1, alpha=0.7)

# Create a grid layout
grid = layout([[p1, p2, p3],
                 [t1],[t2],[t3]])

# Add the layout to the current document (Bokeh server)
curdoc().add_root(grid)