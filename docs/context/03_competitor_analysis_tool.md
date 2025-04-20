# Competitor Analysis Tool

## Purpose  
Build a **Content Framework** by studying up to 5 seed accounts: content mix, posting cadence, engagement behaviors, and writing‑style patterns.

## Workflow  
1. **Input**  
   - Up to 5 Twitter handles  
2. **Data Collection**  
   - For each handle, call `twscrape.api.user_tweets_and_replies(handle, limit=200)`  
   - Store in `rawTweets`  
3. **Analysis Steps**  
   - **Categorization**: tag tweets by type (news, commentary, meme, promo)  
   - **Engagement Scoring**: `(retweets*2) + likes`  
   - **Temporal**: histogram of posts by hour/day  
   - **Hashtag Extraction**: top N hashtags by frequency & engagement  
   - **Sentiment**: run OpenAI or TextBlob → label + score  
   - **Writing‑Style**: cluster tweets by features (avg length, emoji usage, punctuation) → expose 2–3 style presets  
4. **Framework Generation**  
   - `contentCategories`: e.g. `[{"News":40},{"Meme":30},…]`  
   - `postingFrequency`: `{ perDay:3, perWeek:20 }`  
   - `peakTimes`: `{ hours:[12,18], days:["Tue","Thu"] }`  
   - `hashtagStrategy`: `["#ChelseaFC","#CFC"]`  
   - `stylePresets`: `["witty","formal"]`  
5. **Output & Save**  
   - Write to `competitor_analyses` collection  

## Data Model (`competitor_analyses` collection)  
```jsonc
{
  "_id": ObjectId,
  "pipelineId": ObjectId,
  "seedAccounts": ["@ChelseaFC","@talkchelsea"],
  "contentCategories": [{"News":40},{"Meme":30},{"Opinion":30}],
  "postingFrequency": {"perDay":3,"perWeek":21},
  "peakTimes": {"hours":[12,18],"days":["Sat","Tue"]},
  "hashtagStrategy": ["#ChelseaFC","#CFC","#KTBFFH"],
  "stylePresets": ["witty","concise"],
  "createdAt": ISODate,
  "updatedAt": ISODate
}
```

## API Endpoint  
- `POST /analyze/competitors` → Accepts `{ seedAccounts: string[] }`, returns framework JSON.

## UI Considerations  
- Multi‑input for seed handles, validation of handle format  
- Loading spinner per account→"Fetching 200 tweets…"  
- Tabbed report: Categories | Engagement | Calendar | Style presets  
- "Save Framework" button  

## Implementation Notes
- Uses Twitter API or scraping tools for data collection
- Requires text analysis for categorization and sentiment analysis
- Leverages statistical analysis for temporal patterns
- Stores results in MongoDB for future reference
- Links to a specific pipeline via `pipelineId`

## Integration Points
- Provides content framework to Content Generator
- Informs scheduling decisions in Scheduling & CMS
- Referenced by Pipeline Manager via `competitorAnalysisId`
- Feeds hashtag strategy to content formatting
