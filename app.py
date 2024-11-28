import streamlit as st
import numpy as np
import pandas as pd
import altair as alt



#Page title
st.set_page_config(page_title='Ramen Data Explorer', page_icon='📊')
st.title('Interactive Ramen Data Explorer')

#Question Header
st.subheader('Which Ramen Style is more Popular?')

#Load data - CSV to dataframe
df = pd.read_csv('data/ramen-ratings-cleaned.csv')
df.Stars = df.Stars.astype('float')

st.sidebar.header('Input Parameter')
#Ramen selection - dropdown menu for genre selection
st.sidebar.subheader('Ramen style selection parameter')
ramen_list = df.Style.unique()
ramen_selection = st.sidebar.multiselect('Select ramen style', ramen_list, ['Cup', 'Pack', 'Tray', 'Bowl'])

#Country selection 
st.sidebar.subheader('Country selection parameter')
country_list = df.Country.unique()
country_selection_list = st.sidebar.multiselect('Select country', country_list, ['Japan', 'Indonesia', 'China', 'Thailand', 'Taiwan'])
print(country_selection_list)

#Subset data - Filter dataframe based on selections
df_selection = df[df.Style.isin(ramen_selection) & df['Country'].isin(country_selection_list)]
reshaped_df = df_selection.pivot_table(index='Country', columns='Style', values='Stars', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='Country', ascending=False)

#Editable dataframe -
df_editor = st.data_editor(reshaped_df, height=212, use_container_width=True,
							column_config={'Country': st.column_config.TextColumn('Country')},
							num_rows='dynamic')

#Date prep for charting
df_chart = pd.melt(df_editor.reset_index(), id_vars='Country', var_name='Style', value_name='Stars')


c1, c2 = st.columns((7,4))
with c1:
	st.markdown("### Bar chart")
	bar_chart = alt.Chart(df_chart).mark_bar().encode(
		x=alt.X('Country:N', title='Country'),
			y=alt.Y('Stars:Q', title='Stars'),
			color='Style:N').properties(height=320)
	st.altair_chart(bar_chart, use_container_width=True)
with c2:
	st.markdown("### Pie Chart")

	#category - Style. value - Stars. Legend - Country
	base = alt.Chart(df_chart).encode(
			alt.Theta("Stars:Q").stack(True),
			alt.Color("Country:N").legend(None)
			)

	pie = base.mark_arc(outerRadius=120)
	text = base.mark_text(radius=150, size=15).encode(text="Style:N")

	pie + text


left, middle, right = st.columns(3)
right.link_button("Go back to portfolio", "https://ainurafifah00.github.io/", type='primary')
