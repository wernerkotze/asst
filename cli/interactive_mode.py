"""
Interactive chatbot-style interface for the ASST CLI.
"""

import os
import sys
import json
import time
from typing import Dict, List, Any, Optional, Callable

from cli.api import ApiClient
from cli.config import get_config_value

class InteractiveSession:
    """Interactive session for guiding users through the ASST system."""
    
    def __init__(self, api_client: ApiClient = None):
        """Initialize the interactive session."""
        self.api_client = api_client or ApiClient()
        self.context = {}  # Stores session context (pipeline_id, etc.)
        self.history = []  # Conversation history
    
    def start(self):
        """Start the interactive session."""
        self._clear_screen()
        self._print_welcome()
        
        # Main interaction loop
        while True:
            choice = self._main_menu()
            
            if choice == "1":
                self._pipeline_workflow()
            elif choice == "2":
                self._brand_analysis_workflow()
            elif choice == "3":
                self._competitor_analysis_workflow()
            elif choice == "4":
                self._content_generation_workflow()
            elif choice == "5":
                self._scheduling_workflow()
            elif choice == "6":
                self._view_context()
            elif choice == "q":
                self._print_goodbye()
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def _clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _print_welcome(self):
        """Print welcome message."""
        print("\n" + "=" * 80)
        print("🤖 Welcome to ASST Interactive Mode!")
        print("=" * 80)
        print("\nI'll guide you through the ASST AI-Driven Social Media Automation Suite.")
        print("Let's create amazing social media content together!\n")
    
    def _print_goodbye(self):
        """Print goodbye message."""
        print("\n" + "=" * 80)
        print("👋 Thank you for using ASST Interactive Mode!")
        print("=" * 80)
        print("\nYour session context has been saved. See you next time!\n")
    
    def _main_menu(self) -> str:
        """Display main menu and get user choice."""
        print("\n" + "-" * 50)
        print("📋 MAIN MENU")
        print("-" * 50)
        print("1. Pipeline Management")
        print("2. Brand Analysis")
        print("3. Competitor Analysis")
        print("4. Content Generation")
        print("5. Scheduling")
        print("6. View Current Context")
        print("q. Quit")
        
        return input("\n👉 What would you like to do? ").strip().lower()
    
    def _input(self, prompt: str, default: str = None) -> str:
        """Get user input with optional default value."""
        if default:
            result = input(f"{prompt} [{default}]: ").strip()
            return result if result else default
        return input(f"{prompt}: ").strip()
    
    def _confirm(self, prompt: str) -> bool:
        """Get user confirmation."""
        response = input(f"{prompt} (y/n): ").strip().lower()
        return response == "y" or response == "yes"
    
    def _select_from_list(self, items: List[Dict], prompt: str, display_func: Callable = None) -> Optional[Dict]:
        """Let user select an item from a list."""
        if not items:
            print("\n❌ No items available.")
            return None
        
        print(f"\n{prompt}:")
        for i, item in enumerate(items, 1):
            if display_func:
                display_func(i, item)
            else:
                print(f"{i}. {item.get('name', 'Unknown')}")
        
        try:
            choice = int(input("\n👉 Enter number (0 to cancel): "))
            if choice == 0:
                return None
            return items[choice - 1]
        except (ValueError, IndexError):
            print("\n❌ Invalid selection.")
            return None
    
    def _view_context(self):
        """View current session context."""
        print("\n" + "-" * 50)
        print("🔍 CURRENT CONTEXT")
        print("-" * 50)
        
        if not self.context:
            print("\nNo context variables set yet.")
            return
        
        for key, value in self.context.items():
            print(f"{key}: {value}")
        
        input("\nPress Enter to continue...")
    
    def _pipeline_workflow(self):
        """Pipeline management workflow."""
        while True:
            print("\n" + "-" * 50)
            print("🔄 PIPELINE MANAGEMENT")
            print("-" * 50)
            print("1. List Pipelines")
            print("2. Create New Pipeline")
            print("3. Set Active Pipeline")
            print("b. Back to Main Menu")
            
            choice = input("\n👉 Choose an option: ").strip().lower()
            
            if choice == "1":
                self._list_pipelines()
            elif choice == "2":
                self._create_pipeline()
            elif choice == "3":
                self._set_active_pipeline()
            elif choice == "b":
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def _list_pipelines(self):
        """List all pipelines."""
        print("\n📋 Fetching pipelines...")
        
        try:
            pipelines = self.api_client.list_pipelines()
            
            if not pipelines:
                print("\n❌ No pipelines found.")
                return
            
            print("\n" + "-" * 80)
            print(f"{'ID':<15} {'NAME':<30} {'TYPE':<15} {'STATUS'}")
            print("-" * 80)
            
            for pipeline in pipelines:
                print(f"{pipeline.get('id', 'N/A'):<15} {pipeline.get('name', 'Unknown'):<30} {pipeline.get('type', 'Unknown'):<15} {'Active' if pipeline.get('active', False) else 'Inactive'}")
            
            print("-" * 80)
        except Exception as e:
            print(f"\n❌ Error fetching pipelines: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _create_pipeline(self):
        """Create a new pipeline."""
        print("\n🔄 Let's create a new pipeline!")
        
        try:
            # Basic pipeline info
            name = self._input("Enter pipeline name")
            if not name:
                print("\n❌ Pipeline name is required.")
                return
            
            pipeline_type = self._input("Enter pipeline type (business, ai_influencer, automated_social)", "ai_influencer")
            description = self._input("Enter pipeline description", "AI-powered social media content pipeline")
            
            # Persona info
            print("\n👤 Now let's define the persona for this pipeline:")
            persona_name = self._input("Enter persona name", name + " Persona")
            persona_description = self._input("Enter persona description", "Social media persona with a unique voice")
            persona_tone = self._input("Enter persona tone (comma-separated)", "friendly,casual,informative")
            persona_voice = self._input("Enter persona voice", "casual")
            persona_keywords = self._input("Enter persona keywords (comma-separated)", "social media,content,automation")
            
            # Content framework
            print("\n📝 Now let's define the content framework:")
            hashtags = self._input("Enter hashtags (comma-separated)", "#asst,#socialmedia,#automation")
            
            # Publishing schedule
            print("\n📅 Now let's define the publishing schedule:")
            frequency = self._input("Enter frequency (hourly, daily, weekly)", "daily")
            times = self._input("Enter publishing times (comma-separated)", "09:00,15:00,19:00")
            days = self._input("Enter publishing days (comma-separated)", "monday,wednesday,friday")
            timezone = self._input("Enter timezone", "UTC")
            
            # Target platforms
            platforms = self._input("Enter target platforms (comma-separated)", "twitter,instagram")
            
            # Confirm creation
            print("\n✅ Pipeline details:")
            print(f"Name: {name}")
            print(f"Type: {pipeline_type}")
            print(f"Persona: {persona_name}")
            print(f"Platforms: {platforms}")
            
            if not self._confirm("\nCreate this pipeline?"):
                print("\n❌ Pipeline creation cancelled.")
                return
            
            # Create pipeline
            pipeline_data = {
                "name": name,
                "type": pipeline_type,
                "description": description,
                "persona": {
                    "name": persona_name,
                    "description": persona_description,
                    "tone": persona_tone.split(","),
                    "voice": persona_voice,
                    "keywords": persona_keywords.split(",")
                },
                "content_framework": {
                    "content_mix": {"news": 0.4, "meme": 0.3, "opinion": 0.3},
                    "optimal_posting_times": [],
                    "hashtag_strategy": hashtags.split(","),
                    "engagement_tactics": []
                },
                "publishing_schedule": {
                    "frequency": frequency,
                    "times": times.split(","),
                    "days": days.split(","),
                    "timezone": timezone
                },
                "target_platforms": platforms.split(",")
            }
            
            print("\n🔄 Creating pipeline...")
            response = self.api_client.create_pipeline(pipeline_data)
            
            print(f"\n✅ Pipeline created successfully! ID: {response.get('id')}")
            
            # Set as active pipeline
            if self._confirm("Set this as your active pipeline?"):
                self.context["pipeline_id"] = response.get("id")
                self.context["pipeline_name"] = name
                print(f"\n✅ Active pipeline set to: {name}")
        
        except Exception as e:
            print(f"\n❌ Error creating pipeline: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _set_active_pipeline(self):
        """Set the active pipeline for the session."""
        print("\n🔄 Fetching pipelines...")
        
        try:
            pipelines = self.api_client.list_pipelines()
            
            if not pipelines:
                print("\n❌ No pipelines found.")
                return
            
            selected = self._select_from_list(
                pipelines, 
                "Select a pipeline to set as active",
                lambda i, p: print(f"{i}. {p.get('name', 'Unknown')} ({p.get('id', 'N/A')})")
            )
            
            if selected:
                self.context["pipeline_id"] = selected.get("id")
                self.context["pipeline_name"] = selected.get("name")
                print(f"\n✅ Active pipeline set to: {selected.get('name')}")
            
        except Exception as e:
            print(f"\n❌ Error setting active pipeline: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _brand_analysis_workflow(self):
        """Brand analysis workflow."""
        if not self._check_active_pipeline():
            return
            
        print("\n" + "-" * 50)
        print("🎨 BRAND ANALYSIS")
        print("-" * 50)
        print(f"Active Pipeline: {self.context.get('pipeline_name')}")
        
        # Get Pinterest board ID
        board_id = self._input("Enter Pinterest board ID (username/board-name)")
        if not board_id:
            print("\n❌ Pinterest board ID is required.")
            return
            
        # Get brand name
        brand_name = self._input("Enter brand name")
        if not brand_name:
            print("\n❌ Brand name is required.")
            return
            
        # Get industry
        industry = self._input("Enter industry")
        if not industry:
            print("\n❌ Industry is required.")
            return
        
        # Confirm analysis
        if not self._confirm(f"\nAnalyze Pinterest board '{board_id}' for pipeline '{self.context.get('pipeline_name')}'?"):
            print("\n❌ Brand analysis cancelled.")
            return
        
        # Perform analysis
        try:
            print("\n🔄 Analyzing Pinterest board...")
            request_data = {
                "pinterest_board": board_id,
                "pipelineId": self.context.get("pipeline_id"),
                "brand_name": brand_name,
                "industry": industry
            }
            
            response = self.api_client.analyze_brand(request_data)
            
            # Display results
            print("\n✅ Brand analysis completed successfully!")
            print("\n📊 Analysis Results:")
            print(f"Persona Name: {response.get('persona', {}).get('name', 'N/A')}")
            print(f"Color Palette: {', '.join(response.get('visualIdentity', {}).get('colorPalette', ['N/A']))}")
            print(f"Visual Style: {response.get('visualIdentity', {}).get('style', 'N/A')}")
            print(f"Tone: {', '.join(response.get('persona', {}).get('tone', ['N/A']))}")
            
            # Save persona ID to context
            if 'persona' in response and 'id' in response['persona']:
                self.context['persona_id'] = response['persona']['id']
                print(f"\n✅ Persona ID saved to context: {response['persona']['id']}")
        
        except Exception as e:
            print(f"\n❌ Error analyzing brand: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _competitor_analysis_workflow(self):
        """Competitor analysis workflow."""
        if not self._check_active_pipeline():
            return
            
        print("\n" + "-" * 50)
        print("🔍 COMPETITOR ANALYSIS")
        print("-" * 50)
        print(f"Active Pipeline: {self.context.get('pipeline_name')}")
        
        # Get Twitter accounts
        accounts = self._input("Enter Twitter accounts to analyze (comma-separated)")
        if not accounts:
            print("\n❌ Twitter accounts are required.")
            return
        
        # Get tweet limit
        try:
            limit = int(self._input("Enter tweet limit per account", "100"))
        except ValueError:
            print("\n❌ Invalid tweet limit. Using default of 100.")
            limit = 100
        
        # Confirm analysis
        if not self._confirm(f"\nAnalyze Twitter accounts '{accounts}' for pipeline '{self.context.get('pipeline_name')}'?"):
            print("\n❌ Competitor analysis cancelled.")
            return
        
        # Perform analysis
        try:
            print("\n🔄 Analyzing Twitter accounts...")
            request_data = {
                "seedAccounts": accounts.split(","),
                "pipelineId": self.context.get("pipeline_id"),
                "tweetLimit": limit
            }
            
            response = self.api_client.analyze_competitors(request_data)
            
            # Display results
            print("\n✅ Competitor analysis completed successfully!")
            print("\n📊 Analysis Results:")
            print(f"Framework ID: {response.get('frameworkId', 'N/A')}")
            print(f"Total Tweets Analyzed: {response.get('totalTweetsAnalyzed', 0)}")
            print(f"Top Categories: {', '.join(response.get('topCategories', ['N/A']))}")
            print(f"Optimal Posting Times: {', '.join(response.get('optimalPostingTimes', ['N/A']))}")
            
            # Save framework ID to context
            if 'frameworkId' in response:
                self.context['framework_id'] = response['frameworkId']
                print(f"\n✅ Framework ID saved to context: {response['frameworkId']}")
        
        except Exception as e:
            print(f"\n❌ Error analyzing competitors: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _content_generation_workflow(self):
        """Content generation workflow."""
        if not self._check_active_pipeline():
            return
            
        print("\n" + "-" * 50)
        print("✍️ CONTENT GENERATION")
        print("-" * 50)
        print(f"Active Pipeline: {self.context.get('pipeline_name')}")
        
        # Check for persona ID
        persona_id = self.context.get('persona_id')
        if not persona_id:
            print("\n⚠️ No persona ID in context. You may want to run brand analysis first.")
            persona_id = self._input("Enter persona ID (or leave blank to use default)")
        
        # Get content sources
        sources = self._input("Enter content sources (comma-separated)", "news,twitter,sports")
        
        # Get content limit
        try:
            limit = int(self._input("Enter content item limit", "5"))
        except ValueError:
            print("\n❌ Invalid limit. Using default of 5.")
            limit = 5
        
        # Get style preset
        style = self._input("Enter style preset", "witty")
        
        # Get target platform
        platform = self._input("Enter target platform", "twitter")
        
        # Confirm generation
        if not self._confirm(f"\nGenerate content for pipeline '{self.context.get('pipeline_name')}'?"):
            print("\n❌ Content generation cancelled.")
            return
        
        # Generate content
        try:
            # Step 1: Retrieve content
            print("\n🔄 Step 1/5: Retrieving content...")
            retrieve_data = {
                "pipelineId": self.context.get("pipeline_id"),
                "sources": sources.split(","),
                "limit": limit
            }
            
            raw_content = self.api_client.retrieve_content(retrieve_data)
            
            if not raw_content:
                print("\n❌ No content retrieved.")
                return
            
            print(f"\n✅ Retrieved {len(raw_content)} content items.")
            
            # Get content IDs
            raw_content_ids = [item.get("id") for item in raw_content if "id" in item]
            
            # Step 2: Enhance content
            print("\n🔄 Step 2/5: Enhancing content...")
            enhance_data = {
                "rawContentIds": raw_content_ids,
                "pipelineId": self.context.get("pipeline_id")
            }
            
            enhanced_content = self.api_client.enhance_content(enhance_data)
            
            if not enhanced_content:
                print("\n❌ No content enhanced.")
                return
            
            print(f"\n✅ Enhanced {len(enhanced_content)} content items.")
            
            # Step 3: Personalize content (first item only for demo)
            print("\n🔄 Step 3/5: Personalizing content...")
            personalize_data = {
                "enhancedContentId": enhanced_content[0].get("rawContentId"),
                "personaId": persona_id,
                "stylePreset": style
            }
            
            personalized_content = self.api_client.personalize_content(personalize_data)
            print("\n✅ Content personalized successfully.")
            
            # Step 4: Generate image
            print("\n🔄 Step 4/5: Generating image...")
            image_data = {
                "text": personalized_content.get("personalizedText"),
                "method": "dalle"
            }
            
            image_url = self.api_client.generate_image(image_data)
            print(f"\n✅ Image generated: {image_url}")
            
            # Step 5: Format content
            print("\n🔄 Step 5/5: Formatting content...")
            format_data = {
                "personalizedContentId": personalized_content.get("enhancedContentId"),
                "channel": platform,
                "mediaUrls": [image_url]
            }
            
            formatted_content = self.api_client.format_content(format_data)
            
            # Display results
            print("\n✅ Content generation completed successfully!")
            print("\n📝 Final Content:")
            print(f"Text: {formatted_content.get('text', 'N/A')}")
            print(f"Media: {', '.join(formatted_content.get('mediaUrls', ['N/A']))}")
            print(f"Hashtags: {', '.join(formatted_content.get('hashtags', ['N/A']))}")
            
            # Save content ID to context
            if 'id' in formatted_content:
                self.context['content_id'] = formatted_content['id']
                print(f"\n✅ Content ID saved to context: {formatted_content['id']}")
        
        except Exception as e:
            print(f"\n❌ Error generating content: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _scheduling_workflow(self):
        """Scheduling workflow."""
        if not self._check_active_pipeline():
            return
            
        print("\n" + "-" * 50)
        print("📅 CONTENT SCHEDULING")
        print("-" * 50)
        print(f"Active Pipeline: {self.context.get('pipeline_name')}")
        
        # Scheduling options
        print("\n1. Schedule New Post")
        print("2. List Scheduled Posts")
        print("b. Back to Main Menu")
        
        choice = input("\n👉 Choose an option: ").strip().lower()
        
        if choice == "1":
            self._schedule_post()
        elif choice == "2":
            self._list_scheduled_posts()
        elif choice == "b":
            return
        else:
            print("\n❌ Invalid choice. Please try again.")
    
    def _schedule_post(self):
        """Schedule a post for publication."""
        # Check for content ID
        content_id = self.context.get('content_id')
        if not content_id:
            print("\n⚠️ No content ID in context. You may want to generate content first.")
            content_id = self._input("Enter content ID")
            if not content_id:
                print("\n❌ Content ID is required.")
                return
        
        # Get platform
        platform = self._input("Enter target platform", "twitter")
        
        # Get scheduled time
        scheduled_time = self._input("Enter scheduled time (YYYY-MM-DDThh:mm:ssZ)", 
                                  time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 3600)))
        
        # Confirm scheduling
        if not self._confirm(f"\nSchedule content '{content_id}' for {scheduled_time} on {platform}?"):
            print("\n❌ Post scheduling cancelled.")
            return
        
        # Schedule post
        try:
            print("\n🔄 Scheduling post...")
            request_data = {
                "contentId": content_id,
                "channel": platform,
                "scheduledTime": scheduled_time
            }
            
            response = self.api_client.schedule_post(request_data)
            
            # Display results
            print("\n✅ Post scheduled successfully!")
            print(f"Scheduled Post ID: {response.get('id', 'N/A')}")
            print(f"Status: {response.get('status', 'N/A')}")
            print(f"Scheduled Time: {response.get('scheduledTime', 'N/A')}")
        
        except Exception as e:
            print(f"\n❌ Error scheduling post: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _list_scheduled_posts(self):
        """List all scheduled posts."""
        # Get status filter
        status = self._input("Enter status filter (scheduled, published, failed) or leave blank for all")
        
        # List posts
        try:
            print("\n🔄 Fetching scheduled posts...")
            response = self.api_client.list_scheduled_posts(
                pipeline_id=self.context.get("pipeline_id"),
                status=status
            )
            
            if not response:
                print("\n❌ No scheduled posts found.")
                return
            
            print("\n" + "-" * 80)
            print(f"{'ID':<15} {'PLATFORM':<10} {'STATUS':<10} {'SCHEDULED TIME':<25} {'CONTENT'}")
            print("-" * 80)
            
            for post in response:
                content_preview = post.get('content', {}).get('text', 'N/A')
                if len(content_preview) > 30:
                    content_preview = content_preview[:27] + "..."
                    
                print(f"{post.get('id', 'N/A'):<15} {post.get('channel', 'N/A'):<10} {post.get('status', 'N/A'):<10} {post.get('scheduledTime', 'N/A'):<25} {content_preview}")
            
            print("-" * 80)
        
        except Exception as e:
            print(f"\n❌ Error fetching scheduled posts: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _check_active_pipeline(self) -> bool:
        """Check if there is an active pipeline and prompt to set one if not."""
        if not self.context.get("pipeline_id"):
            print("\n⚠️ No active pipeline set.")
            if self._confirm("Would you like to set an active pipeline now?"):
                self._set_active_pipeline()
                return bool(self.context.get("pipeline_id"))
            return False
        return True


def main():
    """Run the interactive CLI."""
    session = InteractiveSession()
    session.start()


if __name__ == "__main__":
    main()
