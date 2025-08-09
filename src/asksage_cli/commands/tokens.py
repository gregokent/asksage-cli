import argparse
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asksageclient import AskSageClient


def register_parser(subparsers) -> None:
    """Register the tokens subcommand parser."""
    parser = subparsers.add_parser('tokens', help='Check token usage statistics')
    parser.add_argument('--format', choices=['human', 'json'], default='human',
                       help='Output format (default: human)')


def execute(client: 'AskSageClient', args: argparse.Namespace) -> None:
    """Execute the tokens command."""
    try:
        _show_token_usage(client, args.format)
    except Exception as e:
        print(f"Error retrieving token usage: {e}", file=sys.stderr)
        sys.exit(1)


def _show_token_usage(client: 'AskSageClient', output_format: str) -> None:
    """Show monthly token usage statistics."""
    try:
        # Get monthly token counts
        monthly_response = client.count_monthly_tokens()
        teach_response = client.count_monthly_teach_tokens()
        
        # Handle different response formats
        def extract_token_count(response):
            if isinstance(response, dict):
                status = response.get('status', 200)
                if status >= 400:
                    error_msg = response.get('error') or response.get('message', 'Unknown error')
                    raise Exception(f"API error: {error_msg}")
                # Extract count from API response format
                return response.get('response', 0)
            elif isinstance(response, (int, float)):
                return int(response)
            else:
                return 0
        
        monthly_tokens = extract_token_count(monthly_response)
        teach_tokens = extract_token_count(teach_response)
        
        if output_format == 'json':
            import json
            data = {
                'monthly_tokens': monthly_tokens,
                'teach_tokens': teach_tokens
            }
            print(json.dumps(data, indent=2))
        else:
            # Human-readable format
            print("Monthly Token Usage:")
            print(f"  Query Tokens:    {monthly_tokens:,}")
            print(f"  Teaching Tokens: {teach_tokens:,}")
            
    except Exception as e:
        print(f"Failed to retrieve token usage: {e}", file=sys.stderr)
        sys.exit(1)