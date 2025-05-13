import json
import sys

def fix_widgets_metadata(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    metadata = nb.get('metadata', {})
    widgets = metadata.get('widgets', None)

    if widgets is not None:
        # Option 1: Remove the widgets metadata entirely
        # del metadata['widgets']

        # Option 2: Ensure 'state' key exists
        if 'state' not in widgets:
            widgets['state'] = {}

        metadata['widgets'] = widgets
        nb['metadata'] = metadata

        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print(f"Fixed: {notebook_path}")
    else:
        print(f"No widgets metadata found in: {notebook_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_notebook_widgets.py <notebook.ipynb>")
    else:
        fix_widgets_metadata(sys.argv[1])