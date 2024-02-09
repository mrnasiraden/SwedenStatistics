
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sweden Statistics", page_icon=":bar_chart:", layout="wide")

# ---- READ DATA ----
@st.cache_data
def get_data():
    df = pd.read_csv('project1_data.csv')
    df.rename({'marital status': 'marital_status'}, axis=1, inplace=True)

    return df

df = get_data()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
county = st.sidebar.multiselect(
    "Select the County:",
    options=df["county"].unique(),
    default=df["county"].unique()[0]
)

gender = st.sidebar.multiselect(
    "Select Gender:",
    options=df["sex"].unique(),
    default=df["sex"].unique(),
)

marital_status = st.sidebar.multiselect(
    "Select Marital Status:",
    options=df["marital_status"].unique(),
    default=df["marital_status"].unique()
)

year = st.sidebar.multiselect(
    "Select Year:",
    options=df["year"].unique(),
    default=[2022]
)

df_selection = df.query(
    "county == @county & sex ==@gender & marital_status == @marital_status & year == @year"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# ---- MAINPAGE ----
st.title(":bar_chart: Sweden Statistics")
st.markdown("##")

# TOP KPI's
total_population = int(df_selection["population"].sum())
marital_mode = df_selection["marital_status"].value_counts().index[0]
total_counties = int(df_selection["county"].nunique())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Population:")
    st.subheader(f"{total_population:,}")
with middle_column:
    st.subheader("Most Marital Status:")
    st.subheader(f"{marital_mode}")
with right_column:
    st.subheader("Total Counties:")
    st.subheader(f"{total_counties}")

st.markdown("""---""")

population_by_gender = df_selection.groupby(by=["sex", "year"])[["population"]].sum().reset_index()

# Line plot
fig_pop_by_gender = px.line(
    population_by_gender,
    x='year',
    y='population',
    color='sex',
    markers=True,
    labels={'population': 'Population', 'year': 'Year'},
    title='Population Trends by Gender Over the Years',
    template='plotly_white'
)


sex_distribution = df_selection.groupby("sex")["population"].sum().reset_index()
# Pie chart
fig_sex_distribution = px.pie(
    sex_distribution,
    names="sex",  # Use the correct column name
    values="population",  # Use the correct column name
    title='Sex Distribution',
    template='plotly_white',
    labels={'sex': 'Sex', 'population': 'Count'},  # Use the correct column name
)

marital_status_distribution = df_selection.groupby("marital_status")["population"].sum().reset_index()

fig_marital_status_entire = px.pie(
    marital_status_distribution,
    names='marital_status',
    values='population',
    title='Marital Status Distribution'
)

age_distribution = df_selection.groupby("age")["population"].sum().reset_index()


fig_age_distribution = px.histogram(
    age_distribution,
    x="age",  
    y="population",  
    title='Age Distribution',
    template='plotly_white',
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_pop_by_gender, use_container_width=True)
left_column.plotly_chart(fig_marital_status_entire, use_container_width=True)
right_column.plotly_chart(fig_sex_distribution, use_container_width=True)
right_column.plotly_chart(fig_age_distribution, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
