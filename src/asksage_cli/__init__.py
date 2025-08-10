import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from asksageclient import AskSageClient

from .commands import datasets, train, query, tokens
from .mock_client import MockAskSageClient


def get_client() -> AskSageClient:
    """Initialize and return AskSage client with credentials from environment or config."""
    # Check for test mode
    if os.getenv('ASKSAGE_TEST_MODE', '').lower() in ('1', 'true', 'yes'):
        print("Running in test mode with mock client")
        return MockAskSageClient(email="test@example.com", api_key="test_key")
    
    email = os.getenv('ASKSAGE_EMAIL')
    api_key = os.getenv('ASKSAGE_API_KEY')
    user_base_url = os.getenv('ASKSAGE_USER_BASE_URL')
    server_base_url = os.getenv('ASKSAGE_SERVER_BASE_URL')
    
    if not email or not api_key:
        config_path = Path.home() / '.asksage' / 'config.json'
        if config_path.exists():
            import json
            try:
                with open(config_path) as f:
                    config = json.load(f)
                email = config.get('email', email)
                api_key = config.get('api_key', api_key)
                user_base_url = config.get('user_base_url', user_base_url)
                server_base_url = config.get('server_base_url', server_base_url)
            except (json.JSONDecodeError, KeyError, FileNotFoundError):
                pass
    
    if not email or not api_key:
        print("Error: AskSage credentials not found.", file=sys.stderr)
        print("Set ASKSAGE_EMAIL and ASKSAGE_API_KEY environment variables,", file=sys.stderr)
        print("or create ~/.asksage/config.json with your credentials.", file=sys.stderr)
        print("Or set ASKSAGE_TEST_MODE=1 to use mock client for testing.", file=sys.stderr)
        sys.exit(1)
    
    # Build client arguments
    client_args = {'email': email, 'api_key': api_key}
    if user_base_url:
        client_args['user_base_url'] = user_base_url
    if server_base_url:
        client_args['server_base_url'] = server_base_url
    
    return AskSageClient(**client_args)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='asksage',
        description='Command-line interface for AskSage AI platform',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Register subcommands
    datasets.register_parser(subparsers)
    train.register_parser(subparsers)
    query.register_parser(subparsers)
    tokens.register_parser(subparsers)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Get client instance
    try:
        client = get_client()
    except Exception as e:
        print(f"Error initializing AskSage client: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Execute the appropriate command
    if args.command == 'datasets':
        datasets.execute(client, args)
    elif args.command == 'train':
        train.execute(client, args)
    elif args.command == 'query':
        query.execute(client, args)
    elif args.command == 'tokens':
        tokens.execute(client, args)
