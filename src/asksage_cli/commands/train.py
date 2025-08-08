import argparse
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from asksageclient import AskSageClient


def register_parser(subparsers) -> None:
    """Register the train subcommand parser."""
    parser = subparsers.add_parser('train', help='Train content into datasets')
    train_subparsers = parser.add_subparsers(dest='train_action', help='Training actions')
    
    # train file
    file_parser = train_subparsers.add_parser('file', help='Train a single file')
    file_parser.add_argument('path', help='Path to the file to train')
    file_parser.add_argument('--dataset', '-d', required=True, help='Dataset name to train into')
    file_parser.add_argument('--context', '-c', help='Optional context information')
    file_parser.add_argument('--summarize', action='store_true', help='Enable summarization during training')
    
    # train directory
    dir_parser = train_subparsers.add_parser('directory', help='Train all files in a directory')
    dir_parser.add_argument('path', help='Path to the directory to train')
    dir_parser.add_argument('--dataset', '-d', required=True, help='Dataset name to train into')
    dir_parser.add_argument('--context', '-c', help='Optional context information')
    dir_parser.add_argument('--summarize', action='store_true', help='Enable summarization during training')
    dir_parser.add_argument('--recursive', '-r', action='store_true', help='Process directories recursively')
    dir_parser.add_argument('--extensions', nargs='*', default=['.txt', '.md', '.py', '.js', '.json'], 
                          help='File extensions to include (default: .txt .md .py .js .json)')


def execute(client: 'AskSageClient', args: argparse.Namespace) -> None:
    """Execute the train command."""
    if not args.train_action:
        print("Error: No train action specified. Use 'file' or 'directory'.", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.train_action == 'file':
            _train_file(client, args)
        elif args.train_action == 'directory':
            _train_directory(client, args)
    except Exception as e:
        print(f"Error executing train command: {e}", file=sys.stderr)
        sys.exit(1)


def _train_file(client: 'AskSageClient', args: argparse.Namespace) -> None:
    """Train a single file."""
    file_path = Path(args.path)
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    if not file_path.is_file():
        print(f"Error: Path is not a file: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Training file: {file_path}")
    
    try:
        # Use train_with_file method from the client
        response = client.train_with_file(
            file_path=str(file_path),
            context=args.context,
            dataset=args.dataset
        )
        
        if isinstance(response, dict) and response.get('success'):
            print(f"Successfully trained file {file_path} into dataset '{args.dataset}'")
        else:
            error_msg = response.get('error', 'Unknown error') if isinstance(response, dict) else str(response)
            print(f"Failed to train file: {error_msg}", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error training file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def _train_directory(client: 'AskSageClient', args: argparse.Namespace) -> None:
    """Train all files in a directory."""
    dir_path = Path(args.path)
    
    if not dir_path.exists():
        print(f"Error: Directory not found: {dir_path}", file=sys.stderr)
        sys.exit(1)
    
    if not dir_path.is_dir():
        print(f"Error: Path is not a directory: {dir_path}", file=sys.stderr)
        sys.exit(1)
    
    # Collect files to train
    files_to_train = _collect_files(dir_path, args.extensions, args.recursive)
    
    if not files_to_train:
        print(f"No files found in directory {dir_path} with extensions {args.extensions}")
        return
    
    print(f"Found {len(files_to_train)} files to train in dataset '{args.dataset}'")
    
    successful = 0
    failed = 0
    
    for file_path in files_to_train:
        print(f"Training: {file_path.relative_to(dir_path)}")
        
        try:
            response = client.train_with_file(
                file_path=str(file_path),
                context=args.context,
                dataset=args.dataset
            )
            
            if isinstance(response, dict) and response.get('success'):
                successful += 1
                print(f"  ✓ Success")
            else:
                failed += 1
                error_msg = response.get('error', 'Unknown error') if isinstance(response, dict) else str(response)
                print(f"  ✗ Failed: {error_msg}")
                
        except Exception as e:
            failed += 1
            print(f"  ✗ Error: {e}")
    
    print(f"\nTraining complete: {successful} successful, {failed} failed")
    
    if failed > 0:
        sys.exit(1)


def _collect_files(directory: Path, extensions: List[str], recursive: bool) -> List[Path]:
    """Collect files to train based on extensions and recursion settings."""
    files = []
    
    # Normalize extensions to lowercase and ensure they start with '.'
    normalized_extensions = []
    for ext in extensions:
        ext = ext.lower()
        if not ext.startswith('.'):
            ext = '.' + ext
        normalized_extensions.append(ext)
    
    if recursive:
        pattern = '**/*'
    else:
        pattern = '*'
    
    for file_path in directory.glob(pattern):
        if file_path.is_file():
            if file_path.suffix.lower() in normalized_extensions:
                files.append(file_path)
    
    return sorted(files)