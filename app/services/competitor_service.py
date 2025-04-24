import logging
import re
from datetime import datetime
from typing import Any, Dict, List
from collections import Counter
import statistics

from app.models.competitor import (
    Tweet, AnalyzedTweet, ContentFramework, 
    CompetitorAnalysisRequest, TweetCategory, TweetSentiment
)

# Set up logging
logger = logging.getLogger(__name__)

async def fetch_tweets(handle: str, limit: int = 200) -> List[Tweet]:
    """
    Fetch tweets from a Twitter handle.
    
    Args:
        handle: Twitter handle (without @)
        limit: Maximum number of tweets to fetch
        
    Returns:
        List[Tweet]: List of tweets from the handle
    """
    logger.info(f"Fetching tweets from Twitter handle: {handle}")
    
    # In a real implementation, this would use the Twitter API or twscrape
    # For now, we'll return mock data
    mock_tweets = []
    
    # Generate different types of tweets for variety
    tweet_types = [
        ("Match day! Chelsea vs Arsenal today at Stamford Bridge. #CFC #CHEARS", ["CFC", "CHEARS"], 800, 3500),
        ("What a goal by Mount! Chelsea leads 1-0. #CFC #Chelsea", ["CFC", "Chelsea"], 1200, 5000),
        ("POLL: Who should start in midfield against Arsenal? #CFC", ["CFC"], 300, 1500),
        ("Throwback to this Drogba masterclass against Arsenal. #CFC #TBT", ["CFC", "TBT"], 900, 4000),
        ("NEW SIGNING: Chelsea announces the signing of striker from Atletico Madrid! #CFC #Chelsea", ["CFC", "Chelsea"], 2000, 8000),
        ("Chelsea stats this season: 25 wins, 8 draws, 5 losses. #CFC #Stats", ["CFC", "Stats"], 500, 2000),
        ("What's your all-time Chelsea XI? Let us know in the comments! #CFC", ["CFC"], 400, 1800),
        ("Chelsea's new kit for next season is now available in our store! #CFC #NewKit", ["CFC", "NewKit"], 600, 2500),
        ("Injury update: Three players doubtful for the weekend. #CFC #Injuries", ["CFC", "Injuries"], 700, 3000),
        ("Happy birthday to Chelsea legend Frank Lampard! #CFC #SuperFrank", ["CFC", "SuperFrank"], 1500, 7000)
    ]
    
    # Create mock tweets with different timestamps
    for i in range(min(limit, 50)):
        tweet_type = tweet_types[i % len(tweet_types)]
        tweet_text, hashtags, retweets, likes = tweet_type
        
        # Vary the engagement slightly
        rt_variation = int(retweets * 0.2 * (i % 5 - 2) / 2)
        like_variation = int(likes * 0.2 * (i % 5 - 2) / 2)
        
        # Create tweet with different timestamps
        hour = (i % 24)
        day = (i % 7) # 0 = Monday, 6 = Sunday
        days_ago = i % 30
        
        tweet_date = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
        tweet_date = tweet_date.replace(day=tweet_date.day - days_ago)
        
        mock_tweets.append(Tweet(
            id=f"{handle}_tweet_{i}",
            text=tweet_text,
            author=handle,
            created_at=tweet_date,
            retweets=max(0, retweets + rt_variation),
            likes=max(0, likes + like_variation),
            replies=int((retweets + likes) * 0.05),
            hashtags=hashtags
        ))
    
    return mock_tweets

async def categorize_tweet(tweet: Tweet) -> TweetCategory:
    """
    Categorize a tweet based on its content.
    
    Args:
        tweet: Tweet to categorize
        
    Returns:
        TweetCategory: Category of the tweet
    """
    text = tweet.text.lower()
    
    # In a real implementation, this would use NLP or ML classification
    # For now, we'll use simple keyword matching
    if re.search(r'poll|what|who|how|when|where|why|your', text):
        return TweetCategory.QUESTION
    elif re.search(r'goal|score|leads|wins|match day|vs|against|played', text):
        return TweetCategory.NEWS
    elif re.search(r'stats|statistics|numbers|%|percent', text):
        return TweetCategory.STATS
    elif re.search(r'throwback|tbt|remember|classic|history', text):
        return TweetCategory.MEME
    elif re.search(r'available|store|buy|shop|merch|kit|ticket', text):
        return TweetCategory.PROMO
    elif re.search(r'think|should|opinion|view|perspective', text):
        return TweetCategory.COMMENTARY
    else:
        return TweetCategory.OTHER

async def analyze_sentiment(tweet: Tweet) -> TweetSentiment:
    """
    Analyze the sentiment of a tweet.
    
    Args:
        tweet: Tweet to analyze
        
    Returns:
        TweetSentiment: Sentiment of the tweet
    """
    text = tweet.text.lower()
    
    # In a real implementation, this would use NLP or OpenAI
    # For now, we'll use simple keyword matching
    positive_words = ['win', 'goal', 'lead', 'great', 'amazing', 'excellent', 'happy', 'congratulations', 'victory']
    negative_words = ['lose', 'lost', 'defeat', 'disappointing', 'injury', 'bad', 'poor', 'unfortunate']
    
    positive_count = sum(1 for word in positive_words if word in text)
    negative_count = sum(1 for word in negative_words if word in text)
    
    if positive_count > negative_count:
        return TweetSentiment.POSITIVE
    elif negative_count > positive_count:
        return TweetSentiment.NEGATIVE
    else:
        return TweetSentiment.NEUTRAL

