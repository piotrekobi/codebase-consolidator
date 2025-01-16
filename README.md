# Codebase Consolidator

A simple utility to consolidate your codebase into a single file, making it easier to share your project context with AI assistants like Claude. Instead of uploading multiple files one by one, you can create a single file containing your entire codebase structure and the contents of selected files.

## Why?

When working with AI assistants, you often need to share multiple files to provide context about your project. Uploading files one by one is tedious and you need to repeat this process every time you start a new conversation. This tool creates a single file that includes:
- A tree view of your project structure
- Contents of all the files you want to share
- Proper file path labeling for context

## Usage

1. Create a `.codebase_filenames` file in your project root:
    ```
    Included:
    src/main.py
    src/utils.py
    config/settings.json

    Ignored from tree:
    node_modules*
    *.pyc
    build*
    ```

2. Run the script:
    ```bash
    python codebase_consolidator.py
    ```

The script will generate a `.codebase_content` file containing your project tree and the contents of specified files.

## Alias Setup (PowerShell)

1. Save the script as `codebase_consolidator.py` in your home directory
2. Create/edit your PowerShell profile (will be created if it doesn't exist):
    ```powershell
    if (!(Test-Path -Path $PROFILE)) {
        New-Item -ItemType File -Path $PROFILE -Force
    }
    notepad $PROFILE
    ```
3. Add this line to your profile:
    ```powershell
    Function codebase { python $HOME\codebase_consolidator.py }
    ```
4. Reload your profile:
    ```powershell
    . $PROFILE
    ```

## Alias Setup (bash)

1. Save the script as `codebase_consolidator.py` in your home directory
2. Add this line to your `~/.bashrc` (or `~/.zshrc` for Zsh):
    ```bash
    alias codebase="python ~/codebase_consolidator.py"
    ```
3. Reload your shell configuration:
    ```bash
    source ~/.bashrc  # or source ~/.zshrc for Zsh
    ```

## File Format

**`.codebase_filenames`:**
- `Included:` section - List files you want to include in the output
- `Ignored from tree:` section - Patterns for files/directories to exclude from the project tree (uses glob patterns like .gitignore)

## Output Example

The generated `.codebase_content` file will look like this:

```
Project Tree:
├── src
│   ├── main.py
│   └── utils.py
└── config
    └── settings.json

================================================================================

[FILE: src/main.py]

<contents of main.py>

================================================================================

[FILE: src/utils.py]

<contents of utils.py>

================================================================================
```
