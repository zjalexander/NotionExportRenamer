import os
import re
from pathlib import Path

def strip_guid_from_name(name):
    """
    Remove GUID patterns from a filename or folder name.
    Handles common GUID formats:
    - name_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    - name-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    - name xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    """
    # Pattern for standard GUID format (8-4-4-4-12 hexadecimal digits)
    guid_pattern = r'[-_\s][0-9a-fA-F\-]{32,}'
    
    # For files, preserve the extension
    if '.' in name:
        name_part, ext = os.path.splitext(name)
        cleaned_name = re.sub(guid_pattern, '', name_part)
        return cleaned_name + ext
    else:
        # For folders or files without extensions
        return re.sub(guid_pattern, '', name)

def rename_recursively(directory_path, dry_run=True):
    """
    Recursively rename files and folders to remove GUIDs.
    
    Args:
        directory_path: Root directory to process
        dry_run: If True, only print what would be renamed without actually renaming
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Error: Directory '{directory_path}' does not exist")
        return
    
    # Process from deepest level first to avoid issues with renaming parent folders
    all_paths = sorted(directory.rglob('*'), key=lambda p: len(p.parts), reverse=True)
    
    renamed_count = 0
    
    for path in all_paths:
        old_name = path.name
        new_name = strip_guid_from_name(old_name)
        
        # Only rename if the name changed
        if new_name != old_name and new_name.strip():
            new_path = path.parent / new_name
            
            # Check if target already exists
            if new_path.exists():
                print(f"⚠️  Skipping (target exists): {path}")
                continue
            
            if dry_run:
                print(f"Would rename: {path}")
                print(f"         to: {new_path}\n")
            else:
                try:
                    path.rename(new_path)
                    print(f"✓ Renamed: {old_name} → {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"✗ Error renaming {path}: {e}")
    
    if dry_run:
        print("\n*** DRY RUN MODE - No files were actually renamed ***")
        print("Run with dry_run=False to perform actual renaming")
    else:
        print(f"\n✓ Successfully renamed {renamed_count} items")

# Example usage:
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Remove hex string identifiers from file and folder names')
    parser.add_argument('path', help='Directory path to process')
    parser.add_argument('--no-dry-run', action='store_true', 
                        help='Actually perform the renaming (default is dry-run mode)')
    
    args = parser.parse_args()
    
    dry_run = not args.no_dry_run
    
    if dry_run:
        print("=== DRY RUN MODE ===")
        print("(Use --no-dry-run to actually rename files)\n")
    else:
        print("=== RENAMING FILES ===\n")
    
    rename_recursively(args.path, dry_run=dry_run)
