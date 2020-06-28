import pandas as pd
import yfinance as yf
from bokeh.plotting import figure, output_file, show

def get_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date, progress=False)

def make_plot(data, column, ticker=None):
    p = figure(x_axis_type="datetime", title=f"Stock {column} Prices", sizing_mode="stretch_width", plot_width=800, plot_height=600)
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'

    p.line(data.index, data[column], color='#A6CEE3', legend_label=ticker)
    if ticker:
        p.legend.location = "top_left"
    return p