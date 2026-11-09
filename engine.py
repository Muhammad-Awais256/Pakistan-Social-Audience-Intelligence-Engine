import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def load_data():
    # Load the cleaned datasets
    posts = pd.read_csv("posts_clean.csv")
    comments = pd.read_csv("comments_clean.csv")
    return posts, comments

def cluster_comments(comments, n_clusters=7):
    # Safety check: Ensure n_clusters does not exceed the number of comments
    n_clusters = min(n_clusters, len(comments)) 
    
    # Initialize TF-IDF Vectorizer for text processing (handles both English and Roman Urdu)
    vec = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1, 2))
    X = vec.fit_transform(comments['comment_text'].astype(str))
    
    # Apply K-Means clustering
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    comments['cluster'] = km.fit_predict(X)
    
    # Extract top keywords for each cluster to understand the segment
    terms = vec.get_feature_names_out()
    cluster_labels = {}
    for i in range(n_clusters):
        center = km.cluster_centers_[i]
        # Get indices of the top 8 words in the cluster center
        top_idx = center.argsort()[-8:][::-1]
        cluster_labels[i] = ", ".join([terms[j] for j in top_idx])
    
    return comments, cluster_labels

# ==========================================
# TESTING BLOCK (Executes only if run directly)
# ==========================================
if __name__ == "__main__":
    print("--- 1. Loading Data ---")
    try:
        posts, comments = load_data()
        print(f"✅ Success: {len(posts)} posts and {len(comments)} comments loaded.")
    except FileNotFoundError as e:
        print(f"❌ ERROR: File not found! Please run fix_data.py first. Details: {e}")
        exit()

    print("\n--- 2. Clustering Comments ---")
    # Perform clustering (will automatically adjust if there are fewer than 7 comments)
    comments, labels = cluster_comments(comments, n_clusters=7) 
    
    print("✅ Clustering Done. Top words per cluster:")
    for cid, words in labels.items():
        print(f"   Cluster {cid}: {words}")

    print("\n--- DONE! You can now run the Streamlit app ---")