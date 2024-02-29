import pandas as pd
from dash import Dash, dcc, html, Input, Output, State

import plotly.graph_objects as go


rooms = ["1","3","4","5"]
colors = ["blue","orange","green","blue"]
source_files = [f"./data/temp{_r}_mon_out.txt" for _r in rooms]
room_names = [f"Room {_r}" for _r in rooms]
df_list = {}
for _r in rooms:
    source_file = f"../temp{_r}_mon_out.txt"
    print(_r)
    _df = pd.read_csv(source_file).assign(datetime=lambda data: pd.to_datetime(data['datetime'],format = "%Y-%m-%d %H:%M:%S" )).sort_values(by="datetime")
    _df["room"] = _r
    df_list[_r]= _df
coldict = dict(zip(rooms,colors))
app = Dash(__name__)
temperature_fig = {
        "data":[
            {
                "x":df_list[_r]["datetime"],
                "y":df_list[_r]["temp"],
                "type":"scattergl",
                "hoverplate":("%{y:.1f} C<extra></extra>"),
                "name":_r,
                "visible":True,
                "marker":{"color":coldict[_r]},
            } for _r in rooms 
          ],
        "layout":{
            "title":"Temperature Evolution [C]",
            "legend":{"title":{"text":"Rooms"}},
            "showlegend":True,
            "x": 0.05,
            "xanchor":"Left",
            
            },
        }

humidity_fig = {
        "data":[
            {
                "x":df_list[_r]["datetime"],
                "y":df_list[_r]["humid"],
                "type":"scattergl",
                "hoverplate":("%{y:.1f} %<extra></extra>"),
                "name":_r,
                "visible":True,
                "marker":{"color":coldict[_r]},
            } for _r in rooms 
          ],
        "layout":{
            "title":"Huimidity Evolution [%]",
            "x": 0.05,
            "xanchor":"Left",
            "legend":{"title":{"text":"Rooms"}},
            "showlegend":True,
            },
        }

co2_fig = {
        "data":[
            {
                "x":df_list[_r]["datetime"],
                "y":df_list[_r]["co2"],
                "type":"scattergl",
                "hoverplate":("%{y:.1f} ppm<extra></extra>"),
                "name":_r,
                "visible":True,
                "marker":{"color":coldict[_r]},
            } for _r in rooms 
          ],
        "layout":{
            "title":"CO2 Evolution [ppm]",
            "x": 0.05,
            "xanchor":"Left",
            "legend":{"title":{"text":"Rooms"}},
            "showlegend":True,
            },
        }

#data = (pd.concat(df_list,copy=False)) 
app.layout = html.Div(
        children = [
            #title
			html.Div(
                children = [html.H1(children="Indoor Air Quality Monitor",className="header-title"),
                    html.P(
                        children=("Temperature, Humidity and CO2 Levels"),
                        className="header-description",
                        ),
                    ],
                className="header",
                ),
            #menu checklist
            html.Div(children = dcc.Checklist(
                id="room-filter",
                options = dict(zip(rooms,room_names)),
                value = ["1"],
                inline=True,),
                ),
            #the plots
            html.Div(
                children = [
                    html.Div(children=dcc.Graph(id = "temperature-plot",figure=temperature_fig),className="card"),
                    html.Div(children=dcc.Graph(id = "humidity-plot",figure=humidity_fig),className="card"),
                    html.Div(children=dcc.Graph(id = "co2-plot",figure=co2_fig),className="card"),
                    ],
                className="wrapper",
                ),
            ],
        )

            
        

@app.callback(
    Output("temperature-plot", "figure"),
    Output("humidity-plot", "figure"),
    Output("co2-plot", "figure"),
    Input("room-filter", "value"),
    [State("temperature-plot","figure"),
        State("humidity-plot","figure"),
        State("co2-plot","figure")]
)
def update_plots(input_rooms,*existing):
    #print(input_rooms)
    #print(existing)
    for _fig in existing:
        for _t in _fig["data"]:
            _t["visible"] = (_t["name"] in input_rooms)
            #_t["color"] = coldict[_t["name"]]

    return existing


if __name__ == "__main__":
    app.run_server(debug=True)

