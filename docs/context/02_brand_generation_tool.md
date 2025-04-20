# Brand Generation Tool

## Purpose  
Automatically infer a brand's visual identity and voice from curated image/text sources (e.g., Pinterest boards, uploaded assets). Outputs a reusable **Persona Profile**.

## Workflow  
1. **Input**  
   - Pinterest Board ID or URL  
   - Optional manual uploads: logo files, style guides (SVG, PNG, PDF)  
2. **Data Fetch**  
   - Call Pinterest API `/v5/boards/{board_id}/pins`  
   - Store raw pin data in `rawPins` array  
3. **Image Analysis**  
   - For each pin image URL: fetch and run ColorThief → get dominant color  
   - Aggregate top 5 hex codes  
4. **Text Analysis**  
   - Combine all pin descriptions  
   - Run OpenAI prompt: "Extract tone, keywords, thematic traits…"  
5. **Persona Synthesis**  
   - Collect:  
     - `colors`: ["#C16639", "#708D81", …]  
     - `traits`: ["playful", "cozy", "vintage"]  
     - `voiceDescription`: free‑text summary  
     - `keywords`: words/themes from descriptions  
6. **Output & Save**  
   - Write to `personas` collection  
   - Return JSON response  

## Data Model (`personas` collection)  
```jsonc
{
  "_id": ObjectId,
  "pipelineId": ObjectId,
  "name": "Vintage Cozy",
  "colors": ["#C16639","#708D81","#F5A9B8"],
  "traits": ["playful","cozy","vintage"],
  "voiceDescription": "Warm, nostalgic, friendly tone",
  "keywords": ["home","retro","comfort"],
  "createdAt": ISODate,
  "updatedAt": ISODate
}
```

## API Endpoint  
- `POST /analyze/brand` → Accepts `{ boardId: string, assets?: [] }`, returns persona profile JSON.

## UI Considerations  
- Simple form: Dropbox for board URL + asset uploader  
- Progress indicator: "Fetching 120 pins… Analyzing colors…"  
- Result card: show palette swatches, trait tags, voice blurb  
- "Save to Pipeline" button  

## Implementation Notes
- Uses Pinterest API for data collection
- Requires ColorThief or similar library for color analysis
- Leverages OpenAI for text analysis and persona synthesis
- Stores results in MongoDB for future reference
- Links to a specific pipeline via `pipelineId`

## Integration Points
- Provides persona data to Content Generator for tone and style guidance
- Feeds visual identity elements to content formatting
- Referenced by Pipeline Manager via `personaId`
- May inform image generation in Content Generator
