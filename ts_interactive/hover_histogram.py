from bokeh.plotting import figure, curdoc
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, HoverTool, Range1d
import numpy as np

from pentropy import PermutationEntropy
from lorenz import lorenz_ts


def generate_pattern_hist(pentropy, ordering, title=None, ylim=None):
    pattern_frequencies = {k: pentropy.patterns[k] for k in ordering}
    # Convert pattern_frequencies (Counter) to lists for Bokeh
    patterns = [''.join(map(str, pattern)) for pattern in pattern_frequencies.keys()]
    frequencies = list(pattern_frequencies.values())

    # Prepare data for Bokeh
    source = ColumnDataSource(data={
        'patterns': patterns,
        'frequencies': frequencies,
        'vectors': [list(pattern) for pattern in pattern_frequencies.keys()],  # Tooltip vectors
    })


    # Initialize Bokeh plot
    p = figure(x_range=patterns, title=title) # toolbar_location=None, tools=""

    # Create the histogram
    p.vbar(x='patterns', top='frequencies', width=0.9, source=source)

    # Add hover tool
    hover = HoverTool(tooltips=[
        ("Ordering", "@vectors"),  # Display vector (ordinal pattern) in tooltip
        ("Frequency", "@frequencies")
    ])

    p.add_tools(hover)

    # Add axis labels
    p.xaxis.axis_label = "Ordinal Patterns"
    p.xaxis.major_label_text_font_size = "0pt"
    p.yaxis.axis_label = "Frequency"
    if ylim:
        p.y_range = Range1d(0, ylim)

    return p

def make_ts_plot(x,t, title=None):
    TOOLS = "box_select,lasso_select,help"
    p1 = figure(title=title, tools=TOOLS)
    p1.line(x, t, line_width=2, alpha=0.7)
    return p1

# Sample time series and randomized version
K = 5
timeseries, _, _, t = lorenz_ts([1.0, 1.0, 1.0], 50, 10000)
rand_ts = np.random.choice(timeseries, len(timeseries), replace=False)
# ts_plot = make_ts_plot(t, timeseries, title="Timeseries")

# Initialize Permutation Entropy class and get pattern frequencies
lorenz_pe = PermutationEntropy(timeseries, K)
print("Lorenz PE computed")
rand_pe = PermutationEntropy(rand_ts, K)
print("Rand PE computed")
# Define some aesthetic choices
x_ordering = [k for k, _ in sorted(lorenz_pe.patterns.items(), key=lambda item: item[1], reverse=True)] 
y_max = max(lorenz_pe.patterns.values())*1.05

p = generate_pattern_hist(lorenz_pe, x_ordering, title= "Lorenz Timeseries (X)", ylim=y_max)
q = generate_pattern_hist(rand_pe, x_ordering, title = "Random Control", ylim = y_max)


# Display the plot and the Div
layout = gridplot([[p, q]]) #,


# Add the layout to the current document (Bokeh server)
curdoc().add_root(layout)

