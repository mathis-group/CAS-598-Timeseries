from bokeh.io import curdoc
# from bokeh.models import ColumnDataSource, Slider
# from bokeh.plotting import figure
# from bokeh.layouts import column

# # Sample data
# x = list(range(100))
# y = [xi**0.5 for xi in x]

# # Data source
# source = ColumnDataSource(data=dict(x=x, y=y))
# filtered_source = ColumnDataSource(data=dict(x=x, y=y))  # This will store the filtered data

# # Create a plot
# plot = figure(title="Data Plot with Range Slider", width=600, height=400)
# # plot.line('x', 'y', source=filtered_source)
# plot.scatter('x', 'y', source=filtered_source, size=1, color='black', alpha=0.5)

# # Create a range slider
# slider_start = Slider(start=min(x), end=max(x), value=min(x), step=2, title="Range Start")
# slider_end = Slider(start=min(x), end=max(x), value=max(x), step=1, title="Range End")

# # Callback function to update the plot based on the slider range
# def update_plot(attr, old, new):
#     # Get the current slider values
#     start = slider_start.value
#     end = slider_end.value
    
#     # Filter the data based on the slider range
#     selected_indices = [i for i, val in enumerate(source.data['x']) if start <= val <= end]
#     filtered_data = {k: [source.data[k][i] for i in selected_indices] for k in source.data}
    
#     # Update the plot's data source
#     filtered_source.data = filtered_data

# # Add callbacks to the sliders
# slider_start.on_change('value', update_plot)
# slider_end.on_change('value', update_plot)

# # Layout: Sliders + plot
# layout = column(slider_start, slider_end, plot)

# # Add layout to the current document
# curdoc().add_root(layout)

import numpy as np

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure, show
from bokeh.sampledata.stocks import AAPL

dates = np.array(AAPL['date'], dtype=np.datetime64)
source = ColumnDataSource(data=dict(date=dates, close=AAPL['adj_close']))

p = figure(height=300, width=800, tools="xpan", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(dates[1500], dates[2500]))

p.line('date', 'close', source=source)
p.yaxis.axis_label = 'Price'

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range, start_gesture="pan")
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('date', 'close', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)

layout = column(select, p)
curdoc().add_root(layout)
