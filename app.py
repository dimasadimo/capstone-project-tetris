import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout="wide")

st.markdown("Developed by **Dimas Adi Hartomo**")
st.title("Chocolate Consumption and Happiness throughout the World")
st.markdown("---")

st.caption('According to the [portal news](https://www.liputan6.com/health/read/3776965/alasan-makan-cokelat-bisa-bikin-stres-menurun-dan-bahagia-meningkat), chocolate contains theobramine and phenylethylamine, which are responsible for regulating feelings of happiness. The human body releases the hormone that makes us feel happier when we consume chocolate.')
st.caption("Are there any data to support this claim? Let's find out...")

df_chocolate = pd.read_excel("https://docs.google.com/spreadsheets/d/e/2PACX-1vQEaB5kqREDO9ftItk0Oe_cMV3EttH_HryjtrzwyYu8ei3R_U1vU04iJuV31Z0Hrw/pub?output=xlsx")
df_chocolateV1 = df_chocolate.drop(['No', 'Continent'], axis=1)

df_chocolateV2 = df_chocolateV1.drop(['Country'], axis=1)

source_choco = df_chocolateV1.reset_index().melt(id_vars=["Country"], 
        var_name="Year", 
        value_name="Value")

line_chart = alt.Chart(source_choco).mark_line(interpolate='basis').encode(
    alt.X('Year', title='Year', scale=alt.Scale(domain=[2014, 2021])),
    alt.Y('Value', title='Consumption of Chocolate per Kilograms', scale=alt.Scale(domain=[0, 15])),
    color='Country:N'
).properties(
    title='Chocolate Consumption COuntries Around the World in 2014-2021',
    width=1500, height=800
)

st.altair_chart(line_chart, use_container_width=False)

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

bar_plot = alt.layer(bars, error_bars, data=source_chocobar).facet(column='Continent:N')

st.altair_chart(bar_plot, use_container_width=False)