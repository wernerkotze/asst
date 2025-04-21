"""
API interaction module for the ASST CLI.
"""

import json
import sys
import requests
from typing import Dict, List, Any

from cli.config import get_config_value

class ApiClient:
    """Client for interacting with the ASST API."""
    
    def __init__(self, api_url: str = None):
        """Initialize the API client."""
        self.api_url = api_url or get_config_value("api_url")
        self.headers = {"Content-Type": "application/json"}
        self.timeout = get_config_value("timeout")
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Any:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (get, post, patch, delete)
            endpoint: API endpoint
            data: Request data
            params: Query parameters
            
        Returns:
            Any: Response data
        """
        url = f"{self.api_url}{endpoint}"
        
        try:
            if method.lower() == "get":
                response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            elif method.lower() == "post":
                response = requests.post(url, headers=self.headers, json=data, params=params, timeout=self.timeout)
            elif method.lower() == "patch":
                response = requests.patch(url, headers=self.headers, json=data, params=params, timeout=self.timeout)
            elif method.lower() == "delete":
                response = requests.delete(url, headers=self.headers, params=params, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            if response.status_code == 204:  # No content
                return {"status": "success"}
            
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to the API at {self.api_url}")
            print("Make sure the API server is running and accessible.")
            sys.exit(1)
        except requests.exceptions.Timeout:
            print(f"Error: Request timed out after {self.timeout} seconds")
            sys.exit(1)
        except requests.exceptions.HTTPError as e:
            print(f"Error: HTTP {e.response.status_code} - {e.response.reason}")
            try:
                error_data = e.response.json()
                print(f"Detail: {error_data.get('detail', 'No detail provided')}")
            except json.JSONDecodeError:
                print(f"Response: {e.response.text}")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Could not parse response as JSON")
            sys.exit(1)
    
    # Pipeline operations
    def list_pipelines(self, pipeline_type: str = None, active_only: bool = True) -> List[Dict]:
        """List all pipelines."""
        params = {}
        if pipeline_type:
            params["pipeline_type"] = pipeline_type
        params["active_only"] = str(active_only).lower()
        
        return self.make_request("get", "/pipelines/", params=params)
    
    def create_pipeline(self, pipeline_data: Dict) -> Dict:
        """Create a new pipeline."""
        return self.make_request("post", "/pipelines/", data=pipeline_data)
    
    def get_pipeline(self, pipeline_id: str) -> Dict:
        """Get a specific pipeline."""
        return self.make_request("get", f"/pipelines/{pipeline_id}")
    
    # Brand analysis operations
    def analyze_brand(self, request_data: Dict) -> Dict:
        """Analyze a brand using Pinterest board."""
        return self.make_request("post", "/analyze/brand/", data=request_data)
    
    def upload_brand_assets(self, files: List[str]) -> List[str]:
        """Upload brand assets."""
        # This would require multipart/form-data handling
        # For simplicity, we'll just return mock URLs
        return [f"https://storage.asst.ai/brand-assets/{file}" for file in files]
    
    # Competitor analysis operations
    def analyze_competitors(self, request_data: Dict) -> Dict:
        """Analyze competitors using Twitter handles."""
        return self.make_request("post", "/analyze/competitors/", data=request_data)
    
    def get_framework(self, framework_id: str) -> Dict:
        """Get a specific content framework."""
        return self.make_request("get", f"/analyze/competitors/frameworks/{framework_id}")
    
    # Content generation operations
    def retrieve_content(self, request_data: Dict) -> List[Dict]:
        """Retrieve content from various sources."""
        return self.make_request("post", "/content/retrieve", data=request_data)
    
    def enhance_content(self, request_data: Dict) -> List[Dict]:
        """Enhance raw content with hashtags and sentiment."""
        return self.make_request("post", "/content/enhance", data=request_data)
    
    def personalize_content(self, request_data: Dict) -> Dict:
        """Personalize content using AI."""
        return self.make_request("post", "/content/personalize", data=request_data)
    
    def generate_image(self, request_data: Dict) -> str:
        """Generate or fetch an image for content."""
        return self.make_request("post", "/content/image", data=request_data)
    
    def format_content(self, request_data: Dict) -> Dict:
        """Format content for a specific channel."""
        return self.make_request("post", "/content/format", data=request_data)
    
    # Scheduling operations
    def schedule_post(self, request_data: Dict) -> Dict:
        """Schedule a post for publication."""
        return self.make_request("post", "/schedule/post", data=request_data)
    
    def list_scheduled_posts(self, pipeline_id: str = None, status: str = None) -> List[Dict]:
        """List all scheduled posts."""
        params = {}
        if pipeline_id:
            params["pipeline_id"] = pipeline_id
        if status:
            params["status"] = status
        
        return self.make_request("get", "/schedule/posts", params=params)
    
    def get_scheduled_post(self, post_id: str) -> Dict:
        """Get a specific scheduled post."""
        return self.make_request("get", f"/schedule/posts/{post_id}")
    
    def publish_post_now(self, post_id: str) -> Dict:
        """Immediately publish a scheduled post."""
        return self.make_request("post", f"/schedule/posts/{post_id}/publish-now")
    
    def cancel_scheduled_post(self, post_id: str) -> Dict:
        """Cancel a scheduled post."""
        return self.make_request("delete", f"/schedule/posts/{post_id}")
