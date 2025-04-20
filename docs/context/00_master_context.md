# ASST – Master Context Reference

This document provides an overview of the ASST platform architecture and how the different modules interact with each other. It serves as an entry point to the more detailed context files for each module.

## System Overview

ASST is an AI-Driven Social Media Automation Suite designed to help brands, influencers, and creators generate and publish social media content efficiently using AI and data-driven insights.

The platform consists of six core modules that work together to create a complete content automation pipeline:

1. **Pipeline Manager** - Central configuration hub that defines the overall automation strategy
2. **Brand Generation Tool** - Creates persona profiles from visual and textual inputs
3. **Competitor Analysis Tool** - Builds content frameworks by analyzing successful accounts
4. **Content Generator Wizard** - Transforms raw content into personalized, platform-ready posts
5. **Scheduling & CMS** - Manages content publication across multiple platforms
6. **Monitoring & Feedback** - Tracks performance and provides optimization insights

## Data Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Pipeline       │────▶│  Brand          │────▶│  Competitor     │
│  Manager        │     │  Generation     │     │  Analysis       │
│                 │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │                       ▼                       ▼
         │              ┌─────────────────────────────────────────┐
         └─────────────▶│                                         │
                        │  Content Generator Wizard               │
                        │                                         │
                        └────────────────────┬────────────────────┘
                                             │
                                             ▼
                        ┌─────────────────────────────────────────┐
                        │                                         │
                        │  Scheduling & CMS                       │
                        │                                         │
                        └────────────────────┬────────────────────┘
                                             │
                                             ▼
                        ┌─────────────────────────────────────────┐
                        │                                         │
                        │  Monitoring & Feedback                  │
                        │                                         │
                        └─────────────────────────────────────────┘
```

## Key Data Models

The system uses the following primary collections in MongoDB:

1. **pipelines** - Central configuration for content automation
2. **personas** - Brand identity and voice profiles
3. **competitor_analyses** - Content frameworks derived from competitor analysis
4. **content_pieces** - Content at various stages of the generation process
5. **scheduled_posts** - Posts scheduled for publication
6. **engagement_metrics** - Performance data for published content

## Technology Stack

- **Backend**: FastAPI with Python 3.10+
- **Database**: MongoDB / DynamoDB for document storage, Redis for caching
- **Cloud Infrastructure**: AWS Lambda, EventBridge, S3
- **AI Services**: OpenAI for content generation and analysis
- **External APIs**: Twitter, Pinterest, NewsAPI, etc.
- **Monitoring**: CloudWatch for system monitoring, custom analytics for content performance

## Integration Architecture

The ASST platform is designed with a modular, serverless architecture that allows for:

1. **Horizontal Scaling** - Each module can scale independently based on demand
2. **Service Isolation** - Modules communicate via well-defined APIs
3. **Extensibility** - New platforms and content types can be added with minimal changes
4. **Resilience** - Failure in one module doesn't affect the entire system

## Security Considerations

- API keys and credentials are stored securely in environment variables
- User authentication and authorization is implemented at the API level
- Content validation ensures no harmful or inappropriate content is published
- Rate limiting prevents abuse of external APIs

## Detailed Module Documentation

For detailed information about each module, refer to the following context files:

1. [Pipeline Manager](./01_pipeline_manager.md)
2. [Brand Generation Tool](./02_brand_generation_tool.md)
3. [Competitor Analysis Tool](./03_competitor_analysis_tool.md)
4. [Content Generator Wizard](./04_content_generator_wizard.md)
5. [Scheduling & CMS](./05_scheduling_cms.md)
6. [Monitoring & Feedback](./06_monitoring_feedback.md)

## Development Roadmap

- **v1.0**: Core modules + Twitter support
- **v1.1**: Logo generation, Instagram & LinkedIn channels
- **v2.0**: Video/audio content automation, team collaboration features

This context file serves as the authoritative reference for the system architecture and module integration. Update it as the system evolves.
