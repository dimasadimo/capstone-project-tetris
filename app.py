import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

#st.set_page_config(layout="wide")

st.markdown("Developed by **Dimas Adi Hartomo**")
st.title("Chocolate Consumption and Happiness throughout the World")
st.markdown("---")

st.caption('According to the [portal news](https://www.liputan6.com/health/read/3776965/alasan-makan-cokelat-bisa-bikin-stres-menurun-dan-bahagia-meningkat), chocolate contains theobramine and phenylethylamine, which are responsible for regulating feelings of happiness. The human body releases the hormone that makes us feel happier when we consume chocolate.')
st.caption("Are there any data to support this claim? Let's find out...")

df_chocolate = pd.read_excel("https://docs.google.com/spreadsheets/d/e/2PACX-1vQEaB5kqREDO9ftItk0Oe_cMV3EttH_HryjtrzwyYu8ei3R_U1vU04iJuV31Z0Hrw/pub?output=xlsx")
df_hi = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTiNVCW218YXeJLpuKNjKzS4rObMCufRgLf27GlavQBHTR4WdErqp0sIsBr7I8jGQmPwaqrIUCUqWql/pub?gid=1456601958&single=true&output=csv")
df_chocolateV1 = df_chocolate.drop(['No', 'Continent'], axis=1)

df_chocolateV2 = df_chocolateV1.drop(['Country'], axis=1)

source_choco = df_chocolateV1.reset_index().melt(id_vars=["Country"], 
        var_name="Year", 
        value_name="Value")

line_chart = alt.Chart(source_choco).mark_line(interpolate='basis').encode(
    alt.X('Year', title='Year', scale=alt.Scale(domain=[2014, 2021]), axis=alt.Axis(tickCount=5)),
    alt.Y('Value', title='Consumption of Chocolate per Kilogram', scale=alt.Scale(domain=[0, 15])),
    color='Country:N'
).properties(
    title='Chocolate Consumption Countries Around the World in 2014-2021',
)

st.altair_chart(line_chart, use_container_width=True)

st.caption('This data indicates that chocolate consumption tends to remain flat across countries every year')

st.markdown("---")

df_chocolateV3 = df_chocolate.drop(['No'], axis=1)
source_chocobar = df_chocolateV3.groupby('Continent')[[2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]].sum().reset_index().melt(id_vars=["Continent"], 
        var_name="Year", 
        value_name="Sum Value")
    
bars = alt.Chart().mark_bar().encode(
    x='Year:O',
    y=alt.Y('mean(Sum Value):Q', title='Mean Yield'),
    color='Year:N',
)

error_bars = alt.Chart().mark_errorbar(extent='ci').encode(
    x='Year:O',
    y='Sum Value:Q'
)

bar_plot = alt.layer(bars, error_bars, data=source_chocobar, width=100).facet(column='Continent:N')

st.altair_chart(bar_plot, use_container_width=True)

st.caption('In the world, Europe consumes more chocolate than any other region')

st.markdown("---")

df_hiV1 = df_hi.drop(['rank', 'happiness2020', 'scoreDifference'], axis=1)
df_chocolateV4 = df_chocolate.drop(['No', 'Continent', 2014, 2015, 2016, 2017, 2018, 2019, 2020], axis=1)

df_merged = pd.merge(df_hiV1, df_chocolateV4, on='Country')
df_merged = df_merged.rename({2021: 'consumption'}, axis=1)
#st.dataframe(df_merged)

column_1 = df_merged["consumption"]
column_2 = df_merged["happiness2021"]
correlation = column_1. corr(column_2) 
#st.text(correlation)

fig = alt.Chart(df_merged).mark_point().encode(x='happiness2021',y='consumption',color='Country', tooltip=['Country', 'happiness2021', 'consumption'])

final_plot = fig + fig.transform_regression('happiness2021', 'consumption').mark_line() + fig.interactive()

st.altair_chart(final_plot, use_container_width=True)

st.markdown("---")