import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import os
import statistics 

TIMENAME = "DateTime"
REF1 = "Voltage"
ENV1  = "Temperature"
ENV2  = "Pressure"

fig = go.Figure()
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path) + '/'
df = pd.read_csv(dir_path + "LogFileA.csv")
#df[MAINDATA] = df[MAINDATA].rolling(10).mean()
#df[QUADATA] = df[QUADATA].rolling(10).mean()
#print(df[MAINDATA].mean())
#print(df[SECDATA].mean())
#print(df[THRDATA].mean())
df = df.dropna()

#x=df[TIMENAME]
fig.add_trace(go.Line(x=df[TIMENAME],y=df[REF1],name=REF1,yaxis="y1"))
fig.add_trace(go.Line(x=df[TIMENAME],y=df[ENV1],name=ENV1,yaxis="y5"))
fig.add_trace(go.Line(x=df[TIMENAME],y=df[ENV2],name=ENV2,yaxis="y6"))

print("Volts Mean: ",statistics.mean(df[REF1]))
print("Volts StDev: ",statistics.stdev(df[REF1]))
print("Temp Mean: ",statistics.mean(df[ENV1]))
print("Temp StDev: ",statistics.stdev(df[ENV1]))
print("Press Mean: ",statistics.mean(df[ENV2]))
print("Press StDev: ",statistics.stdev(df[ENV2]))

# Create axis objects
fig.update_layout(
    xaxis=dict(domain=[1, 1]),
    yaxis1=dict(
        title=REF1,
        titlefont=dict(color="#636EFA"),
        tickfont=dict(color="#636EFA"),
        hoverformat = '.6f'
    ),
    yaxis5=dict(
        title=ENV1,
        titlefont=dict(color="#FFA15A"),
        tickfont=dict(color="#FFA15A"),
        hoverformat = '.2f',
        anchor="x",
        overlaying="y",
        side="right",
    ),
    yaxis6=dict(
        title=ENV2,
        titlefont=dict(color="#19D3F3",),
        tickfont=dict(color="#19D3F3"),
        hoverformat = '.2f',
        anchor="x",
        overlaying="y",
        side="right"
    )
)

# Update layout properties
fig.update_layout(
    title_text="S7061 VS X7000 drift off",
    width=1900,
)

fig.show()