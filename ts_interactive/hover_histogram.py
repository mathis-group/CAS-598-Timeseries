from bokeh.plotting import figure, curdoc
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, Div
import numpy as np
from bokeh.resources import CDN

from pentropy import PermutationEntropy
from lorenz import lorenz_ts

K = 4
# Sample time series and K
timeseries, _, _, t = lorenz_ts([1.0, 1.0, 1.0], 50, 10000)
rand_ts = np.random.choice(timeseries, len(timeseries), replace=False)

# Initialize Permutation Entropy class and get pattern frequencies
lorenz_pe = PermutationEntropy(timeseries, K)
pattern_frequencies = {k: v for k, v in sorted(lorenz_pe.patterns.items(), key=lambda item: item[1], reverse=True)} 

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
p = figure(x_range=patterns, title="Permutation Entropy Histogram",
           toolbar_location=None, tools="")

# Create the histogram
p.vbar(x='patterns', top='frequencies', width=0.9, source=source)

# Add hover tool
hover = HoverTool(tooltips=[
    ("Vector", "@vectors"),  # Display vector (ordinal pattern) in tooltip
    ("Frequency", "@frequencies")
])

p.add_tools(hover)

# Add axis labels
p.xaxis.axis_label = "Ordinal Patterns"
p.xaxis.major_label_text_font_size = "0pt"
p.yaxis.axis_label = "Frequency"


# Rinse Repeat for the random control. I should wrap these up into nicer functions and just return the 
# layouts
rand_pe = PermutationEntropy(rand_ts, K)
rand_pattern_frequencies = {k: v for k, v in sorted(rand_pe.patterns.items(), key=lambda item: item[1], reverse=True)} 

# Convert pattern_frequencies (Counter) to lists for Bokeh
rand_patterns = [''.join(map(str, pattern)) for pattern in rand_pattern_frequencies.keys()]
rand_frequencies = list(rand_pattern_frequencies.values())

# Prepare data for Bokeh
rand_source = ColumnDataSource(data={
    'patterns': rand_patterns,
    'frequencies': rand_frequencies,
    'vectors': [list(rand_patterns) for rand_patterns in rand_pattern_frequencies.keys()],  # Tooltip vectors
})


# Initialize Bokeh plot
q = figure(x_range=rand_patterns,
           toolbar_location=None, tools="")

# Create the histogram
q.vbar(x='patterns', top='frequencies', width=0.9, source=rand_source)


q.add_tools(hover)

# Add axis labels
q.xaxis.axis_label = "Ordinal Patterns"
q.xaxis.major_label_text_font_size = "0pt"
q.yaxis.axis_label = "Frequency"


# Display the plot and the Div
layout = gridplot([[p, q]]) #,


# Add the layout to the current document (Bokeh server)
curdoc().add_root(layout)

