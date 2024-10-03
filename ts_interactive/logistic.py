import numpy as np
from bokeh.layouts import column, layout
from bokeh.models import Slider, ColumnDataSource, Range1d, HoverTool, FactorRange, Div
from bokeh.plotting import figure, curdoc

from pentropy import PermutationEntropy

# Function to compute the logistic map (r*x*(1-x)) over n iterations starting from x0
def logistic_map(r, x0, n):
    x = np.empty(n)  # Initialize an array to store the values
    x[0] = x0  # Set the initial condition
    for i in range(1, n):  # Iterate using the logistic map equation
        x[i] = r * x[i-1] * (1 - x[i-1])
    return x

# Sample initial values and compute the next iteration based on the logistic map
def sample_return_vals(r, n):
    xi = np.random.random(n).tolist()  # Generate random initial values
    next_xs = [logistic_map(r, x, 2)[1] for x in xi]  # Compute the next step in the map for each value
    return xi, next_xs

# Function to generate data for the ordinal pattern histogram
def generate_pattern_hist_data(pentropy, ordering):
    # Extract frequencies from the PermutationEntropy object, following the specified ordering
    pattern_frequencies = {k: pentropy.patterns[k] for k in ordering}
    # Convert patterns to strings and extract their frequencies for visualization
    patterns = [''.join(map(str, pattern)) for pattern in pattern_frequencies.keys()]
    frequencies = list(pattern_frequencies.values())

    # Prepare data dictionary for Bokeh
    data = {
        'patterns': patterns,  # Ordinal patterns as strings
        'frequencies': frequencies,  # Corresponding frequencies
        'vectors': [list(pattern) for pattern in pattern_frequencies.keys()],  # Tooltip data for each pattern
    }

    return data

# Update function called when slider values change
def update(attr, old, new):
    r = r_slider.value  # Get current value of r from the slider
    
    # Recompute the logistic map with new r
    x_values = logistic_map(r, initial_x, iterations)
    time_source.data = {
        'x': x_values,  # Update time series data
        't': [i for i in range(0, iterations)],  # Time (iteration) indices
    }

    # Sample return map values
    xs, next_xs = sample_return_vals(r, 1000)
    return_source.data = {
        'x_i': xs,  # Update return map data (x_i)
        'x_j': next_xs,  # Update return map data (x_{i-1})
    }

    timeseries = x_values  # Use updated logistic map for time series
    global K, x_ordering
    # Check if K (permutation size) has changed and update it if necessary
    if K != k_slider.value:
        K = k_slider.value
        # Recompute the Permutation Entropy with new K
        logistic_pe = PermutationEntropy(timeseries, K)
        # Order patterns by their frequency
        x_ordering = [k for k, _ in sorted(logistic_pe.patterns.items(), key=lambda item: item[1], reverse=True)] 
    else:
        # Recompute the Permutation Entropy with the current K
        logistic_pe = PermutationEntropy(timeseries, K)
    
    # Update pattern histogram data
    new_pe_data = generate_pattern_hist_data(logistic_pe, x_ordering)
    pe_hist.x_range = FactorRange(factors=new_pe_data["patterns"])  # Update x-axis with new patterns
    pe_hist_source.data = new_pe_data  # Update source data for the histogram

    # Update the permutation entropy text
    entropy_text.text = f"Permutation Entropy: {logistic_pe.compute_entropy():.3f}"  # Format to 4 decimal places


# Parameters for the logistic map
iterations = 100  # Number of iterations in the time series
initial_x = np.random.random()  # Random initial value for x

# K (permutation size for Permutation Entropy)
K = 3
# Initial value of r for the logistic map
r_initial = 3.6
# Generate the initial logistic map
x_values = logistic_map(r_initial, initial_x, iterations)

# Data sources for the Bokeh plots
time_source = ColumnDataSource(data={
    'x': x_values,  # Time series data
    't': [i for i in range(0, iterations)],  # Corresponding time steps
})

# Generate initial return map data
xs, next_xs = sample_return_vals(r_initial, 1000)
return_source = ColumnDataSource(data={
    'x_i': xs,  # Values of x_i
    'x_j': next_xs,  # Values of x_{i-1}
})

# Create two figures: one for time series and one for return map
plot_time = figure(title="Logistic Map: x_i vs. Time", sizing_mode="inherit")
plot_return = figure(title="Return Map: x_i vs. x_{i-1}",sizing_mode="inherit")

# Set axis labels for the time series plot
plot_time.xaxis.axis_label = "Iteration"
plot_time.yaxis.axis_label = "x_i"

# Set axis labels for the return map plot
plot_return.xaxis.axis_label = "x_{i-1}"
plot_return.yaxis.axis_label = "x_i"

# Set y-axis range for the time series and return map
plot_time.y_range = Range1d(0.0, 1.0)
plot_return.y_range = Range1d(0.0, 1.0)
plot_return.x_range = Range1d(0.0, 1.0)

# Plot the initial data
scatter_time = plot_time.line('t', 'x', line_width=1.0, source=time_source)  # Time series line plot
scatter_return = plot_return.scatter("x_i", "x_j", source=return_source)  # Return map scatter plot

# Initialize Permutation Entropy and its visualization
logistic_pe = PermutationEntropy(x_values, K)
x_ordering = [k for k, _ in sorted(logistic_pe.patterns.items(), key=lambda item: item[1], reverse=True)] 
pe_data = generate_pattern_hist_data(logistic_pe, x_ordering)
pe_hist = figure(title="Ordinal Distribution", x_range=pe_data["patterns"], sizing_mode="inherit")  # Histogram figure
pe_hist_source = ColumnDataSource(data=pe_data)  # Data source for histogram

# Create the ordinal pattern histogram
pe_hist.vbar(x='patterns', top='frequencies', width=0.9, source=pe_hist_source)

# Add hover tool to show vector patterns and frequencies in the tooltip
hover = HoverTool(tooltips=[
    ("Ordering", "@vectors"),  # Show ordinal patterns
    ("Frequency", "@frequencies")  # Show corresponding frequencies
])
pe_hist.add_tools(hover)

# Add axis labels to the histogram
pe_hist.xaxis.axis_label = "Ordinal Patterns"
pe_hist.xaxis.major_label_text_font_size = "0pt"  # Hide x-axis labels (patterns)
pe_hist.yaxis.axis_label = "Frequency"

# Create a Div to display the permutation entropy
entropy_text = Div(text=f"Permutation Entropy: {logistic_pe.compute_entropy():.3f}", 
                   styles={'font-size': '200%', 'color': 'blue'})

# Slider for adjusting the logistic parameter r
r_slider = Slider(start=2.0, end=4.0, value=r_initial, step=0.01, title="Logistic Parameter: r ")
# Slider for adjusting the permutation size K
k_slider = Slider(start=2, end=6, value=K, step=1, title="Permutation Sizes: K ")

# Attach update functions to sliders
r_slider.on_change('value', update)
k_slider.on_change('value', update)

slider_wrapper = Div(styles={"text-align": "center", "width":"100%"})
slider_spacer = Div(text="",styles={"text-align": "center", "width":"100%"})
text_column = column(slider_wrapper, r_slider, k_slider, slider_spacer, entropy_text, align='center')
text_column.sizing_mode= "stretch_width"

# Layout configuration and add to the current document
grid = layout([
    [plot_return, plot_time],  # Place return map and time series side by side
    [text_column, pe_hist]  # Sliders and histogram below
], sizing_mode="stretch_both")
curdoc().add_root(grid)  # Add layout to the Bokeh document
