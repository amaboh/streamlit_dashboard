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
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]
    
category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()

with col1:
    st.subheader("Sales by Category")
    fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template = "seaborn")
    st.plotly_chart(fig, use_container_width=True, height = 200)
    
with col2:
    st.subheader("Sales by Region")
    fig = px.pie(filtered_df, values = "Sales", names = "Region", hole = 0.5)
    fig.update_traces(text =filtered_df["Region"], textposition = "outside")
    st.plotly_chart(fig, use_container_width=True)


# download data by category and region button
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                           help = "Click here to download the data as a CSV file")
        
with cl2:
    with st.expander("Region_ViewData"):
        region = filtered_df.groupby(by = "Region", as_index = False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime= "text/csv",
                        help = " Click to download the data as CSV file")


filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader(' Time Series Analysis')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales" : "Amount"}, height=500, width=1000, template="gridon")
st.plotly_chart(fig2, use_container_width=True)    

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data = csv, file_name = "TimeSeries.csv", mime='text/csv')
    
# Tree diagram for region, category, sub-category
st.subheader("Treemap of Sales")
fig3 = px.treemap(filtered_df, path = ["Region", "Category", "Sub-Category"], values = "Sales", hover_data= ["Sales"],
                  color = "Sub-Category")

fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)


chart1, chart2 = st.columns((2))

with chart1:
    st.subheader('Sales by Segments')
    fig = px.pie(filtered_df, values = "Sales", names="Segment", template = "plotly_dark")
    fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig, use_container_width=True)
    
with chart2:
    st.subheader('Sales by Category')
    fig = px.pie(filtered_df, values = "Sales", names="Category", template = 'gridon')
    fig.update_traces(text = filtered_df["Category"], textposition= "inside")
    st.plotly_chart(fig, use_container_width=True)
    