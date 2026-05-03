import json
import os
from typing import Dict, Any, List

def load_json(filepath: str) -> Any:
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return None

def save_json(filepath: str, data: Any) -> None:
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def compute_progress(striver_sheet: List[Dict], solved_slugs: set) -> Dict[str, Any]:
    total_problems = len(striver_sheet)
    completed_problems = 0
    topics = {}

    for question in striver_sheet:
        topic = question.get("topic", "Uncategorized")
        slug = question.get("slug")
        
        if topic not in topics:
            topics[topic] = {"done": 0, "total": 0}
            
        topics[topic]["total"] += 1
        
        if slug in solved_slugs:
            topics[topic]["done"] += 1
            completed_problems += 1
            
    percentage = (completed_problems / total_problems * 100) if total_problems > 0 else 0.0
    
    return {
        "total": total_problems,
        "completed": completed_problems,
        "percentage": round(percentage, 1),
        "topics": topics
    }
