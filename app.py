from flask import Flask, render_template, request
import pandas as pd
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.embed import components
import numpy as np
import datetime 

from utils import get_data, make_plot

app = Flask(__name__)

feature_names = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# Index page
@app.route('/')
def index():
	# Determine the selected feature
	current_feature_name = request.args.get("feature_name")
	search = request.args.get("search")
	date = request.args.get("date")

	if date:
		start_date = pd.to_datetime(date)
		end_date = start_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)
	else:
		start_date = pd.to_datetime(pd.datetime.now().strftime("%Y-%m")) # - pd.DateOffset(months=1)
		end_date = start_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)
	start_date_str = start_date.strftime("%m/%Y")

	if search == None:
		return render_template("index.html", ticker_exists=False, search=search,
				feature_names=feature_names,  current_feature_name=current_feature_name, start_date=start_date_str)

	data = get_data(search, start_date, end_date)
	if data.empty:
		#search = None
		return render_template("index.html", ticker_exists=False, search=search,
				feature_names=feature_names,  current_feature_name=current_feature_name, start_date=start_date_str)

	plot = make_plot(data, column=current_feature_name, ticker=search)
		
	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	print(feature_names)
	return render_template("index.html", script=script, div=div, ticker_exists=True, search=search,
							feature_names=feature_names,  current_feature_name=current_feature_name, start_date=start_date_str)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)