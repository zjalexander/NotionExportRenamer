import os
import re
from pathlib import Path
from urllib.parse import unquote, quote

def strip_guid_from_name(name):
    """
    Remove hex string patterns from a filename or folder name.
    Handles:
    - name xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (space + 32+ hex chars)
    - name_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (underscore + 32+ hex chars)
    - name-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (hyphen + 32+ hex chars)
    - name xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (standard GUID format)
    """
    # Pattern for hex strings (32 or more hex characters, with or without dashes)
    guid_pattern = r'[-_\s][0-9a-fA-F\-]{32,}'
    
    # For files, preserve the extension
    if '.' in name:
        name_part, ext = os.path.splitext(name)
        cleaned_name = re.sub(guid_pattern, '', name_part)
        return cleaned_name + ext
    else:
        # For folders or files without extensions
        return re.sub(guid_pattern, '', name)

def clean_markdown_links(content):
    """
    Clean hex strings from markdown links in content.
    Handles both inline links [text](file.md) and reference-style links.
    Also handles URL-encoded links with %20 for spaces.
    """
    # Pattern for inline markdown links: [text](filename)
    def replace_inline_link(match):
        text = match.group(1)
        link = match.group(2)
        
        # Decode URL encoding to get actual filename
        decoded_link = unquote(link)
        # Clean the hex strings
        cleaned_link = strip_guid_from_name(decoded_link)
        # Re-encode for use in markdown link
        encoded_link = quote(cleaned_link, safe='/.#?=&')
        
        return f"[{text}]({encoded_link})"
    
    # Pattern for reference-style links: [text][ref] or [ref]: url
    def replace_reference_link(match):
        ref = match.group(1)
        link = match.group(2)
        
        # Decode URL encoding to get actual filename
        decoded_link = unquote(link)
        # Clean the hex strings
        cleaned_link = strip_guid_from_name(decoded_link)
        # Re-encode for use in markdown link
        encoded_link = quote(cleaned_link, safe='/.#?=&')
        
        return f"[{ref}]: {encoded_link}"
    
    # Clean inline links: [text](link)
    content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', replace_inline_link, content)
    
    # Clean reference-style links: [ref]: link
    content = re.sub(r'\[([^\]]+)\]:\s*(.+)$', replace_reference_link, content, flags=re.MULTILINE)
    
    # Clean wiki-style links: [[filename]]
    def replace_wiki_link(match):
        link = match.group(1)
        cleaned_link = strip_guid_from_name(link)
        return f"[[{cleaned_link}]]"
    
    content = re.sub(r'\[\[([^\]]+)\]\]', replace_wiki_link, content)
    
    return content

def update_markdown_files(directory_path, dry_run=True):
    """
    Update markdown file contents to clean links.
    """
    directory = Path(directory_path)
    updated_count = 0
    
    for md_file in directory.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            cleaned_content = clean_markdown_links(original_content)
            
            if cleaned_content != original_content:
                if dry_run:
                    print(f"Would update links in: {md_file}")
                else:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)
                    print(f"✓ Updated links in: {md_file.name}")
                    updated_count += 1
        except Exception as e:
            print(f"✗ Error processing {md_file}: {e}")
    
    return updated_count

def rename_recursively(directory_path, dry_run=True):
    """
    Recursively rename files and folders to remove GUIDs, and update markdown links.
    
    Args:
        directory_path: Root directory to process
        dry_run: If True, only print what would be renamed without actually renaming
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Error: Directory '{directory_path}' does not exist")
        return
    
    # First, update markdown file contents
    print("=== Updating Markdown Links ===\n")
    updated_count = update_markdown_files(directory_path, dry_run)
    
    if not dry_run:
        print(f"\n✓ Updated {updated_count} markdown files\n")
    
    print("\n=== Renaming Files and Folders ===\n")
    
    # Process from deepest level first to avoid issues with renaming parent folders
    all_paths = sorted(directory.rglob('*'), key=lambda p: len(p.parts), reverse=True)
    
    renamed_count = 0
    
    for path in all_paths:
        if not path.is_file() and not path.is_dir():
            continue
            
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
        print("Run with --no-dry-run to perform actual renaming")
    else:
        print(f"\n✓ Successfully renamed {renamed_count} items")

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
