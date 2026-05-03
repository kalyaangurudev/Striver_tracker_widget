import os
import logging
from dotenv import load_dotenv
from leetcode_api import get_all_solved_questions
from mapper import load_json, save_json, compute_progress

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
STRIVER_SHEET_PATH = os.path.join(DATA_DIR, 'striver_sheet.json')
PROGRESS_PATH = os.path.join(DATA_DIR, 'progress.json')

def main():
    # Load environment variables
    load_dotenv()
    username = os.getenv("LEETCODE_USERNAME")
    
    if not username:
        logging.error("LEETCODE_USERNAME is not set in .env")
        return

    # Load Striver sheet
    striver_sheet = load_json(STRIVER_SHEET_PATH)
    if not striver_sheet:
        logging.error("Could not load striver_sheet.json")
        return

    # Load existing progress to get previously tracked slugs
    progress_data = load_json(PROGRESS_PATH) or {}
    existing_slugs = set(progress_data.get("solved_slugs", []))

    # Fetch recently solved questions
    recent_slugs = get_all_solved_questions(username)
    
    # Merge existing slugs with recent slugs
    new_slugs_added = 0
    for slug in recent_slugs:
        if slug not in existing_slugs:
            existing_slugs.add(slug)
            new_slugs_added += 1
            
    if new_slugs_added > 0:
        logging.info(f"Added {new_slugs_added} new solved problems.")
    else:
        logging.info("No new solved problems found.")

    # Compute progress based on updated slug list
    progress_stats = compute_progress(striver_sheet, existing_slugs)
    
    # Add the full list of slugs to the progress data so it persists
    progress_stats["solved_slugs"] = list(existing_slugs)

    # Save output
    save_json(PROGRESS_PATH, progress_stats)
    logging.info(f"Progress updated! Total completion: {progress_stats['percentage']}%")

if __name__ == "__main__":
    main()
