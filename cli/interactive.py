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
