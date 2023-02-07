import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title('In search of Happiness')

df = pd.read_csv('happy.csv')

columns = list(df.columns[1:])
x_axis = st.selectbox("Select parameter for X axis", 
    options=[column.title().replace('_', ' ') for column in columns])
df_x = x_axis.lower().replace(' ', '_')
columns.remove(x_axis.lower().replace(' ', '_'))
y_axis = st.selectbox("Select parameter for Y axis", 
    options=[column.title().replace('_', ' ') for column in columns])
df_y = y_axis.lower().replace(' ', '_')

st.subheader(f'{x_axis} and {y_axis}')

show_countries = st.checkbox("Show country names?")
show_trend = st.checkbox("Show trend?")


figure = px.scatter(df, x=df_x, y=df_y, 
                    text='country' if show_countries else None,
                    labels={df_x: x_axis, df_y: y_axis},
                    trendline="ols" if show_trend else None
                    )


if False: #was if show_trend, result the same as trendline
    
    x_data = df[df_x].values.tolist()
    y_data = df[df_y].values.tolist()

    sum_x = sum(x_data)
    sum_x2 = sum([x**2 for x in x_data])
    sum_x_2 = sum_x**2
    sum_y = sum(y_data)
    sum_xy = sum([x*y for x, y in zip(x_data, y_data)])
    rowcount = len(x_data)

    trend_a = (rowcount*sum_xy - sum_x*sum_y)/(rowcount*sum_x2 - sum_x_2)
    trend_b = (sum_y*sum_x2 - sum_x*sum_xy)/(rowcount*sum_x2 - sum_x_2)
    print(f'{trend_a}, {trend_b}')
    x_trend = [min(x_data)*0.9, max(x_data)+min(x_data)*0.1]
    y_trend = [x*trend_a + trend_b for x in x_trend]

    trend_figure = px.line(x=x_trend, y=y_trend)
    layout = go.Layout(xaxis=dict(title=x_axis), yaxis=dict(title=y_axis))

    figure = go.Figure(layout = layout, data=figure.data + trend_figure.data)


st.plotly_chart(figure)