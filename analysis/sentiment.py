from transformers import pipeline

# Load the pre-trained sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    # Analyze sentiment using the model
    result = sentiment_pipeline(text)
    return result[0]['label']
