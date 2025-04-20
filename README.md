# ASST
**AI‑Driven Social Media Automation Suite**

![CI Status](https://github.com/yourusername/asst/actions/workflows/ci.yml/badge.svg)

## Vision

Enable brands, influencers, and creators to go from inspiration to published social content in minutes—powered by data, AI, and a unified, modular workflow.

## What is ASST?

ASST (pronounced "assist") is a serverless, API‑first platform that:

- **Analyzes** brand identity and competitor strategies  
- **Synthesizes** a custom persona, voice, and visual palette  
- **Generates** on‑brand, data‑backed posts via AI  
- **Schedules** and **publishes** automatically to your social channels  
- **Monitors** performance and **feeds back** actionable insights  

## Setup

### Prerequisites

- Python 3.10+
- Docker (optional)

### Environment Variables

Create a `.env` file with the following variables:

```
# API Configuration
API_KEY=your_api_key

# Database Configuration
DB_HOST=localhost
DB_PORT=27017
DB_NAME=asst

# AWS Configuration (if using DynamoDB)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-west-2
```

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/asst.git
   cd asst
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running Locally

Start the server with:

```
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running with Docker

Build and run the Docker container:

```
docker build -t asst .
docker run -p 8000:8000 --env-file .env asst
```

## API Endpoints

- `/analyze/brand` - Brand analysis
- `/analyze/competitors` - Competitor analysis
- `/generate/content` - Content generation

## Core Modules

### 1. Pipeline Manager
Defines *what* you're automating—  
- **Business** (new or existing)  
- **AI Influencer** (fan account, personal brand, niche expert)  
- **Automated Social** (news feed, meme channel, publication)

Each pipeline ties together a persona, content framework, data sources, and publishing schedule.

### 2. Brand Generation Tool
Extracts your visual and verbal identity from:  
- **Pinterest boards** (colors, themes, imagery)  
- **Brand assets** (logos, style guides)  
- **OpenAI analysis** (tone, personality traits)  

Outputs a reusable **Persona Profile** (color palette, keywords, voice).

### 3. Competitor Analysis Tool
Studies up to 5 seed accounts on Twitter (or other channels) to derive:  
- **Content mix** (news, commentary, memes, etc.)  
- **Posting cadence** (frequency, optimal times)  
- **Engagement tactics** (hashtags, polls, CTAs)  
- **Writing‑style presets** (tone, formality, emoji usage)

Generates a strategic **Content Framework**.

### 4. Content Generator Wizard
A 7‑step, AI‑powered workflow that:  
1. Selects your pipeline  
2. Pulls source content (news, stats, social, etc.)  
3. Enhances with tags, sentiment, media  
4. Personalizes tone + emojis  
5. Generates or selects images  
6. Formats per platform (Twitter, LinkedIn, etc.)  
7. Previews, queues or publishes  

### 5. Scheduling & CMS
- **Airtable**–backed draft/review queue and calendar  
- **Automated posting** via Twitter API (and other channels later)  
- **Serverless scheduling** (Lambda + EventBridge)

### 6. Monitoring & Feedback
- **Engagement metrics** (likes, shares, comments) fetched automatically  
- **Performance dashboards** highlight top content types, times, and tone  
- **Continuous optimization** loops back into the Pipeline

## Tech Stack (Lean & Serverless)
- **API**: FastAPI + AWS Lambda / API Gateway  
- **Data Storage**: DynamoDB (on‑demand) + S3 for media  
- **CMS**: Airtable  
- **AI & Integrations**:  
  - OpenAI (text generation & analysis)  
  - Twitter API / twscrape  
  - Pinterest API  
  - NewsAPI, Football‑Data API  
  - Google Images API  

## Example Use Cases

- **Chelsea FC AI Influencer**  
  - Real‑time match updates + fan banter  
  - Live stats integration + witty commentary  
- **Day‑Trading Persona**  
  - Market news + ticker sentiment  
  - Scheduled morning recaps and midday insights  
- **Lifestyle Brand Launch**  
  - Pinterest‑derived color scheme + tone  
  - Competitor‑inspired content cadence  

## Roadmap

- **v1.0**: Core modules + Twitter support  
- **v1.1**: Logo generation, Instagram & LinkedIn channels  
- **v2.0**: Video/audio content automation, team collaboration features  

## Development

Run tests:

```
pytest
```

Run linting:

```
flake8
```

---

ASST brings together art and data—helping you craft the *right* message at the *right* time, every time.
