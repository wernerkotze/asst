#!/usr/bin/env python3
"""
ASST CLI - Command Line Interface for the ASST AI-Driven Social Media Automation Suite
"""

import argparse
import json
import sys
from typing import Dict

from cli.api import ApiClient
from cli.config import get_config_value

class AsstCli:
    """Main CLI class for ASST."""
    
    def __init__(self, api_url: str = None):
        """Initialize the CLI with API URL."""
        self.api_client = ApiClient(api_url=api_url)
    
    def _print_json(self, data: Dict, pretty: bool = True) -> None:
        """Print JSON data."""
        if pretty:
            print(json.dumps(data, indent=2))
        else:
            print(json.dumps(data))
    
    def list_pipelines(self, args: argparse.Namespace) -> None:
        """List all pipelines."""
        response = self.api_client.list_pipelines(pipeline_type=args.type, active_only=args.active_only)
        if args.output == "json":
            self._print_json(response)
        else:
            print("\nPipelines:")
            print("=" * 80)
            for pipeline in response:
                print(f"ID: {pipeline.get('id', 'N/A')}")
                print(f"Name: {pipeline.get('name', 'N/A')}")
                print(f"Type: {pipeline.get('type', 'N/A')}")
                print(f"Description: {pipeline.get('description', 'N/A')}")
                print("-" * 80)
    
    def create_pipeline(self, args: argparse.Namespace) -> None:
        """Create a new pipeline."""
        # Basic pipeline data
        pipeline_data = {
            "name": args.name,
            "type": args.type,
            "description": args.description,
            "persona": {
                "name": args.persona_name,
                "description": args.persona_description,
                "tone": args.persona_tone.split(","),
                "voice": args.persona_voice,
                "keywords": args.persona_keywords.split(",")
            },
            "content_framework": {
                "content_mix": {"news": 0.4, "meme": 0.3, "opinion": 0.3},
                "optimal_posting_times": [],
                "hashtag_strategy": args.hashtags.split(","),
                "engagement_tactics": []
            },
            "publishing_schedule": {
                "frequency": args.frequency,
                "times": args.times.split(","),
                "days": args.days.split(","),
                "timezone": args.timezone
            },
            "target_platforms": args.platforms.split(",")
        }
        
        response = self.api_client.create_pipeline(pipeline_data)
        print("\nPipeline created successfully!")
        self._print_json(response)
    
    def analyze_brand(self, args: argparse.Namespace) -> None:
        """Analyze a brand using Pinterest board."""
        request_data = {
            "boardId": args.board_id,
            "pipelineId": args.pipeline_id
        }
        
        response = self.api_client.analyze_brand(request_data)
        print("\nBrand analysis completed successfully!")
        self._print_json(response)
    
    def analyze_competitors(self, args: argparse.Namespace) -> None:
        """Analyze competitors using Twitter handles."""
        request_data = {
            "seedAccounts": args.accounts.split(","),
            "pipelineId": args.pipeline_id,
            "tweetLimit": args.limit
        }
        
        response = self.api_client.analyze_competitors(request_data)
        print("\nCompetitor analysis completed successfully!")
        self._print_json(response)
    
    def generate_content(self, args: argparse.Namespace) -> None:
        """Generate content using the wizard."""
        # Step 1: Retrieve content
        retrieve_data = {
            "pipelineId": args.pipeline_id,
            "sources": args.sources.split(","),
            "limit": args.limit
        }
        
        print("\nStep 1: Retrieving content...")
        raw_content = self.api_client.retrieve_content(retrieve_data)
        
        if not raw_content:
            print("No content retrieved.")
            return
        
        raw_content_ids = [item.get("id") for item in raw_content]
        print(f"Retrieved {len(raw_content_ids)} content items.")
        
        # Step 2: Enhance content
        enhance_data = {
            "rawContentIds": raw_content_ids,
            "pipelineId": args.pipeline_id
        }
        
        print("\nStep 2: Enhancing content...")
        enhanced_content = self.api_client.enhance_content(enhance_data)
        
        if not enhanced_content:
            print("No content enhanced.")
            return
        
        # Step 3: Personalize content (first item only for demo)
        personalize_data = {
            "enhancedContentId": enhanced_content[0].get("rawContentId"),
            "personaId": args.persona_id,
            "stylePreset": args.style
        }
        
        print("\nStep 3: Personalizing content...")
        personalized_content = self.api_client.personalize_content(personalize_data)
        
        # Step 4: Generate image
        image_data = {
            "text": personalized_content.get("personalizedText"),
            "method": "dalle"
        }
        
        print("\nStep 4: Generating image...")
        image_url = self.api_client.generate_image(image_data)
        
        # Step 5: Format content
        format_data = {
            "personalizedContentId": personalized_content.get("enhancedContentId"),
            "channel": args.platform,
            "mediaUrls": [image_url]
        }
        
        print("\nStep 5: Formatting content...")
        formatted_content = self.api_client.format_content(format_data)
        
        print("\nContent generation completed successfully!")
        print("\nFinal Content:")
        print("=" * 80)
        print(f"Text: {formatted_content.get('formattedText')}")
        print(f"Platform: {formatted_content.get('channel')}")
        print(f"Media: {', '.join(formatted_content.get('mediaUrls', []))}")
        print("=" * 80)
    
    def schedule_post(self, args: argparse.Namespace) -> None:
        """Schedule a post for publication."""
        request_data = {
            "contentId": args.content_id,
            "channel": args.platform,
            "scheduledTime": args.time
        }
        
        response = self.api_client.schedule_post(request_data)
        print("\nPost scheduled successfully!")
        self._print_json(response)
    
    def list_scheduled_posts(self, args: argparse.Namespace) -> None:
        """List all scheduled posts."""
        response = self.api_client.list_scheduled_posts(
            pipeline_id=args.pipeline_id,
            status=args.status
        )
        
        if args.output == "json":
            self._print_json(response)
        else:
            print("\nScheduled Posts:")
            print("=" * 80)
            for post in response:
                print(f"ID: {post.get('id', 'N/A')}")
                print(f"Content ID: {post.get('contentId', 'N/A')}")
                print(f"Platform: {post.get('channel', 'N/A')}")
                print(f"Scheduled Time: {post.get('scheduledTime', 'N/A')}")
                print(f"Status: {post.get('status', 'N/A')}")
                print("-" * 80)

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="ASST CLI - Command Line Interface for the ASST AI-Driven Social Media Automation Suite"
    )
    
    parser.add_argument("--api-url", help=f"API URL (default: {get_config_value('api_url')})")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format (default: text)")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Interactive mode command
    interactive_parser = subparsers.add_parser("interactive", help="Start interactive chatbot-style mode")
    
    # List pipelines command
    list_pipelines_parser = subparsers.add_parser("list-pipelines", help="List all pipelines")
    list_pipelines_parser.add_argument("--type", choices=["business", "ai_influencer", "automated_social"], help="Filter by pipeline type")
    list_pipelines_parser.add_argument("--active-only", action="store_true", default=True, help="Only show active pipelines")
    
    # Create pipeline command
    create_pipeline_parser = subparsers.add_parser("create-pipeline", help="Create a new pipeline")
    create_pipeline_parser.add_argument("--name", required=True, help="Pipeline name")
    create_pipeline_parser.add_argument("--type", required=True, choices=["business", "ai_influencer", "automated_social"], help="Pipeline type")
    create_pipeline_parser.add_argument("--description", required=True, help="Pipeline description")
    create_pipeline_parser.add_argument("--persona-name", required=True, help="Persona name")
    create_pipeline_parser.add_argument("--persona-description", required=True, help="Persona description")
    create_pipeline_parser.add_argument("--persona-tone", default="casual,friendly", help="Persona tone (comma-separated)")
    create_pipeline_parser.add_argument("--persona-voice", default="casual", help="Persona voice")
    create_pipeline_parser.add_argument("--persona-keywords", default="", help="Persona keywords (comma-separated)")
    create_pipeline_parser.add_argument("--hashtags", default="", help="Hashtag strategy (comma-separated)")
    create_pipeline_parser.add_argument("--frequency", default="daily", help="Posting frequency")
    create_pipeline_parser.add_argument("--times", default="09:00,12:00,17:00", help="Posting times (comma-separated)")
    create_pipeline_parser.add_argument("--days", default="monday,wednesday,friday", help="Posting days (comma-separated)")
    create_pipeline_parser.add_argument("--timezone", default="UTC", help="Timezone")
    create_pipeline_parser.add_argument("--platforms", default="twitter", help="Target platforms (comma-separated)")
    
    # Analyze brand command
    analyze_brand_parser = subparsers.add_parser("analyze-brand", help="Analyze a brand using Pinterest board")
    analyze_brand_parser.add_argument("--board-id", required=True, help="Pinterest board ID or URL")
    analyze_brand_parser.add_argument("--pipeline-id", help="Pipeline ID to associate with the persona")
    
    # Analyze competitors command
    analyze_competitors_parser = subparsers.add_parser("analyze-competitors", help="Analyze competitors using Twitter handles")
    analyze_competitors_parser.add_argument("--accounts", required=True, help="Twitter handles (comma-separated)")
    analyze_competitors_parser.add_argument("--pipeline-id", help="Pipeline ID to associate with the framework")
    analyze_competitors_parser.add_argument("--limit", type=int, default=200, help="Maximum number of tweets to analyze per account")
    
    # Generate content command
    generate_content_parser = subparsers.add_parser("generate-content", help="Generate content using the wizard")
    generate_content_parser.add_argument("--pipeline-id", required=True, help="Pipeline ID")
    generate_content_parser.add_argument("--sources", default="news,twitter", help="Content sources (comma-separated)")
    generate_content_parser.add_argument("--limit", type=int, default=10, help="Maximum number of items to retrieve")
    generate_content_parser.add_argument("--persona-id", required=True, help="Persona ID for personalization")
    generate_content_parser.add_argument("--style", default="witty", help="Style preset for personalization")
    generate_content_parser.add_argument("--platform", default="twitter", help="Platform to format for")
    
    # Schedule post command
    schedule_post_parser = subparsers.add_parser("schedule-post", help="Schedule a post for publication")
    schedule_post_parser.add_argument("--content-id", required=True, help="Content ID to schedule")
    schedule_post_parser.add_argument("--platform", required=True, help="Platform to publish to")
    schedule_post_parser.add_argument("--time", required=True, help="When to publish (ISO format)")
    
    # List scheduled posts command
    list_scheduled_posts_parser = subparsers.add_parser("list-scheduled-posts", help="List all scheduled posts")
    list_scheduled_posts_parser.add_argument("--pipeline-id", help="Filter by pipeline ID")
    list_scheduled_posts_parser.add_argument("--status", choices=["scheduled", "published", "failed"], help="Filter by status")
    
    args = parser.parse_args()
    
    # Run interactive mode if requested
    if args.command == "interactive":
        from cli.interactive_mode import InteractiveSession
        session = InteractiveSession(ApiClient(api_url=args.api_url))
        session.start()
        return
    
    # Initialize CLI
    cli = AsstCli(api_url=args.api_url)
    
    # Run command
    if args.command == "list-pipelines":
        cli.list_pipelines(args)
    elif args.command == "create-pipeline":
        cli.create_pipeline(args)
    elif args.command == "analyze-brand":
        cli.analyze_brand(args)
    elif args.command == "analyze-competitors":
        cli.analyze_competitors(args)
    elif args.command == "generate-content":
        cli.generate_content(args)
    elif args.command == "schedule-post":
        cli.schedule_post(args)
    elif args.command == "list-scheduled-posts":
        cli.list_scheduled_posts(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
