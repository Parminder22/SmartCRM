import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="SmartCRM RFM Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Header
# ----------------------------
st.title("SmartCRM — RFM Customer Segmentation")
st.markdown("""
Analyze customer behavior using **Recency, Frequency, Monetary (RFM)** metrics,  
visualize segments, and generate actionable insights for marketing strategies.
""")

# ----------------------------
# Load data
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("customer_segments.csv")  # make sure CSV is in project folder

df = load_data()

# ----------------------------
# Sidebar filters
# ----------------------------
st.sidebar.header("Filters")
show_data = st.sidebar.checkbox("Show Raw Data")
segments = df['Segment'].unique()
selected_segments = st.sidebar.multiselect(
    "Select Segment(s)",
    segments,
    default=list(segments)
)
top_n = st.sidebar.slider("Top N customers by Monetary", 5, 50, 10)

filtered_df = df[df['Segment'].isin(selected_segments)]

# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs(["Charts", "Data", "Insights"])

# ----------------------------
# Tab 1: Data
# ----------------------------
with tabs[1]:
    st.subheader("Customer Data")
    if show_data:
        st.dataframe(filtered_df)
    st.download_button(
        label="Download Filtered Data",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_customers.csv",
        mime="text/csv"
    )

# ----------------------------
# Tab 2: Charts
# ----------------------------
with tabs[0]:
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", filtered_df.shape[0])
    col2.metric("Avg Recency", round(filtered_df['Recency'].mean(),2))
    col3.metric("Avg Frequency", round(filtered_df['Frequency'].mean(),2))
    col4.metric("Avg Monetary", round(filtered_df['Monetary'].mean(),2))

    st.subheader("Segment Distribution")
    pie_fig = px.pie(
        filtered_df,
        names='Segment',
        title="Customer Segments",
        color='Segment',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(pie_fig, use_container_width=True)

    st.subheader("RFM Distribution by Segment")
    fig, axes = plt.subplots(1,3, figsize=(18,5))
    sns.boxplot(data=filtered_df, x='Segment', y='Recency', ax=axes[0], palette="Set2")
    axes[0].set_title('Recency')
    sns.boxplot(data=filtered_df, x='Segment', y='Frequency', ax=axes[1], palette="Set2")
    axes[1].set_title('Frequency')
    sns.boxplot(data=filtered_df, x='Segment', y='Monetary', ax=axes[2], palette="Set2")
    axes[2].set_title('Monetary')
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader(f"Top {top_n} Customers by Monetary Value")
    st.dataframe(filtered_df.sort_values(by='Monetary', ascending=False).head(top_n))

# ----------------------------
# Tab 3: Insights
# ----------------------------
with tabs[2]:
    st.subheader("Segment Insights")

    # Define insights text for each segment
    insights_dict = {
        "High-Value Loyal Shoppers": "Engage frequently and spend the most, prioritize VIP offers.",
        "Frequent Spenders": "Moderate to high spending, can be upsold premium products.",
        "Regular Shoppers": "Consistent engagement, target for loyalty programs.",
        "Occasional Shoppers": "Low engagement, need retargeting campaigns.",
        "Inactive Shoppers": "Lost customers, consider win-back campaigns."
    }

    # Define card colors for each segment
    card_colors = {
        "High-Value Loyal Shoppers": "#FFD700",  # gold
        "Frequent Spenders": "#87CEEB",         # sky blue
        "Regular Shoppers": "#90EE90",          # light green
        "Occasional Shoppers": "#FFA07A",       # light salmon
        "Inactive Shoppers": "#D3D3D3"          # light gray
    }

    # Display segments in 2 columns per row
    for i in range(0, len(selected_segments), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(selected_segments):
                segment = selected_segments[i + j]
                seg_df = filtered_df[filtered_df['Segment'] == segment]

                # Card HTML
                card_style = f"""
                <div style='
                    background-color:{card_colors.get(segment,"#f0f2f6")};
                    padding:20px;
                    border-radius:15px;
                    margin-bottom:20px;
                    box-shadow:3px 3px 10px rgba(0,0,0,0.15);
                    color:black
                '>
                    <h3 style='text-align:center;'>{segment}</h3>
                    <p><b>Total Customers:</b> {seg_df.shape[0]}</p>
                    <p><b>Avg Recency:</b> {round(seg_df['Recency'].mean(),2)}</p>
                    <p><b>Avg Frequency:</b> {round(seg_df['Frequency'].mean(),2)}</p>
                    <p><b>Avg Monetary:</b> {round(seg_df['Monetary'].mean(),2)}</p>
                    <p><b>Insight:</b> {insights_dict.get(segment,'')}</p>
                </div>
                """

                col.markdown(card_style, unsafe_allow_html=True)
