import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from engine import load_data, cluster_comments
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Set page configuration
st.set_page_config(page_title="Audience Intelligence Engine", layout="wide")
st.title("👗 Audience Intelligence Engine — Pakistani Lawn Suits")
st.markdown("Discover audience segments, identify unusual patterns, and generate marketing actions.")

# Load and process data
# Load and process data
@st.cache_data
def process_data():
    posts, comments = load_data()
    comments, cluster_labels = cluster_comments(comments, n_clusters=7)
    
    posts = posts.copy()
    
    # FIX 1: Agar columns missing hain toh unhein default values ke sath banao
    if 'likes' not in posts.columns: posts['likes'] = 100
    if 'comments_count' not in posts.columns: posts['comments_count'] = 10
    if 'shares' not in posts.columns: posts['shares'] = 5
    if 'views' not in posts.columns: posts['views'] = 1000
    if 'content_type' not in posts.columns: posts['content_type'] = 'General Post'
    
    # FIX 2: Data types ko numbers mein convert karo (agar text mein hain toh)
    posts['likes'] = pd.to_numeric(posts['likes'], errors='coerce').fillna(0)
    posts['comments_count'] = pd.to_numeric(posts['comments_count'], errors='coerce').fillna(0)
    posts['shares'] = pd.to_numeric(posts['shares'], errors='coerce').fillna(0)
    posts['views'] = pd.to_numeric(posts['views'], errors='coerce').fillna(1000)
    
    # FIX 3: Views ko 1 karo taake divide by zero error na aaye
    posts['views'] = posts['views'].replace(0, 1)
    
    # Engagement Rate Calculate karo
    posts['engagement_rate'] = (posts['likes'] + posts['comments_count'] * 2 + posts['shares'] * 3) / posts['views']
    
    # Negative Ratio for Anomaly Detection
    neg_counts = comments[comments['sentiment'] == 'Negative'].groupby('post_id').size()
    all_counts = comments.groupby('post_id').size()
    neg_ratio = (neg_counts / all_counts).fillna(0)
    posts['negative_ratio'] = posts['post_id'].map(neg_ratio).fillna(0)
    
    # Anomaly flag
    posts['anomaly_flag'] = posts['negative_ratio'] > 0.30
    
    return posts, comments, cluster_labels

posts, comments, cluster_labels = process_data()

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👥 Audience Segments", "🚨 Unusual Patterns", "✅ Action Plan"])

# --- TAB 1: DASHBOARD ---
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Posts", len(posts))
    col2.metric("Total Comments", len(comments))
    col3.metric("Avg Engagement Rate", f"{posts['engagement_rate'].mean():.2%}")
    col4.metric("Anomalies Detected", posts['anomaly_flag'].sum())
    
    st.markdown("---")
    st.subheader("Which content attracts attention?")
    
    # Bar chart for engagement by post
    fig = px.bar(posts, x='post_id', y='engagement_rate', color='content_type',
                 title="Engagement Rate by Post",
                 labels={'engagement_rate': 'Engagement Rate', 'post_id': 'Post ID'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("What does the audience want? (Topic Distribution)")
    topic_counts = comments['topic'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    fig_pie = px.pie(topic_counts, names='Topic', values='Count', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)


# --- TAB 2: AUDIENCE SEGMENTS ---
with tab2:
    st.subheader("Discovered Audience Segments (K-Means Clustering)")
    st.write("The AI has grouped comments into the following distinct segments based on their keywords:")
    
    # Display clusters and their top words
    for cid, words in cluster_labels.items():
        st.info(f"**Segment {cid}:** Top keywords include: `{words}`")
        
    st.markdown("---")
    st.subheader("Explore Segment Comments")
    selected_cluster = st.selectbox("Select a Segment to view raw comments:", sorted(comments['cluster'].unique()))
    filtered_comments = comments[comments['cluster'] == selected_cluster]
    st.dataframe(filtered_comments[['post_id', 'comment_text', 'language_type', 'sentiment']], use_container_width=True)


# --- TAB 3: UNUSUAL PATTERNS ---
with tab3:
    st.subheader("🚨 Anomaly Detection (Unusual Patterns)")
    st.write("These posts have an unusually high ratio of negative comments compared to normal posts. This requires further investigation.")
    
    anomalies = posts[posts['anomaly_flag']]
    if len(anomalies) > 0:
        st.dataframe(anomalies[['post_id', 'content_type', 'campaign', 'engagement_rate', 'negative_ratio']], use_container_width=True)
    else:
        st.success("No unusual patterns detected in the current dataset.")


# --- TAB 4: ACTION PLAN ---
with tab4:
    st.subheader("📋 Evidence-Based Marketing Recommendations")
    st.write("Based on the data and AI analysis, here is what the marketing team should do next:")
    
    # Dynamic Recommendations based on data
    recommendations = []
    
    # 1. Price Recommendation
    price_share = len(comments[comments['topic'].str.contains('price', case=False)]) / len(comments)
    if price_share > 0.20:
        recommendations.append("🔴 **Price Inquiries:** Over 20% of comments are about price. **Action:** Add 'PKR [Price]' directly in the caption for the next 2 Reels to reduce repeated questions.")
        
    # 2. Delivery Recommendation
    delivery_share = len(comments[comments['topic'].str.contains('delivery', case=False)]) / len(comments)
    if delivery_share > 0.10:
        recommendations.append("🟠 **Delivery Concerns:** Customers are worried about delivery. **Action:** Pin a comment with exact delivery timelines and logistics info on every post.")
        
    # 3. Anomaly Recommendation
    if len(anomalies) > 0:
        recommendations.append(f"⚠️ **Negative Sentiment Alert:** Post(s) {', '.join(anomalies['post_id'].astype(str).tolist())} have unusually high negative comments. **Action:** Investigate the comments immediately, address complaints publicly, or consider an apology/update post.")

    if len(recommendations) == 0:
        recommendations.append("🟢 Continue current content strategy. Engagement is stable and no major audience concerns were detected.")
        
    for rec in recommendations:
        st.markdown(rec)
