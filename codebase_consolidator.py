import os
from pathlib import Path
import fnmatch

# Always ignore these files
BUILT_IN_IGNORES = ['.codebase_filenames', '.codebase_content']

def parse_codebase_filenames():
    """Parse the .codebase_filenames file to get included files and ignored patterns."""
    included_files = []
    ignored_patterns = []
    
    current_section = None
    with open('.codebase_filenames', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            if line == "Included:":
                current_section = "included"
                continue
            elif line == "Ignored from tree:":
                current_section = "ignored"
                continue
                
            if current_section == "included":
                # Don't include built-in ignored files
                if line not in BUILT_IN_IGNORES:
                    included_files.append(str(Path(line)))
            elif current_section == "ignored":
                ignored_patterns.append(line.replace('\\', '/'))
                
    return included_files, ignored_patterns

def should_ignore(path, ignore_patterns):
    """Check if a path should be ignored based on patterns."""
    # Convert to forward slashes for pattern matching
    path_str = str(path).replace(os.sep, '/')
    
    # Check built-in ignores first
    if path.name in BUILT_IN_IGNORES:
        return True
        
    # Then check user-defined patterns
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path_str, pattern):
            return True
    return False

def generate_tree(ignore_patterns):
    """Generate a tree structure of the entire codebase, excluding ignored patterns."""
    tree = {}
    
    for root, dirs, files in os.walk('.'):
        # Convert root to relative path and normalize separators
        rel_root = Path(root).relative_to('.')
        
        # Remove ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(rel_root / d, ignore_patterns)]
        
        current = tree
        if str(rel_root) != '.':
            parts = rel_root.parts
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        
        # Add non-ignored files
        for file in files:
            if not should_ignore(rel_root / file, ignore_patterns):
                current[file] = None
    
    return tree

def print_tree(node, prefix="", is_last=True):
    """Convert tree structure to string representation."""
    lines = []
    if prefix == "":
        lines.append("Project Tree:")
    
    items = list(node.items())
    for i, (name, subtree) in enumerate(items):
        is_last_item = i == len(items) - 1
        connector = "└── " if is_last_item else "├── "
        lines.append(prefix + connector + name)
        
        if subtree is not None:  # If it's a directory
            extension = "    " if is_last_item else "│   "
            lines.extend(print_tree(subtree, prefix + extension, is_last_item))
    return lines

def consolidate_codebase():
    """Consolidate codebase files into a single file."""
    included_files, ignored_patterns = parse_codebase_filenames()
    
    # Generate and format the tree
    tree = generate_tree(ignored_patterns)
    tree_text = "\n".join(print_tree(tree))
    
    with open('.codebase_content', 'w', encoding='utf-8') as out:
        # Write the tree
        out.write(tree_text + "\n\n")
        out.write("=" * 80 + "\n\n")
        
        # Process each included file
        for file_path in included_files:
            path = Path(file_path)
            if not path.exists():
                print(f"Warning: File not found: {file_path}")
                continue
            
            # Write file path label using forward slashes for consistency
            display_path = str(path).replace(os.sep, '/')
            out.write(f"[FILE: {display_path}]\n\n")
            
            # Write file contents
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    out.write(content)
                    if not content.endswith('\n'):
                        out.write('\n')
                    out.write('\n')
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
            
            out.write("=" * 80 + "\n\n")

if __name__ == "__main__":
    try:
        consolidate_codebase()
        print("Successfully consolidated codebase into .codebase_content")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)