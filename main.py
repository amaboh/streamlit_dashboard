import streamlit as st
import plotly.express as px
import pandas as pd
import os 
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Shopping Center!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Shopping Center EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

f1 = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt","xlsx", "xls"]))
if f1 is not None:
    filename = f1.name
    st.write(filename)
    
    # Check file extension
    if filename.endswith('.xls') or filename.endswith('.xlsx'):
        df = pd.read_excel(f1)
    else:
        df = pd.read_csv(f1, encoding="ISO-8859-1")
else:
    os.chdir("/Volumes/AM/Desktop/Projects/streamlit_dashboard")
    df = pd.read_excel("Sample-store.xls")
    
col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Get min and max dates 
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
    
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))
    
df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header("Choose a filter: ")

# Create selector for region
region = st.sidebar.multiselect(" Pick a Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# Create selector for state
state = st.sidebar.multiselect("Pick a state", df2["State"].unique())
if not state:
    df3 = df2.copy()
else: 
    df3 = df2[df2["State"].isin(state)]
    
#Create city selector
city = st.sidebar.multiselect("Pick a City", df3["City"].unique())
    
    
# Filter the data based on Region, State and City
 
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df["State"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["State"].isin(region) & df3["City"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(city)]