# asksage-cli

Command-line interface for the AskSage AI platform. Provides streamlined access to datasets, training, querying, and token management.

## Installation

```bash
uv sync
```

## Configuration

Set credentials via environment variables:
```bash
export ASKSAGE_EMAIL="your_email@example.com"
export ASKSAGE_API_KEY="your_api_key"
```

Or create `~/.asksage/config.json`:
```json
{
  "email": "your_email@example.com",
  "api_key": "your_api_key"
}
```

For testing without credentials:
```bash
export ASKSAGE_TEST_MODE=1
```

## Usage

### Dataset Management

```bash
# List all datasets
uv run asksage_cli datasets list

# Add new dataset
uv run asksage_cli datasets add my-dataset

# Delete dataset (supports short or full names)
uv run asksage_cli datasets delete my-dataset
```

### Training Content

```bash
# Train single file
uv run asksage_cli train file document.pdf -d my-dataset

# Train directory with options
uv run asksage_cli train directory ./docs -d my-dataset --recursive --extensions .md .txt

# Add context during training
uv run asksage_cli train file code.py -d my-dataset --context "Python utility functions"
```

### Querying Models

```bash
# Basic query
uv run asksage_cli query "What is machine learning?"

# Query with dataset context
uv run asksage_cli query "Explain the API" --dataset my-dataset

# Query with file attachment
uv run asksage_cli query "Analyze this document" --file report.pdf
```

### Token Usage

```bash
# Human-readable format
uv run asksage_cli tokens

# JSON format
uv run asksage_cli tokens --format json
```

## Dataset Names

The CLI supports both short names and full unique names. When you create a dataset called `my-project`, it becomes `user_custom_123456_my-project_content` internally. You can reference it by either name:

```bash
uv run asksage_cli datasets delete my-project
# or
uv run asksage_cli datasets delete user_custom_123456_my-project_content
```

## Architecture

- `src/asksage_cli/` - Main CLI package
- `src/asksage_cli/commands/` - Subcommand implementations
- `src/asksage_cli/dataset_utils.py` - Dataset name resolution
- `src/asksage_cli/mock_client.py` - Testing client
