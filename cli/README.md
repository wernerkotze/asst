# ASST CLI

Command Line Interface for the ASST AI-Driven Social Media Automation Suite.

## Installation

```bash
# Install the CLI tool
cd /Users/werner/www/asst
pip install -e cli/
```

## Usage

The ASST CLI provides a command-line interface to interact with the ASST API. It allows you to manage pipelines, analyze brands and competitors, generate content, and schedule posts.

### Global Options

- `--api-url`: API URL (default: http://localhost:8000)
- `--output`: Output format (text or json, default: text)

### Commands

#### List Pipelines

```bash
asst list-pipelines
```

#### Create Pipeline

```bash
asst create-pipeline \
  --name "Chelsea FC Fan Account" \
  --type ai_influencer \
  --description "AI-powered Chelsea FC fan account posting match updates and fan banter" \
  --persona-name "BluesFanAI" \
  --persona-description "Passionate Chelsea FC supporter with deep knowledge of the club's history" \
  --persona-tone "enthusiastic,witty,knowledgeable" \
  --persona-voice "casual" \
  --persona-keywords "Chelsea,Blues,Stamford Bridge,Premier League" \
  --hashtags "#CFC,#Chelsea,#KTBFFH" \
  --frequency "daily" \
  --times "08:00,12:00,18:00" \
  --days "monday,tuesday,wednesday,thursday,friday,saturday,sunday" \
  --timezone "Europe/London" \
  --platforms "twitter,instagram"
```

#### Analyze Brand

```bash
asst analyze-brand \
  --board-id "username/chelsea-brand-board" \
  --pipeline-id "pipeline_12345"
```

#### Analyze Competitors

```bash
asst analyze-competitors \
  --accounts "ChelseaFC,talkchelsea" \
  --pipeline-id "pipeline_12345" \
  --limit 200
```

#### Generate Content

```bash
asst generate-content \
  --pipeline-id "pipeline_12345" \
  --sources "news,twitter,sports" \
  --limit 10 \
  --persona-id "persona_67890" \
  --style "witty" \
  --platform "twitter"
```

#### Schedule Post

```bash
asst schedule-post \
  --content-id "content_12345" \
  --platform "twitter" \
  --time "2025-04-21T09:00:00Z"
```

#### List Scheduled Posts

```bash
asst list-scheduled-posts \
  --pipeline-id "pipeline_12345" \
  --status "scheduled"
```

## Examples

### Create a Pipeline and Generate Content

```bash
# Create a pipeline
pipeline_id=$(asst create-pipeline \
  --name "Chelsea FC Fan Account" \
  --type ai_influencer \
  --description "AI-powered Chelsea FC fan account" \
  --persona-name "BluesFanAI" \
  --persona-description "Passionate Chelsea FC supporter" \
  --output json | jq -r '.id')

# Analyze competitors
asst analyze-competitors \
  --accounts "ChelseaFC,talkchelsea" \
  --pipeline-id "$pipeline_id"

# Get persona ID
persona_id=$(asst list-pipelines --output json | \
  jq -r ".[] | select(.id == \"$pipeline_id\") | .persona.id")

# Generate content
asst generate-content \
  --pipeline-id "$pipeline_id" \
  --persona-id "$persona_id" \
  --style "witty" \
  --platform "twitter"
```

## Environment Variables

- `ASST_API_URL`: API URL (default: http://localhost:8000)

## Development

### Running Tests

```bash
cd /Users/werner/www/asst/cli
pytest
```

### Building the Package

```bash
cd /Users/werner/www/asst/cli
python setup.py sdist bdist_wheel
```
