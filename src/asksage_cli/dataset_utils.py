"""Utilities for dataset name resolution and management."""

import re
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from asksageclient import AskSageClient


def resolve_dataset_name(client, dataset_name: str) -> Optional[str]:
    """
    Resolve a dataset name to its full unique name.
    
    Args:
        client: AskSage client instance
        dataset_name: Either short name (e.g., 'sage-cli') or full name (e.g., 'user_custom_123_sage-cli_content')
    
    Returns:
        Full unique dataset name if found, None if not found
    """
    try:
        response = client.get_datasets()
        
        # Handle different response formats
        if isinstance(response, dict):
            status = response.get('status', 200)
            if status >= 400:
                return None  # Error getting datasets
            all_datasets = response.get('response', [])
        elif isinstance(response, list):
            all_datasets = response
        else:
            return None
        
        # If the provided name is already in the list (exact match), return it
        if dataset_name in all_datasets:
            return dataset_name
        
        # Look for datasets that match the pattern with this short name
        pattern = rf"user_custom_\d+_{re.escape(dataset_name)}_content$"
        
        matches = [ds for ds in all_datasets if re.match(pattern, ds)]
        
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            # Multiple matches - this shouldn't happen normally but handle gracefully
            return matches[0]  # Return the first match
        else:
            # No matches found
            return None
            
    except Exception:
        # If we can't get datasets, assume the name is correct as-is
        return dataset_name


def extract_short_name(full_dataset_name: str) -> str:
    """
    Extract the short name from a full dataset name.
    
    Args:
        full_dataset_name: Full name like 'user_custom_123_sage-cli_content'
    
    Returns:
        Short name like 'sage-cli', or the original name if it doesn't match the pattern
    """
    pattern = r"user_custom_\d+_(.+)_content$"
    match = re.match(pattern, full_dataset_name)
    
    if match:
        return match.group(1)
    else:
        # Return the original name if it doesn't match the expected pattern
        return full_dataset_name


def list_datasets_with_short_names(client) -> List[tuple[str, str]]:
    """
    Get all datasets with both their full and short names.
    
    Returns:
        List of tuples (full_name, short_name)
    """
    try:
        response = client.get_datasets()
        
        # Handle different response formats
        if isinstance(response, dict):
            status = response.get('status', 200)
            if status >= 400:
                return []  # Error getting datasets
            all_datasets = response.get('response', [])
        elif isinstance(response, list):
            all_datasets = response
        else:
            return []
        
        return [(ds, extract_short_name(ds)) for ds in all_datasets]
    except Exception:
        return []