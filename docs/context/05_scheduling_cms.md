# Scheduling & CMS

## Purpose  
Store approved content, schedule publishing, and integrate with Airtable + Twitter API.

## Workflow  
1. **Save Draft** → Write to `content_pieces` with status=`draft`  
2. **Review Queue** UI reads drafts from Airtable table  
3. **Schedule** → POST `/schedule/post`  
   - Saves record in `scheduled_posts`  
   - Sets up an EventBridge rule or Lambda timer for `scheduledTime`  
4. **Publish** → at trigger time, Lambda calls Twitter API to post; updates `status` & `postedAt`  
5. **Failure Handling** → on error, record `failureReason`, send alert via CloudWatch alarm

## Data Model (`scheduled_posts` collection)
```jsonc
{
  "_id": ObjectId,
  "contentId": ObjectId,          // reference to content_pieces
  "pipelineId": ObjectId,         // reference to pipelines
  "channel": "twitter",
  "scheduledTime": ISODate,
  "status": "scheduled",          // scheduled, published, failed
  "postedAt": ISODate,            // when actually posted
  "platformPostId": "1234567890", // ID returned by platform API
  "failureReason": null,          // error message if failed
  "createdAt": ISODate,
  "updatedAt": ISODate
}
```

## UI Considerations  
- Calendar view (month/week) from Airtable data  
- Inline editing of schedule  
- Indicators: draft ● scheduled ● posted ✔ ● failed ✖  

## Implementation Notes
- Uses AWS EventBridge or similar for scheduling
- Integrates with Twitter API for publishing
- May use Airtable as a secondary storage/UI layer
- Requires error handling and retry logic
- Needs to handle rate limits from social platforms

## API Endpoints
- `POST /schedule/post` → Schedules a post for publishing
- `GET /schedule/posts` → Lists all scheduled posts
- `GET /schedule/posts/{id}` → Gets details of a specific scheduled post
- `PATCH /schedule/posts/{id}` → Updates scheduling details
- `DELETE /schedule/posts/{id}` → Cancels a scheduled post
- `POST /schedule/posts/{id}/publish-now` → Immediately publishes a scheduled post

## Integration Points
- Consumes final content from Content Generator
- Provides publishing status to Monitoring & Feedback
- May integrate with external calendar systems
- Feeds published content IDs to analytics collection
