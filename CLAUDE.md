# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `asksage-cli`, a Python command-line tool that provides a streamlined interface for using AskSage from the command line, built on top of the `asksageclient` library.

## Development Commands

### Installation and Setup
- Install dependencies: `uv sync`
- Install in development mode: `uv pip install -e .`

### Running the Application
- Run the CLI: `asksage_cli` (after installation)
- Run directly from source: `python -m asksage_cli`

### Building
- Build the package: `uv build`

## CLI Commands

The CLI provides the following subcommands:

### Authentication Setup
Set environment variables:
```bash
export ASKSAGE_EMAIL="your_email@example.com"
export ASKSAGE_API_KEY="your_api_key"
export ASKSAGE_USER_BASE_URL="https://api.asksage.ai/user"    # Optional, defaults to official instance
export ASKSAGE_SERVER_BASE_URL="https://api.asksage.ai/server" # Optional, defaults to official instance
```

Or create `~/.asksage/config.json`:
```json
{
  "email": "your_email@example.com",
  "api_key": "your_api_key",
  "user_base_url": "https://api.asksage.ai/user",
  "server_base_url": "https://api.asksage.ai/server"
}
```

For testing without credentials:
```bash
export ASKSAGE_TEST_MODE=1
```

### Datasets Management
- `asksage_cli datasets list` - List all available datasets
- `asksage_cli datasets add <name>` - Add a new dataset (alphanumeric names)
- `asksage_cli datasets delete <full_name>` - Delete an existing dataset

### Training Content
- `asksage_cli train file <path> -d <dataset>` - Train a single file into a dataset
- `asksage_cli train directory <path> -d <dataset>` - Train all files in a directory
  - `--recursive` - Process directories recursively
  - `--extensions .txt .py .md` - Specify file extensions (default: .txt .md .py .js .json)
  - `--context "context info"` - Add context information
  - `--summarize` - Enable summarization during training

### Querying Models
- `asksage_cli query "Your question here"` - Basic query
- `asksage_cli query "Question" --dataset <name>` - Query limited to specific dataset
- `asksage_cli query "Question" --file <path>` - Query with file attachment
- `asksage_cli query "Question" --plugin <plugin_name>` - Query using specific plugin

### Token Usage
- `asksage_cli tokens` - Show monthly token usage in human-readable format
- `asksage_cli tokens --format json` - Show token usage in JSON format

## Architecture

The project follows a simple Python CLI structure:

- **Entry Point**: `src/asksage/__init__.py` contains the `main()` function that serves as the CLI entry point
- **Package Structure**: Standard Python package layout with `src/` directory
- **Dependencies**: Built on `asksageclient>=1.31` for AskSage integration
- **Build System**: Uses `uv_build` as the build backend

The CLI is currently in early development with a basic "Hello from asksage!" placeholder implementation.

## Development Notes

- Python 3.13+ required
- Uses `uv` for dependency management and building
- Main entry point defined in `pyproject.toml` as `asksage = "asksage:main"`