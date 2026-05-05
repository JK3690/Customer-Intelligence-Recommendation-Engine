import streamlit as st
from main import run_pipeline, show_customer_summary

st.markdown("""
<style>
/* Main background */
[data-testid="stAppViewContainer"] {background-color: #0E1117;}

/* Sidebar */
[data-testid="stSidebar"] {background-color: #111827;}

/* Buttons */
.stButton>button {background-color: #6366F1; color: white; border-radius: 8px;}

/* Metrics */
[data-testid="metric-container"] {background-color: #1E222A; padding: 10px; border-radius: 10px;}

/* Input box */
.stNumberInput input {background-color: #1E222A; color: white;}
</style>
""", unsafe_allow_html=True)

#-----LAYOUT-----
st.set_page_config(page_title="Customer Intelligence Dashboard", page_icon="📊", layout="wide")
st.title("Customer Intelligence & Recommendation Engine")
st.markdown("""
<div style="padding:10px 0;">
    <span style="color:#9CA3AF;">Customer analytics dashboard with segmentation, scoring, and recommendations</span>
</div>""", unsafe_allow_html=True)
st.caption("Analyze customer value, priority, and recommended actions using data-driven scoring.")
df=run_pipeline()

with st.sidebar:
        st.title("Customer Intelligence")

        st.markdown("### Filters for Insights")

        segment_filter = st.multiselect("Segment", options=df["segment"].unique(), default=df["segment"].unique())
        priority_filter = st.multiselect("Priority", options=df["priority"].unique(), default=df["priority"].unique())

#-----TABS-----
tab1, tab2, tab3 = st.tabs(["📊 Overview", "👤 Customer", "📈 Insights"])
with tab1:
    st.header("Overview")
    
    st.subheader("Top Customers")
    top = df.sort_values(by="final_score", ascending=False).head(10)
    st.dataframe(top[["Customer ID", "final_score", "priority"]], width='stretch', height=300)
    st.divider()
    
    total = len(df)
    p1 = (df["priority"] == "Priority 1").sum()

    m1, m2 = st.columns(2)
    m1.metric("Total Customers", total)
    m2.metric("High Priority Customers", p1)
    
with tab2:
    col1, col2 = st.columns([1, 2])
    
    with col1: 
        st.header("Customer Analysis")

        customer_id = st.number_input("Enter Customer ID (1-3900) & Press Button", step=1)
        analyze = st.button("Analyze Customer", disabled=(customer_id == 0))
        
    with col2:
        if analyze:
            result = show_customer_summary(df, customer_id)
        
            if not result:
                st.error("Customer not found")
                
            else:
                st.write("### Customer Summary")
                
                def priority_color(priority):
                    if priority == "Priority 1":
                        return "🔴"
                    elif priority == "Priority 2":
                        return "🟠"
                    else:
                        return "🟢"
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Priority", f"{priority_color(result['priority'])} {result['priority']}")
                m2.metric("Segment", result["segment"])
                m3.metric("Score", f"{result['final_score']:.2f}")
                st.divider()
                
                st.subheader("Recommended Action")
                st.markdown(f""" 
                <div style = "background-color:#1E222A; padding:15px; border-radius:10px; border-left:5px solid #6366F1;">
                <strong> {result["action"]} </strong>
                </div> """, unsafe_allow_html=True)
                st.divider()
                
                st.subheader("Insight")
                st.info(result["insight"])
                st.divider()

with tab3:
    st.header("Insights")
    
    filtered_df = df[(df["segment"].isin(segment_filter)) & (df["priority"].isin(priority_filter))]
    filtered_df = filtered_df.sort_values(by="final_score", ascending=False)
    
    st.subheader("Filtered Data")
    st.dataframe(filtered_df[["Customer ID", "segment", "priority", "final_score"]], width='stretch')
    st.divider()
    
    priority_counts = filtered_df["priority"].value_counts()
    st.subheader("Customer Priority Distribution")
    st.dataframe(priority_counts.rename("Count"), width="stretch")
    st.bar_chart(priority_counts, color="#6366F1")
    st.divider()
    
    st.subheader("Average Score by Segment")
    Segment_scores = filtered_df.groupby("segment")["final_score"].mean()
    st.bar_chart(Segment_scores, color="#6366F1")
    st.divider()

#streamlit run source/app.py