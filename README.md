# Striver DSA Tracker & macOS Widget

A local project that tracks your progress on the Striver A2Z DSA Sheet by syncing solved problems from LeetCode and displaying them in a beautiful macOS desktop widget.

## Features
- Fetches recent accepted submissions from LeetCode.
- Maps your solved questions against a predefined list of Striver's A2Z Sheet problems.
- Computes overall completion percentage and topic-wise statistics.
- Displays progress using a clean, dark-themed macOS widget (powered by Übersicht).

## Prerequisites
- Python 3.10+
- macOS (for the widget)
- [Übersicht](http://tracesof.net/uebersicht/)

## Installation & Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure `.env`:**
   Open `.env` and set your LeetCode username:
   ```env
   LEETCODE_USERNAME=your_username_here
   ```

3. **Initial Run:**
   Fetch your recent solved problems and initialize the `progress.json` data:
   ```bash
   python src/tracker.py
   ```
   *Note: This script uses LeetCode's public API to fetch your recent submissions. Run it periodically (or let the widget run it) to keep your progress updated.*

4. **Widget Setup (Übersicht):**
   - Install Übersicht.
   - Open your Übersicht widgets folder (Usually `~/Library/Application Support/Übersicht/widgets/`).
   - Copy or symlink the `widget/dsa-widget.jsx` file to that folder.
   - Ensure the path to the tracker inside `dsa-widget.jsx` correctly points to your project directory. 
   - Refresh Übersicht to see the widget.
