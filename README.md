# ASST - Analysis and Content Generation Service

![CI Status](https://github.com/yourusername/asst/actions/workflows/ci.yml/badge.svg)

## Overview

ASST is a FastAPI-based service that provides brand analysis, competitor analysis, and content generation capabilities through a RESTful API.

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

## Development

Run tests:

```
pytest
```

Run linting:

```
flake8
```
