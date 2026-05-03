import requests
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_all_solved_questions(username: str) -> list[str]:
    """
    Fetches the recently accepted questions for the user.
    Since LeetCode's public API only exposes the most recent AC submissions,
    this function will return those. The tracker will incrementally add them 
    to the progress data to build up a complete list over time.
    """
    url = "https://leetcode.com/graphql"
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        titleSlug
      }
    }
    """
    
    variables = {
        "username": username,
        "limit": 50 # Fetch up to 50 recent submissions
    }
    
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/{username}/"
    }

    # Optional: if a session cookie is provided, use it to try to fetch more or make authenticated queries
    session_cookie = os.getenv("LEETCODE_SESSION")
    if session_cookie:
        headers["Cookie"] = f"LEETCODE_SESSION={session_cookie};"

    try:
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            logging.error(f"GraphQL errors: {data['errors']}")
            return []
            
        submissions = data.get("data", {}).get("recentAcSubmissionList", [])
        if not submissions:
            return []
            
        slugs = [sub["titleSlug"] for sub in submissions if sub.get("titleSlug")]
        
        # Deduplicate while preserving order
        unique_slugs = list(dict.fromkeys(slugs))
        logging.info(f"Fetched {len(unique_slugs)} recent unique accepted submissions for {username}")
        print(unique_slugs)
        return unique_slugs

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from LeetCode API: {e}")
        return []
