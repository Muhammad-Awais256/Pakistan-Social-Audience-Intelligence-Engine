
import pandas as pd
import random

random.seed(42)

# ==========================================
# FILE 1: GENERATE POSTS DATASET
# ==========================================

brands = ["Sapphire", "Khaadi", "Gul Ahmed", "Limelight"]
platforms = ["Instagram", "TikTok", "Facebook"]
campaigns = ["Eid Collection", "11.11 Sale", "Winter Wear"]

content_types = [
    "Reel",
    "Photo",
    "Influencer Post",
    "Styling Video"
]

posts = []

for i in range(1, 26):

    post_id = f"P{i:03d}"
    brand = random.choice(brands)
    platform = random.choice(platforms)
    campaign = random.choice(campaigns)
    content_type = random.choice(content_types)

    days_since_post = random.randint(1, 30)

    # Engagement based on content type
    if content_type in ["Reel", "Influencer Post", "Styling Video"]:
        views = random.randint(20000, 100000)
        likes = random.randint(1000, 5000)
        comments_count = random.randint(100, 500)
        shares = random.randint(100, 1000)

    else:
        views = random.randint(5000, 20000)
        likes = random.randint(100, 1000)
        comments_count = random.randint(20, 150)
        shares = random.randint(10, 200)

    # Special anomaly: P015
    if post_id == "P015":

        content_type = "Photo"
        views = 5000
        likes = 180
        comments_count = 250
        shares = 15

    # Exceptional engagement: P008
    if post_id == "P008":

        content_type = "Reel"
        views = 250000
        likes = 18000
        comments_count = 1800
        shares = 6500

    posts.append({
        "post_id": post_id,
        "brand": brand,
        "platform": platform,
        "campaign": campaign,
        "content_type": content_type,
        "likes": likes,
        "comments_count": comments_count,
        "shares": shares,
        "views": views,
        "days_since_post": days_since_post
    })

posts_df = pd.DataFrame(posts)

posts_df.to_csv(
    "posts.csv",
    index=False,
    encoding="utf-8-sig"
)

print("posts.csv created successfully!")


# ==========================================
# FILE 2: GENERATE COMMENTS DATASET
# ==========================================

comment_templates = {

    "price": {
        "Positive": [
            ("English", "The price seems reasonable for this design."),
            ("Roman Urdu", "Price quality ke hisaab se achi hai."),
            ("Urdu", "قیمت مناسب لگ رہی ہے۔")
        ],
        "Neutral": [
            ("English", "What is the price of this suit?"),
            ("Roman Urdu", "Is suit ki price kya hai?"),
            ("Urdu", "قیمت کتنی ہے؟")
        ],
        "Negative": [
            ("English", "The price is too expensive."),
            ("Roman Urdu", "Price bohat zyada hai."),
            ("Urdu", "قیمت بہت زیادہ ہے۔")
        ]
    },

    "delivery": {
        "Positive": [
            ("English", "My order arrived on time."),
            ("Roman Urdu", "Meri delivery time par mil gayi."),
            ("Urdu", "میرا آرڈر وقت پر پہنچ گیا۔")
        ],
        "Neutral": [
            ("English", "How many days will delivery take?"),
            ("Roman Urdu", "Delivery kitne din mein hogi?"),
            ("Urdu", "ڈیلیوری کتنے دن میں ہوگی؟")
        ],
        "Negative": [
            ("English", "Ordered last week, still waiting for delivery."),
            ("Roman Urdu", "Last week order kiya tha abhi tak parcel nahi aya."),
            ("Urdu", "پچھلے ہفتے آرڈر کیا تھا، ابھی تک پارسل نہیں آیا۔")
        ]
    },

    "sizing": {
        "Positive": [
            ("English", "The size fits perfectly."),
            ("Roman Urdu", "Size bilkul perfect hai."),
            ("Urdu", "سائز بالکل درست ہے۔")
        ],
        "Neutral": [
            ("English", "Do you have small and medium sizes?"),
            ("Roman Urdu", "Small aur medium dono available hain?"),
            ("Urdu", "کیا چھوٹے اور درمیانے سائز دستیاب ہیں؟")
        ],
        "Negative": [
            ("English", "The size is smaller than expected."),
            ("Roman Urdu", "Size expected se chota nikla."),
            ("Urdu", "سائز توقع سے چھوٹا نکلا۔")
        ]
    },

    "availability": {
        "Positive": [
            ("English", "Glad this design is back in stock!"),
            ("Roman Urdu", "Acha hua ye design dobara available hai."),
            ("Urdu", "اچھا ہوا یہ ڈیزائن دوبارہ دستیاب ہے۔")
        ],
        "Neutral": [
            ("English", "Is this available in Karachi?"),
            ("Roman Urdu", "Ye Karachi mein available hai?"),
            ("Urdu", "کیا یہ ڈیزائن دستیاب ہے؟")
        ],
        "Negative": [
            ("English", "My size is always out of stock."),
            ("Roman Urdu", "Mera size hamesha out of stock hota hai."),
            ("Urdu", "میرا سائز ہمیشہ دستیاب نہیں ہوتا۔")
        ]
    },

    "fabric_quality": {
        "Positive": [
            ("English", "The fabric quality looks amazing."),
            ("Roman Urdu", "Fabric ki quality bohat achi hai."),
            ("Urdu", "کپڑے کا معیار بہت اچھا ہے۔")
        ],
        "Neutral": [
            ("English", "How is the fabric quality?"),
            ("Roman Urdu", "Fabric kaisa hai?"),
            ("Urdu", "کپڑے کا معیار کیسا ہے؟")
        ],
        "Negative": [
            ("English", "The fabric quality is disappointing."),
            ("Roman Urdu", "Fabric ki quality bilkul achi nahi."),
            ("Urdu", "کپڑے کا معیار اچھا نہیں ہے۔")
        ]
    },

    "discount": {
        "Positive": [
            ("English", "Great discount, definitely worth buying!"),
            ("Roman Urdu", "Discount bohat acha hai, order karungi."),
            ("Urdu", "بہت اچھا ڈسکاؤنٹ ہے۔")
        ],
        "Neutral": [
            ("English", "Is there any discount available?"),
            ("Roman Urdu", "Koi discount available hai?"),
            ("Urdu", "کیا کوئی ڈسکاؤنٹ دستیاب ہے؟")
        ],
        "Negative": [
            ("English", "The discount is too small."),
            ("Roman Urdu", "Discount bohat kam hai."),
            ("Urdu", "ڈسکاؤنٹ بہت کم ہے۔")
        ]
    },

    "general_praise": {
        "Positive": [
            ("English", "This dress is absolutely beautiful!"),
            ("Roman Urdu", "Bohat khoobsurat dress hai."),
            ("Urdu", "بہت خوبصورت ڈریس ہے۔")
        ],
        "Neutral": [
            ("English", "Can you share more pictures?"),
            ("Roman Urdu", "Iski aur pictures share kar dein."),
            ("Urdu", "اس کی مزید تصاویر شیئر کر دیں۔")
        ],
        "Negative": [
            ("English", "The design looks different from the pictures."),
            ("Roman Urdu", "Pictures mein design different lag raha tha."),
            ("Urdu", "تصاویر میں ڈیزائن مختلف لگ رہا تھا۔")
        ]
    }
}


