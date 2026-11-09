# 👗 Pakistan Social Audience & Campaign Intelligence Engine

A Streamlit-based web application designed for Pakistani fashion brands (e.g., Lawn Suits) to discover audience segments, identify unusual marketing patterns, and generate data-driven recommendations from social media comments.

## 🎯 Project Overview
This project addresses the real business problem of marketing teams receiving thousands of mixed-language (English, Roman Urdu, Urdu) comments on Instagram, TikTok, and Facebook. Instead of simple sentiment analysis, this engine groups similar audience behaviors and identifies unusual campaign patterns.

## 🛠️ Features
1. **Dashboard:** Compares engagement rates across Reels, Photos, and Influencer posts.
2. **Audience Segments:** Uses K-Means clustering and TF-IDF to group comments into segments (Price-focused, Delivery-concerned, etc.).
3. **Unusual Patterns (Anomaly Detection):** Flags posts with statistically significant negative comment ratios or unusually high engagement.
4. **Action Plan:** Generates evidence-based marketing recommendations.

## 📊 Dataset
The dataset is synthetically generated to simulate a real-world Pakistani fashion brand, containing:
*   **25 Posts** (Table A format)
*   **450 Comments** (Table B format) featuring English, Roman Urdu, and Urdu texts.
