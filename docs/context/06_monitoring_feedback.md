# Monitoring & Feedback

## Purpose  
Continuously fetch performance metrics and inform future pipelines.

## Workflow  
1. **Fetch Metrics** → Cron/Lambda runs `GET statuses/lookup` or `twscrape` for each `scheduled_post`  
2. **Compute Engagement** → `(retweets*2)+likes` → store in `engagement_metrics`  
3. **Analytics Dashboard**  
   - Charts: top‑performing categories, best times, winning tone  
   - Comparison: persona vs. competitor baseline  
4. **Feedback Loop**  
   - Optionally auto‑update competitor framework or send recommendations to user  
   - Display "Increase news posts on Wed 6pm" in UI

## Data Model (`engagement_metrics` collection)
```jsonc
{
  "_id": ObjectId,
  "scheduledPostId": ObjectId,     // reference to scheduled_posts
  "contentId": ObjectId,           // reference to content_pieces
  "pipelineId": ObjectId,          // reference to pipelines
  "platform": "twitter",
  "platformPostId": "1234567890",  // ID returned by platform API
  "metrics": {
    "impressions": 5000,
    "likes": 120,
    "shares": 45,
    "comments": 23,
    "clicks": 67,
    "profileVisits": 34,
    "followersGained": 12,
    "engagementRate": 4.8          // percentage
  },
  "measuredAt": ISODate,           // when metrics were collected
  "createdAt": ISODate,
  "updatedAt": ISODate
}
```

## UI Considerations  
- Metrics table per post (likes, RTs, score)  
- Trend graphs (line chart of engagement over time)  
- "Recommended Adjustment" callouts  

## Implementation Notes
- Uses scheduled Lambda functions to collect metrics
- Requires integration with platform-specific analytics APIs
- Implements statistical analysis for trend detection
- May use machine learning for recommendation generation
- Needs to handle rate limits from social platforms

## API Endpoints
- `GET /analytics/metrics/{postId}` → Gets metrics for a specific post
- `GET /analytics/pipeline/{pipelineId}` → Gets aggregated metrics for a pipeline
- `GET /analytics/recommendations/{pipelineId}` → Gets recommendations for improving performance
- `POST /analytics/apply-recommendations/{pipelineId}` → Automatically applies recommendations to pipeline

## Integration Points
- Consumes publishing data from Scheduling & CMS
- May feed back into Competitor Analysis Tool for framework updates
- Provides insights to Pipeline Manager for optimization
- Informs Content Generator about high-performing content types