comments = []

topics = list(comment_templates.keys())

for i in range(450):

    # Concentrate negative delivery complaints on P015
    if i < 45:

        post_id = "P015"
        topic = "delivery"
        sentiment = "Negative"

    else:

        post_id = f"P{random.randint(1, 25):03d}"

        topic = random.choice(topics)

        # General sentiment distribution
        sentiment = random.choices(
            ["Positive", "Neutral", "Negative"],
            weights=[45, 35, 20],
            k=1
        )[0]

    # Select matching language and comment
    language, comment_text = random.choice(
        comment_templates[topic][sentiment]
    )

    # Purchase intent based on sentiment and topic
    if sentiment == "Negative":
        purchase_intent = random.choice(["Low", "None"])

    elif sentiment == "Positive":
        purchase_intent = random.choice(["High", "Low"])

    else:
        if topic in ["price", "availability", "sizing", "discount"]:
            purchase_intent = random.choice(["High", "Low", "None"])
        else:
            purchase_intent = random.choice(["Low", "None"])

    comments.append({
        "post_id": post_id,
        "comment_text": comment_text,
        "language_type": language,
        "topic": topic,
        "sentiment": sentiment,
        "purchase_intent": purchase_intent
    })


comments_df = pd.DataFrame(comments)

comments_df.to_csv(
    "comments.csv",
    index=False,
    encoding="utf-8-sig"
)

print("comments.csv created successfully!")


# ==========================================
# DATASET VALIDATION
# ==========================================

print("\n========== DATASET SUMMARY ==========")

print("\nPosts Dataset:")
print("Total Posts:", len(posts_df))
print("Unique Post IDs:", posts_df["post_id"].nunique())

print("\nComments Dataset:")
print("Total Comments:", len(comments_df))
print("Unique Post IDs in Comments:", comments_df["post_id"].nunique())

print("\nComments by Language:")
print(comments_df["language_type"].value_counts())

print("\nComments by Sentiment:")
print(comments_df["sentiment"].value_counts())

print("\nComments by Topic:")
print(comments_df["topic"].value_counts())

print("\nComments on P015:")
print(comments_df[
    comments_df["post_id"] == "P015"
]["sentiment"].value_counts())

print("\nBoth CSV files generated successfully!")
