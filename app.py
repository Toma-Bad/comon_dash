import pandas as pd
from dash import Dash, dcc, html


data = (pd.read_csv("../temp1_mon_out.txt")
		.assign(datetime=lambda data: pd.to_datetime(data['datetime'],format = "%Y-%m-%d %H:%M:%S" ))
		.sort_values(by="datetime")
	)
app = Dash(__name__)
app.layout = html.Div(
		children = [
			html.Div(children = [html.H1(children="Indoor Air Quality Monitor",className="header-title"),
				html.P(
					children=(
					"Temperature, Humidity and CO2 Levels"
					),
					className="header-description",
					),

				],
				className="header",
				),

			html.Div(
				children=[
					html.Div(
						children=dcc.Graph(
							figure={
								"data": [
									{
										"x":data["datetime"],
										"y":data["temp"],
										"type":"scatter",
										"hovertemplate":("%{y:.1f} C<extra></extra>"),
									},
									],
								"layout":{
									"title":{
										"text":"Temperature Evolution [C]",
										"x": 0.05,
										"xanchor":"left",
										},
																		},
								},
							),
						className="card"
						),
					html.Div(
						children=dcc.Graph(
							figure={
								"data": [
									{
										"x":data["datetime"],
										"y":data["humid"],
										"type":"scatter",
										"hovertemplate":("%{y:.0f} %<extra></extra>"),
									},
									],
								"layout":{
									"title":{
										"text":"Humidity Evolution [%]",
										"x": 0.05,
										"xanchor":"left",
										},
									},
								},
							),
						className="card"
						),
					html.Div(
						children=dcc.Graph(
							figure={
								"data": [
									{
										"x":data["datetime"],
										"y":data["co2"],
										"type":"scatter",
										"hovertemplate":("%{y:.0f} ppm<extra></extra>"),							
									},
									],
								"layout":{
									"title":{
										"text":"CO2 Concentration Evolution [ppm]",
										"x": 0.05,
										"xanchor":"left",
										},
									},

								},
							),
						className="card"
						),
					],
				className="wrapper",
				),
			]

		)

if __name__ == "__main__":
    app.run_server(host = "0.0.0.0",port=443,debug=True)
#data = (
#    pd.read_csv("avocado.csv")
#    .query("type == 'conventional' and region == 'Albany'")
#    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d %H:%M:%S"))
#   .sort_values(by="Date")
#)131.220.98.205
