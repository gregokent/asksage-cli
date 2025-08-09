import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from ..dataset_utils import resolve_dataset_name, extract_short_name

if TYPE_CHECKING:
    from asksageclient import AskSageClient


def register_parser(subparsers) -> None:
    """Register the query subcommand parser."""
    parser = subparsers.add_parser('query', help='Query AskSage AI models')
    parser.add_argument('message', help='The question or message to query')
    parser.add_argument('--dataset', '-d', help='Limit query to specific dataset (short name or full name)')
    parser.add_argument('--model', '-m', help='Specify AI model to use')
    parser.add_argument('--file', '-f', help='Include a file with the query')
    parser.add_argument('--persona', '-p', help='Use a specific persona for the query')
    parser.add_argument('--plugin', help='Use a specific plugin for the query')


def execute(client: 'AskSageClient', args: argparse.Namespace) -> None:
    """Execute the query command."""
    try:
        if args.file:
            _query_with_file(client, args)
        elif args.plugin:
            _query_with_plugin(client, args)
        else:
            _query_basic(client, args)
    except Exception as e:
        print(f"Error executing query: {e}", file=sys.stderr)
        sys.exit(1)


def _query_basic(client: 'AskSageClient', args: argparse.Namespace) -> None:
    """Execute a basic text query."""
    try:
        # Resolve and assign dataset if specified
        if args.dataset:
            dataset_name = resolve_dataset_name(client, args.dataset)
            if dataset_name is None:
                print(f"Error: Dataset '{args.dataset}' not found.", file=sys.stderr)
                sys.exit(1)
            client.assign_dataset(dataset=dataset_name)
        
        response = client.query(message=args.message)
        
        if isinstance(response, dict):
            # Check for API error responses
            if response.get('status', 200) >= 400:
                error_msg = response.get('error') or response.get('message', 'Unknown error')
                print(f"Query failed: {error_msg}", file=sys.stderr)
                sys.exit(1)
            else:
                # Extract response message from proper API format
                message = response.get('message') or response.get('response', 'No response content')
                print(message)
        else:
            # Handle string response
            print(response)
            
    except Exception as e:
        print(f"Error executing query: {e}", file=sys.stderr)
        sys.exit(1)


def _query_with_file(client: 'AskSageClient', args: argparse.Namespace) -> None:
    """Execute a query with an attached file."""
    file_path = Path(args.file)
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    if not file_path.is_file():
        print(f"Error: Path is not a file: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Resolve and assign dataset if specified
        if args.dataset:
            dataset_name = resolve_dataset_name(client, args.dataset)
            if dataset_name is None:
                print(f"Error: Dataset '{args.dataset}' not found.", file=sys.stderr)
                sys.exit(1)
            client.assign_dataset(dataset=dataset_name)
        
        response = client.query_with_file(
            message=args.message,
            file_path=str(file_path)
        )
        
        if isinstance(response, dict):
            # Check for API error responses
            if response.get('status', 200) >= 400:
                error_msg = response.get('error') or response.get('message', 'Unknown error')
                print(f"Query failed: {error_msg}", file=sys.stderr)
                sys.exit(1)
            else:
                # Extract response message from proper API format
                message = response.get('message') or response.get('response', 'No response content')
                print(message)
        else:
            print(response)
            
    except Exception as e:
        print(f"Error executing query with file: {e}", file=sys.stderr)
        sys.exit(1)


def _query_with_plugin(client: 'AskSageClient', args: argparse.Namespace) -> None:
    """Execute a query using a specific plugin."""
    try:
        # Resolve and assign dataset if specified
        if args.dataset:
            dataset_name = resolve_dataset_name(client, args.dataset)
            if dataset_name is None:
                print(f"Error: Dataset '{args.dataset}' not found.", file=sys.stderr)
                sys.exit(1)
            client.assign_dataset(dataset=dataset_name)
        
        response = client.query_plugin(
            message=args.message,
            plugin_name=args.plugin
        )
        
        if isinstance(response, dict):
            # Check for API error responses
            if response.get('status', 200) >= 400:
                error_msg = response.get('error') or response.get('message', 'Unknown error')
                print(f"Query failed: {error_msg}", file=sys.stderr)
                sys.exit(1)
            else:
                # Extract response message from proper API format
                message = response.get('message') or response.get('response', 'No response content')
                print(message)
        else:
            print(response)
            
    except Exception as e:
        print(f"Error executing plugin query: {e}", file=sys.stderr)
        sys.exit(1)