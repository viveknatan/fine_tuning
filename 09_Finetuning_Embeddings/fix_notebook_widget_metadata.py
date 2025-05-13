#!/usr/bin/env python3
import json
import sys
import os
import re
import nbformat
from pathlib import Path

def fix_notebook(notebook_path):
    """
    Comprehensive fix for Jupyter notebook widget metadata issues that prevent GitHub rendering.
    This function can:
    1. Add missing 'state' key to 'metadata.widgets'
    2. Remove problematic widget metadata entirely
    3. Clean up any corrupt metadata structures
    """
    print(f"Processing notebook: {notebook_path}")
    
    # Create backup of original file
    backup_path = f"{notebook_path}.backup"
    try:
        Path(notebook_path).rename(backup_path)
        print(f"Created backup at: {backup_path}")
        
        # Copy the backup back to original path for processing
        with open(backup_path, 'rb') as src, open(notebook_path, 'wb') as dst:
            dst.write(src.read())
    except Exception as e:
        print(f"Warning: Failed to create backup: {e}")
    
    # Try using nbformat first (recommended approach)
    try:
        notebook = nbformat.read(notebook_path, as_version=nbformat.NO_CONVERT)
        modified = False
        
        # Check if the notebook has metadata
        if hasattr(notebook, 'metadata'):
            # Option 1: Fix widget metadata by adding state
            if 'widgets' in notebook.metadata:
                if 'state' not in notebook.metadata.widgets:
                    notebook.metadata.widgets['state'] = {}
                    modified = True
                    print("Added missing 'state' key to metadata.widgets")
                
                # Ensure widget metadata structure is valid
                if not isinstance(notebook.metadata.widgets, dict):
                    notebook.metadata.widgets = {'state': {}}
                    modified = True
                    print("Fixed invalid widgets metadata structure")
            
            # Option 2: If there are deeper issues, remove widgets metadata entirely
            if 'widgets' in notebook.metadata:
                del notebook.metadata['widgets']
                modified = True
                print("Removed potentially problematic widgets metadata")
        
        if modified:
            # Write the fixed notebook using nbformat
            nbformat.write(notebook, notebook_path)
            print(f"Notebook updated successfully using nbformat")
            return True
            
    except Exception as e:
        print(f"Warning: nbformat approach failed: {e}")
    
    # Fallback to manual JSON parsing if nbformat fails
    try:
        # Read the file as text first
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to fix any JSON formatting issues using regex before parsing
        # Replace any instances of trailing commas in objects/arrays
        content = re.sub(r',(\s*[\]}])', r'\1', content)
        
        # Parse the possibly fixed JSON
        notebook = json.loads(content)
        modified = False
        
        # Approach 1: Remove widgets metadata entirely
        if 'metadata' in notebook and 'widgets' in notebook['metadata']:
            del notebook['metadata']['widgets']
            modified = True
            print("Removed widgets metadata completely")
        
        # Approach 2: If no metadata section exists, create bare minimum
        if 'metadata' not in notebook:
            notebook['metadata'] = {}
            modified = True
            print("Added missing metadata section")
        
        if modified:
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1)
            print(f"Notebook updated successfully using manual JSON approach")
            return True
    
    except Exception as e:
        print(f"Error: Both approaches failed. Manual editing may be required: {e}")
        # Restore from backup if we haven't been able to fix it
        try:
            os.remove(notebook_path)
            Path(backup_path).rename(notebook_path)
            print(f"Restored original file from backup due to processing errors")
        except Exception as restore_err:
            print(f"Error: Failed to restore from backup: {restore_err}")
    
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_notebook_widgets.py path/to/notebook.ipynb")
        sys.exit(1)
    
    notebook_path = sys.argv[1]
    if not os.path.exists(notebook_path):
        print(f"Error: File not found: {notebook_path}")
        sys.exit(1)
    
    if not notebook_path.endswith('.ipynb'):
        print(f"Warning: File does not have .ipynb extension: {notebook_path}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    success = fix_notebook(notebook_path)
    if success:
        print("Notebook has been fixed. Try uploading to GitHub again.")
    else:
        print("Unable to fix notebook automatically.")