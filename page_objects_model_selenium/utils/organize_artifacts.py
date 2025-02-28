# utils/organize_artifacts.py
import os
import re
import shutil
import glob
import json
from datetime import datetime

def organize_test_artifacts(base_dir="reports"):
    """
    Organize test artifacts into a structured format:
    - reports/
      - test_runs/
        - YYYY-MM-DD_HH-MM-SS/
          - test_name_1/
            - video.mp4
            - screenshot.png
            - logs.txt
            - page_source.html
          - test_name_2/
            ...
    """
    print("Organizing test artifacts...")
    
    # Create directories
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    run_dir = os.path.join(base_dir, "test_runs", timestamp)
    os.makedirs(run_dir, exist_ok=True)
    
    # Find all session info files
    session_files = glob.glob(os.path.join(base_dir, "videos", "session_info_*.txt"))
    
    for session_file in session_files:
        # Extract test name and session ID
        test_name = None
        session_id = None
        
        with open(session_file, 'r') as f:
            content = f.read()
            test_match = re.search(r'Test: (.*?)\n', content)
            session_match = re.search(r'Session ID: (.*?)\n', content)
            
            if test_match:
                test_name = test_match.group(1)
                test_name = re.sub(r'[^\w\-]', '_', test_name)  # Clean test name
            
            if session_match:
                session_id = session_match.group(1)
        
        if not test_name or not session_id:
            print(f"Couldn't extract test info from {session_file}")
            continue
            
        # Create test directory
        test_dir = os.path.join(run_dir, test_name)
        os.makedirs(test_dir, exist_ok=True)
        
        # Copy session info
        shutil.copy(session_file, os.path.join(test_dir, "session_info.txt"))
        
        # Find and copy video
        video_file = os.path.join(base_dir, "videos", f"{session_id}.mp4")
        if os.path.exists(video_file):
            shutil.copy(video_file, os.path.join(test_dir, "test_execution.mp4"))
        
        # Find and copy screenshots
        screenshot_pattern = os.path.join(base_dir, "screenshots", f"*{test_name}*.png")
        for screenshot in glob.glob(screenshot_pattern):
            shutil.copy(screenshot, os.path.join(test_dir, "failure_screenshot.png"))
            
        # Find and copy HTML source
        html_pattern = os.path.join(base_dir, "screenshots", f"page_source_*{test_name}*.html")
        for html_file in glob.glob(html_pattern):
            shutil.copy(html_file, os.path.join(test_dir, "page_source.html"))
            
    print(f"Artifacts organized in: {run_dir}")
    return run_dir