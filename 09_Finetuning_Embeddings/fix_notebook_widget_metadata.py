#!/usr/bin/env python3
import json
import sys
import os

def fix_notebook(notebook_path):
    """
    Fix Jupyter notebook widget metadata by adding the missing 'state' key
    to the 'metadata.widgets' section if needed.
    """
    print(f"Processing notebook: {notebook_path}")
    
    # Read the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    modified = False
    
    # Check if the notebook has metadata
    if 'metadata' in notebook:
        # Check if metadata has widgets section
        if 'widgets' in notebook['metadata']:
            # Check if state key is missing
            if 'state' not in notebook['metadata']['widgets']:
                # Add empty state dictionary
                notebook['metadata']['widgets']['state'] = {}
                modified = True
                print("Added missing 'state' key to metadata.widgets")
            else:
                print("'state' key already exists in metadata.widgets")
        else:
            print("No 'widgets' section found in metadata")
    else:
        print("No metadata found in notebook")
    
    # Save the modified notebook if changes were made
    if modified:
        # Create backup of original file
        backup_path = notebook_path + '.backup'
        os.rename(notebook_path, backup_path)
        print(f"Created backup at: {backup_path}")
        
        # Write the fixed notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2)
        print(f"Notebook updated successfully at: {notebook_path}")
    else:
        print("No changes were needed or made to the notebook")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_notebook_widget_metadata.py path/to/notebook.ipynb")
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
    
    fix_notebook(notebook_path)