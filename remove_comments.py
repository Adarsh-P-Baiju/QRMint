import os
import re

def remove_comments_from_file(filepath):
    """Remove simple single-line comments from Python files"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified_lines = []
    for line in lines:
        # Remove standalone comment lines (lines that are only whitespace + comment)
        if re.match(r'^\s*#[^!]', line):
            # Skip this line (don't add it)
            continue
        # Remove inline comments (keep the code, remove the comment)
        elif ' #' in line and not line.strip().startswith('#'):
            # Remove inline comment but keep the code
            code_part = line.split(' #')[0].rstrip() + '\n'
            modified_lines.append(code_part)
        else:
            modified_lines.append(line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(modified_lines)
    
    print(f"Processed: {filepath}")

def process_directory(directory):
    """Process all Python files in directory and subdirectories"""
    for root, dirs, files in os.walk(directory):
        # Skip env directory
        if 'env' in dirs:
            dirs.remove('env')
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    remove_comments_from_file(filepath)
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    upi_app_dir = r"f:\python\upi qr code\upi_app"
    process_directory(upi_app_dir)
    print("\nComment removal complete!")