async def analyze_tweets(tweets: List[Tweet]) -> List[AnalyzedTweet]:
    """
    Analyze a list of tweets.
    
    Args:
        tweets: List of tweets to analyze
        
    Returns:
        List[AnalyzedTweet]: List of analyzed tweets
    """
    analyzed_tweets = []
    
    for tweet in tweets:
        # Calculate engagement score
        engagement_score = (tweet.retweets * 2) + tweet.likes
        
        # Get hour and day
        hour_of_day = tweet.created_at.hour
        day_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][tweet.created_at.weekday()]
        
        # Categorize and analyze sentiment
        category = await categorize_tweet(tweet)
        sentiment = await analyze_sentiment(tweet)
        
        analyzed_tweets.append(AnalyzedTweet(
            **tweet.dict(),
            category=category,
            sentiment=sentiment,
            engagement_score=engagement_score,
            hour_of_day=hour_of_day,
            day_of_week=day_of_week
        ))
    
    return analyzed_tweets

async def generate_content_framework(analyzed_tweets: List[AnalyzedTweet], seed_accounts: List[str]) -> ContentFramework:
    """
    Generate a content framework from analyzed tweets.
    
    Args:
        analyzed_tweets: List of analyzed tweets
        seed_accounts: List of Twitter handles used for analysis
        
    Returns:
        ContentFramework: Generated content framework
    """
    # Calculate content categories distribution
    category_counts = Counter([tweet.category for tweet in analyzed_tweets])
    total_tweets = len(analyzed_tweets)
    content_categories = {category: count / total_tweets for category, count in category_counts.items()}
    
    # Calculate posting frequency
    # In a real implementation, this would be more sophisticated
    per_day = round(total_tweets / 30)  # Assuming 30 days of data
    per_week = per_day * 7
    
    # Find peak posting times
    hour_counts = Counter([tweet.hour_of_day for tweet in analyzed_tweets])
    day_counts = Counter([tweet.day_of_week for tweet in analyzed_tweets])
    
    # Get top 2 hours and days
    top_hours = [hour for hour, _ in hour_counts.most_common(2)]
    top_days = [day for day, _ in day_counts.most_common(2)]
    
    # Extract hashtag strategy
    all_hashtags = [hashtag for tweet in analyzed_tweets for hashtag in tweet.hashtags]
    hashtag_counts = Counter(all_hashtags)
    top_hashtags = [hashtag for hashtag, _ in hashtag_counts.most_common(5)]
    
    # Determine style presets
    # In a real implementation, this would use clustering or more sophisticated analysis
    # For now, we'll use simple heuristics
    avg_length = statistics.mean([len(tweet.text) for tweet in analyzed_tweets])
    emoji_usage = sum(1 for tweet in analyzed_tweets if re.search(r'[\U0001F300-\U0001F5FF]', tweet.text))
    question_usage = sum(1 for tweet in analyzed_tweets if '?' in tweet.text)
    
    style_presets = []
    if avg_length < 100:
        style_presets.append("concise")
    else:
        style_presets.append("detailed")
        
    if emoji_usage > total_tweets * 0.3:
        style_presets.append("emoji-heavy")
    
    if question_usage > total_tweets * 0.2:
        style_presets.append("engaging")
        
    # Add a tone based on sentiment analysis
    positive_tweets = sum(1 for tweet in analyzed_tweets if tweet.sentiment == TweetSentiment.POSITIVE)
    if positive_tweets > total_tweets * 0.6:
        style_presets.append("positive")
    elif positive_tweets < total_tweets * 0.4:
        style_presets.append("neutral")
    
    # Create content framework
    framework = ContentFramework(
        seedAccounts=seed_accounts,
        contentCategories=content_categories,
        postingFrequency={"perDay": per_day, "perWeek": per_week},
        peakTimes={"hours": top_hours, "days": top_days},
        hashtagStrategy=top_hashtags,
        stylePresets=style_presets
    )
    
    return framework

async def analyze_competitors(request: CompetitorAnalysisRequest, db: Any) -> ContentFramework:
    """
    Analyze competitors based on Twitter handles and generate a content framework.
    
    Args:
        request: The competitor analysis request containing Twitter handles
        db: Database connection
        
    Returns:
        ContentFramework: The generated content framework
    """
    logger.info(f"Analyzing competitors from Twitter handles: {request.seedAccounts}")
    
    try:
        all_tweets = []
        
        # 1. Fetch tweets from each handle
        for handle in request.seedAccounts:
            tweets = await fetch_tweets(handle, request.tweetLimit)
            logger.info(f"Fetched {len(tweets)} tweets from {handle}")
            all_tweets.extend(tweets)
        
        # 2. Analyze tweets
        analyzed_tweets = await analyze_tweets(all_tweets)
        logger.info(f"Analyzed {len(analyzed_tweets)} tweets")
        
        # 3. Generate content framework
        framework = await generate_content_framework(analyzed_tweets, request.seedAccounts)
        logger.info("Generated content framework")
        
        # 4. Save to database
        if db and request.pipelineId:
            # In a real implementation, this would save to the database
            # framework.id = await db.competitor_analyses.insert_one(framework.dict()).inserted_id
            framework.id = "framework_" + datetime.now().strftime("%Y%m%d%H%M%S")
            framework.pipelineId = request.pipelineId
        
        return framework
    except Exception as e:
        logger.error(f"Error analyzing competitors: {str(e)}")
        raise
