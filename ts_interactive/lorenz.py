import numpy as np
from scipy.integrate import odeint
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot
from bokeh.io import output_notebook


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



if __name__ == "__main__":

    # Initial state (x0, y0, z0)
    initial_state = [1.0, 1.0, 1.0]

    x,y,z,t = lorenz_ts(initial_state, 50, 10000)
    # Plotting the Lorenz attractor
    # Create Bokeh figures
    # output_notebook()
    p1 = figure(title="Lorenz Attractor: X-Y Plane", width=400, height=400)
    p1.line(x, y, line_width=2, alpha=0.7)

    p2 = figure(title="Lorenz Attractor: X-Z Plane", width=400, height=400)
    p2.line(x, z, line_width=2, alpha=0.7)

    p3 = figure(title="Lorenz Attractor: Y-Z Plane", width=400, height=400)
    p3.line(y, z, line_width=2, alpha=0.7)

    # Create a grid layout
    grid = gridplot([[p1, p2, p3]])

    # Show the result
    show(grid)