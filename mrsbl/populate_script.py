#!/usr/bin/env python3
print('hi')
import argparse
import os
import re
import sys

def create_subject_specific_script(sub, ses, template_script_path):
    """
    Create a customized MATLAB script for a given subject and session.
    
    Args:
        sub (str): Subject identifier (e.g., 'sub-01')
        ses (str): Session identifier (e.g., 'ses-01')
        template_script_path (str): Path to the MATLAB template file
    
    Returns:
        str: Full path to the newly created script
    """
    if not os.path.isfile(template_script_path):
        sys.exit(f"Error: Template file not found at {template_script_path}")

    with open(template_script_path, 'r') as f:
        content = f.read()
    
    content = re.sub(r"sub\s*=\s*'.*?';", f"sub = '{sub}';", content)
    content = re.sub(r"ses\s*=\s*'.*?';", f"ses = '{ses}';", content)

    base_dir = os.path.dirname(template_script_path)
    new_filename = f"quality_check_setup_MC_{sub}_{ses}.m"
    new_filename=new_filename.replace('-', '_')  # Replace spaces with underscores
    new_filepath = os.path.join(base_dir, new_filename)

    with open(new_filepath, 'w') as f:
        f.write(content)
    
    return new_filepath

def main():
    parser = argparse.ArgumentParser(
        description="Generate subject/session-specific MATLAB script from template."
    )
    parser.add_argument('--sub', required=True, help="Subject ID (e.g., sub-01)")
    parser.add_argument('--ses', required=True, help="Session ID (e.g., ses-01)")
    parser.add_argument('--template', required=True, help="Path to template MATLAB script")

    args = parser.parse_args()
    new_script = create_subject_specific_script(args.sub, args.ses, args.template)
    print(f"New script created: {new_script}")

if __name__ == "__main__":
    main()
