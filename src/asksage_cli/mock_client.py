"""Mock AskSage client for testing without network calls."""

from typing import Dict, List, Any, Union
import json
import os
import random
from pathlib import Path


class MockAskSageClient:
    """Mock client that simulates AskSage API responses without making network calls."""
    
    def __init__(self, email: str, api_key: str, **kwargs):
        self.email = email
        self.api_key = api_key
        # Mock some realistic dataset names
        self._user_id = 145128821  # Fixed user ID for consistent testing
        self._datasets = [
            f"user_custom_{self._user_id}_example_content",
            f"user_custom_{self._user_id}_test-data_content",
            f"user_custom_{self._user_id}_docs_content"
        ]
        self._current_dataset = None
    
    def add_dataset(self, dataset: str) -> Dict[str, Any]:
        """Mock dataset addition."""
        full_name = f"user_custom_{self._user_id}_{dataset}_content"
        if full_name not in self._datasets:
            self._datasets.append(full_name)
            return {"status": 200, "response": f"Dataset {dataset} created successfully"}
        return {"status": 400, "error": "Dataset already exists"}
    
    def delete_dataset(self, dataset: str) -> Dict[str, Any]:
        """Mock dataset deletion."""
        if dataset in self._datasets:
            self._datasets.remove(dataset)
            return {"status": 200, "response": f"Dataset {dataset} deleted successfully"}
        return {"status": 404, "error": "Dataset not found"}
    
    def get_datasets(self) -> Dict[str, Any]:
        """Mock get datasets."""
        return {"status": 200, "response": self._datasets.copy()}
    
    def assign_dataset(self, dataset: str) -> Dict[str, Any]:
        """Mock dataset assignment."""
        self._current_dataset = dataset
        return {"status": 200, "response": f"Dataset {dataset} assigned"}
    
    def train_with_file(self, file_path: str, context: str = None, dataset: str = None, **kwargs) -> Dict[str, Any]:
        """Mock file training."""
        if not os.path.exists(file_path):
            return {"status": 404, "error": f"File not found: {file_path}"}
        
        file_size = os.path.getsize(file_path)
        return {
            "status": 200,
            "response": f"Successfully trained file {file_path}",
            "embedding": [0.1, 0.2, 0.3] * 100,  # Mock embedding vector
            "tokens_used": min(file_size // 4, 1000),  # Mock token calculation
            "dataset": dataset or self._current_dataset
        }
    
    def train(self, content: Dict[str, str], **kwargs) -> Dict[str, Any]:
        """Mock content training."""
        content_length = len(str(content))
        return {
            "status": 200,
            "response": "Content trained successfully",
            "embedding": [0.1, 0.2, 0.3] * 100,  # Mock embedding vector
            "tokens_used": content_length // 4,
            "dataset": kwargs.get('force_dataset') or self._current_dataset
        }
    
    def query(self, message: str, **kwargs) -> Dict[str, Any]:
        """Mock query."""
        mock_responses = [
            "This is a mock response from AskSage AI. Your question was: '{}'".format(message),
            "Mock AI Response: I understand you're asking about '{}'. Here's a simulated answer.".format(message),
            "Simulated AskSage Response: Based on your query '{}', here's what I can tell you...".format(message)
        ]
        
        response_text = mock_responses[len(message) % len(mock_responses)]
        
        return {
            "status": 200,
            "message": response_text,
            "embedding_down": False,
            "vectors_down": False,
            "uuid": "mock-uuid-12345",
            "references": [],
            "teach": False,
            "tokens_used": len(message) // 2,
            "model": "mock-gpt-4o",
            "dataset": self._current_dataset
        }
    
    def query_with_file(self, message: str, file_path: str, **kwargs) -> Dict[str, Any]:
        """Mock query with file."""
        if not os.path.exists(file_path):
            return {"status": 404, "error": f"File not found: {file_path}"}
        
        file_size = os.path.getsize(file_path)
        return {
            "status": 200,
            "message": f"Mock response analyzing file {Path(file_path).name}: {message}",
            "embedding_down": False,
            "vectors_down": False,
            "uuid": "mock-uuid-with-file-12345",
            "references": [f"File: {Path(file_path).name}"],
            "teach": False,
            "tokens_used": (len(message) + file_size) // 3,
            "model": "mock-gpt-4o",
            "file_analyzed": file_path
        }
    
    def query_plugin(self, message: str, plugin_name: str, **kwargs) -> Dict[str, Any]:
        """Mock plugin query."""
        return {
            "status": 200,
            "message": f"Mock response from plugin '{plugin_name}': {message}",
            "embedding_down": False,
            "vectors_down": False,
            "uuid": "mock-plugin-uuid-12345",
            "references": [f"Plugin: {plugin_name}"],
            "teach": False,
            "tokens_used": len(message) // 2,
            "plugin": plugin_name,
            "dataset": self._current_dataset
        }
    
    def count_monthly_tokens(self) -> Dict[str, Any]:
        """Mock monthly token count."""
        return {"status": 200, "response": 15750}
    
    def count_monthly_teach_tokens(self) -> Dict[str, Any]:
        """Mock teaching token count."""
        return {"status": 200, "response": 3280}
    
    def get_models(self) -> List[str]:
        """Mock available models."""
        return [
            "mock-gpt-4o",
            "mock-claude-3.5-sonnet",
            "mock-gemini-pro",
            "mock-llama-3.1"
        ]
    
    def get_personas(self) -> List[Dict[str, Any]]:
        """Mock personas."""
        return [
            {"name": "Assistant", "description": "General purpose AI assistant"},
            {"name": "Developer", "description": "Programming and development focused"},
            {"name": "Researcher", "description": "Academic and research oriented"}
        ]
    
    def get_plugins(self) -> List[Dict[str, Any]]:
        """Mock plugins."""
        return [
            {"name": "web_search", "description": "Search the web for information"},
            {"name": "code_analyzer", "description": "Analyze and review code"},
            {"name": "document_processor", "description": "Process various document formats"}
        ]