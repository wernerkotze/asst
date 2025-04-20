# Pipeline Manager

## Purpose  
Holds the user's overall automation "recipe." Defines **what** kind of social presence to build (business, AI influencer, automated social feed) and wires together persona, framework, sources, and schedule.

## Key Responsibilities  
- Create / Read / Update / Delete pipelines  
- Assign pipeline **type**:  
  - `business` (new or existing brand)  
  - `ai_influencer` (fan account, day trader, personal brand)  
  - `automated_social` (news aggregator, meme account)  
- Link to optional `personaId` and `competitorAnalysisId`  
- Store high‑level settings: `name`, `category`, `subcategory`, `keywords`, `targetChannels`

## Data Model (MongoDB `pipelines` collection)  
```jsonc
{
  "_id": ObjectId,
  "userId": ObjectId,                // owner
  "name": "Chelsea Fan Bot",
  "type": "ai_influencer",
  "category": "Sports",
  "subcategory": "Chelsea FC",
  "keywords": ["Chelsea", "Premier League"],
  "personaId": ObjectId,             // optional
  "competitorAnalysisId": ObjectId,  // optional
  "targetChannels": ["twitter"],
  "createdAt": ISODate,
  "updatedAt": ISODate
}
```

## API Endpoints  
- `POST /pipelines/` → Create  
- `GET /pipelines/{id}` → Read  
- `PATCH /pipelines/{id}` → Update  
- `DELETE /pipelines/{id}` → Delete  
- `GET /pipelines/` → List by user  

## UI Considerations  
- Pipeline list page: show `name`, `type`, linked modules (persona, competitor).  
- Pipeline editor: dropdown for `type`, tag‑input for `keywords`, toggles for `targetChannels`.  
- Button: "Run Persona Analysis" / "Run Competitor Analysis" when links empty.

## Implementation Notes
- The pipeline is the central entity that connects all other components
- Each pipeline has a unique ID that is referenced by other components
- The pipeline type determines the workflow and available options
- The pipeline is owned by a user and can be shared with other users
- The pipeline can be activated or deactivated

## Integration Points
- Integrates with Persona module via `personaId`
- Integrates with Competitor Analysis module via `competitorAnalysisId`
- Provides pipeline context to Content Generator
- Feeds configuration to Scheduling & CMS
