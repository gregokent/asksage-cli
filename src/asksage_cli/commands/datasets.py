import argparse
import sys
from typing import TYPE_CHECKING

from ..dataset_utils import resolve_dataset_name, extract_short_name, list_datasets_with_short_names

if TYPE_CHECKING:
    from asksageclient import AskSageClient


def register_parser(subparsers) -> None:
    """Register the datasets subcommand parser."""
    parser = subparsers.add_parser('datasets', help='Manage datasets')
    datasets_subparsers = parser.add_subparsers(dest='datasets_action', help='Dataset actions')
    
    # datasets add
    add_parser = datasets_subparsers.add_parser('add', help='Add a new dataset')
    add_parser.add_argument('name', help='Name of the dataset to add (alphanumeric)')
    
    # datasets delete  
    delete_parser = datasets_subparsers.add_parser('delete', help='Delete an existing dataset')
    delete_parser.add_argument('name', help='Dataset name to delete (short name or full name)')
    
    # datasets list
    datasets_subparsers.add_parser('list', help='List all datasets')


def execute(client: 'AskSageClient', args: argparse.Namespace) -> None:
    """Execute the datasets command."""
    if not args.datasets_action:
        print("Error: No datasets action specified. Use 'add', 'delete', or 'list'.", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.datasets_action == 'add':
            _add_dataset(client, args.name)
        elif args.datasets_action == 'delete':
            _delete_dataset(client, args.name)
        elif args.datasets_action == 'list':
            _list_datasets(client)
    except Exception as e:
        print(f"Error executing datasets command: {e}", file=sys.stderr)
        sys.exit(1)


def _add_dataset(client: 'AskSageClient', name: str) -> None:
    """Add a new dataset."""
    if not name.replace('-', '').replace('_', '').isalnum():
        print("Error: Dataset name must be alphanumeric (hyphens and underscores allowed).", file=sys.stderr)
        sys.exit(1)
    
    response = client.add_dataset(dataset=name)
    
    if isinstance(response, dict):
        # Check for API error responses based on status codes
        status = response.get('status', 200)
        if status >= 400:
            error_msg = response.get('error') or response.get('message', 'Unknown error')
            print(f"Failed to add dataset: {error_msg}", file=sys.stderr)
            sys.exit(1)
        else:
            # Success response - dataset added
            print(f"Successfully added dataset: {name}")
    else:
        # Handle non-dict responses
        print(f"Successfully added dataset: {name}")


def _delete_dataset(client: 'AskSageClient', name: str) -> None:
    """Delete an existing dataset."""
    # Resolve the dataset name to the full unique name
    full_name = resolve_dataset_name(client, name)
    
    if full_name is None:
        print(f"Error: Dataset '{name}' not found.", file=sys.stderr)
        sys.exit(1)
    
    response = client.delete_dataset(dataset=full_name)
    
    if isinstance(response, dict):
        # Check for API error responses based on status codes
        status = response.get('status', 200)
        if status >= 400:
            error_msg = response.get('error') or response.get('message', 'Unknown error')
            print(f"Failed to delete dataset: {error_msg}", file=sys.stderr)
            sys.exit(1)
        else:
            # Success response - dataset deleted
            short_name = extract_short_name(full_name)
            if short_name != full_name:
                print(f"Successfully deleted dataset: {short_name} ({full_name})")
            else:
                print(f"Successfully deleted dataset: {full_name}")
    else:
        # Handle non-dict responses - assume success if no error
        short_name = extract_short_name(full_name)
        if short_name != full_name:
            print(f"Successfully deleted dataset: {short_name} ({full_name})")
        else:
            print(f"Successfully deleted dataset: {full_name}")


def _list_datasets(client: 'AskSageClient') -> None:
    """List all datasets."""
    try:
        # Get datasets directly from client
        response = client.get_datasets()
        
        # Handle different response formats
        if isinstance(response, dict):
            status = response.get('status', 200)
            if status >= 400:
                error_msg = response.get('error') or response.get('message', 'Unknown error')
                print(f"Failed to retrieve datasets: {error_msg}", file=sys.stderr)
                sys.exit(1)
            
            # Extract dataset list from response
            datasets = response.get('response', [])
        elif isinstance(response, list):
            datasets = response
        else:
            print(f"Unexpected response format: {response}", file=sys.stderr)
            sys.exit(1)
        
        if not datasets:
            print("No datasets found.")
            return
        
        print("Available datasets:")
        for dataset_name in datasets:
            short_name = extract_short_name(dataset_name)
            if short_name != dataset_name:
                print(f"  - {short_name} ({dataset_name})")
            else:
                print(f"  - {dataset_name}")
            
    except Exception as e:
        print(f"Failed to retrieve datasets: {e}", file=sys.stderr)
        sys.exit(1)