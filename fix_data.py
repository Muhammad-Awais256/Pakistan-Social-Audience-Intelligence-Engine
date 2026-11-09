import pandas as pd

print("Data ko saaf kiya ja raha hai...")

# 1. Comments File ko padho (Comma separator use karke)
try:
    comments = pd.read_csv('comments.csv', sep=',', on_bad_lines='skip', encoding='utf-8')
    comments['purchase_intent'] = comments['purchase_intent'].fillna('None')
    # Sirf pehle 6 columns rakho (baqi extra kachra hata do)
    comments = comments.iloc[:, :6]
    
    # Naye column names assign karo
    comments.columns = ['post_id', 'comment_text', 'language_type', 'topic', 'sentiment', 'purchase_intent']
    
    # Khaali rows hata do
    comments = comments.dropna(subset=['comment_text'])
    
    # Wapas save karo
    comments.to_csv('comments_clean.csv', index=False)
    print(f"✅ Comments file saaf ho gayi! Total comments: {len(comments)}")
    print("Pehli 3 comments aisi hain:")
    print(comments.head(3))
except Exception as e:
    print(f"❌ Comments file mein error: {e}")

# 2. Posts File ko padho
try:
    posts = pd.read_csv('posts.csv', sep=',', on_bad_lines='skip', encoding='utf-8')
    posts.to_csv('posts_clean.csv', index=False)
    print(f"\n✅ Posts file saaf ho gayi! Total posts: {len(posts)}")
except Exception as e:
    print(f"❌ Posts file mein error: {e}")