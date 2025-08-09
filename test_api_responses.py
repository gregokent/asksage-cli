#!/usr/bin/env python3
"""
Test script to understand actual asksageclient API response formats.
This will help us align the CLI with the real API responses.
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from asksage_cli.mock_client import MockAskSageClient

def test_mock_client_responses():
    """Test the mock client to understand expected response formats."""
    print("=== TESTING MOCK CLIENT RESPONSES ===\n")
    
    client = MockAskSageClient("test@example.com", "test_key")
    
    print("1. Dataset Operations:")
    print(f"get_datasets(): {repr(client.get_datasets())}")
    print(f"add_dataset('test'): {repr(client.add_dataset('test'))}")
    print(f"delete_dataset('test'): {repr(client.delete_dataset('user_custom_145128821_test_content'))}")
    print()
    
    print("2. Token Operations:")
    print(f"count_monthly_tokens(): {repr(client.count_monthly_tokens())}")
    print(f"count_monthly_teach_tokens(): {repr(client.count_monthly_teach_tokens())}")
    print()
    
    print("3. Query Operations:")
    print(f"query('test'): {repr(client.query('test'))}")
    print()
    
    # Create a test file for training
    test_file = "/tmp/test_api_response.txt"
    with open(test_file, "w") as f:
        f.write("Test content for API response testing")
    
    print("4. Training Operations:")
    print(f"train_with_file(): {repr(client.train_with_file(test_file, dataset='test'))}")
    
    # Clean up
    os.unlink(test_file)

def test_real_client_import():
    """Test importing the real client to see if we can inspect it."""
    print("\n=== TESTING REAL CLIENT IMPORT ===\n")
    
    try:
        from asksageclient import AskSageClient
        print("Successfully imported AskSageClient")
        print(f"AskSageClient methods: {[m for m in dir(AskSageClient) if not m.startswith('_')]}")
        
        # Try to inspect method signatures
        import inspect
        for method in ['get_datasets', 'add_dataset', 'delete_dataset', 'train_with_file', 'query', 'count_monthly_tokens']:
            if hasattr(AskSageClient, method):
                sig = inspect.signature(getattr(AskSageClient, method))
                print(f"{method} signature: {sig}")
        
        # Try to inspect source or docstrings
        print(f"\nget_datasets docstring: {AskSageClient.get_datasets.__doc__}")
        print(f"add_dataset docstring: {AskSageClient.add_dataset.__doc__}")
        
    except Exception as e:
        print(f"Error importing or inspecting AskSageClient: {e}")

def test_real_client_with_dummy_credentials():
    """Try to create real client with dummy credentials to see error responses."""
    print("\n=== TESTING REAL CLIENT ERROR RESPONSES ===\n")
    
    try:
        from asksageclient import AskSageClient
        
        # Create client with dummy credentials to see what error responses look like
        client = AskSageClient("fake@example.com", "fake_api_key")
        
        # Try to call methods and see what error formats we get
        try:
            result = client.get_datasets()
            print(f"get_datasets() with fake creds: {repr(result)}")
        except Exception as e:
            print(f"get_datasets() error: {type(e).__name__}: {e}")
            
        try:
            result = client.count_monthly_tokens()
            print(f"count_monthly_tokens() with fake creds: {repr(result)}")
        except Exception as e:
            print(f"count_monthly_tokens() error: {type(e).__name__}: {e}")
        
    except Exception as e:
        print(f"Error creating or testing real client: {e}")

if __name__ == "__main__":
    test_mock_client_responses()
    test_real_client_import()
    test_real_client_with_dummy_credentials()