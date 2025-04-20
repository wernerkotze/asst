# Content Generator Wizard

## Purpose  
Step‑by‑step UI + backend to turn persona + framework + data feeds into final posts.

## Steps & Data Flow  
```text
1. Select Pipeline → GET /pipelines → choose pipelineId
2. Retrieve Content → POST /content/retrieve { pipelineId }
   • Backend fetches news, sports, tweets via NewsAPI, Football API, Twitter API
   • Returns array of raw items
3. Enhance → POST /content/enhance { itemIds, pipelineId }
   • Adds hashtags (from framework), sentiment tags, suggested media
4. Personalize → POST /content/personalize { enhancedText, personaId, stylePreset }
   • Uses OpenAI with prompt: "Write in [persona.voiceDescription], style=[preset]"
5. Image → POST /content/image { text }
   • Option to fetch from Google Images or generate via DALL·E
6. Format → POST /content/format { channel, text, mediaUrl }
   • Enforce length, preview Card UI
7. Preview & Send →  
   • Save to Drafts (Airtable)  
   • Or POST /schedule/post { contentId, schedule }  
```

## Key Models  
- **ContentItem** (temporary, in‑memory or Redis)  
- **ContentPiece** (persistent in `content_pieces`)

## UI Considerations  
- Wizard stepper at top  
- Clean preview pane for texts & images  
- Inline editing for tags/emojis  
- Channel toggles (Twitter only v1)  

## Implementation Notes
- Uses multiple external APIs for content retrieval
- Leverages OpenAI for content personalization
- May use DALL-E or similar for image generation
- Requires caching for in-progress content items
- Manages the flow from raw content to publishable posts

## Data Model (`content_pieces` collection)
```jsonc
{
  "_id": ObjectId,
  "pipelineId": ObjectId,
  "rawContent": {
    "source": "newsapi",
    "title": "Chelsea wins Premier League",
    "url": "https://example.com/news/123",
    "summary": "Chelsea FC has won the Premier League..."
  },
  "enhancedContent": {
    "text": "Chelsea wins Premier League! #ChelseaFC #CFC",
    "sentiment": "positive",
    "suggestedMedia": ["https://example.com/images/chelsea-win.jpg"]
  },
  "personalizedContent": {
    "text": "INCREDIBLE! Our boys in blue have done it again! Chelsea are Premier League champions! 🏆 #ChelseaFC #CFC",
    "stylePreset": "witty"
  },
  "finalContent": {
    "text": "INCREDIBLE! Our boys in blue have done it again! Chelsea are Premier League champions! 🏆 #ChelseaFC #CFC",
    "mediaUrls": ["https://storage.asst.ai/media/chelsea-win-generated.jpg"],
    "channel": "twitter",
    "status": "draft" // draft, scheduled, published, failed
  },
  "createdAt": ISODate,
  "updatedAt": ISODate
}
```

## API Endpoints
- `POST /content/retrieve` → Fetches raw content based on pipeline settings
- `POST /content/enhance` → Enhances raw content with hashtags and sentiment
- `POST /content/personalize` → Personalizes content using OpenAI
- `POST /content/image` → Generates or fetches images for content
- `POST /content/format` → Formats content for specific channels
- `POST /content/save` → Saves content as draft

## Integration Points
- Consumes pipeline configuration from Pipeline Manager
- Uses persona data from Brand Generation Tool
- Applies content framework from Competitor Analysis Tool
- Feeds final content to Scheduling & CMS
