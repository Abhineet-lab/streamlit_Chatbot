# Install required library first:
# pip install streamlit dateparser

import streamlit as st
from datetime import datetime, timedelta
import re
import dateparser

# -------------------------------
# Time expression parser function
# -------------------------------
def get_date_range_from_expression(expression: str):
    now = datetime.now()

    expression = expression.lower().strip()

    # Handle quarter-based expressions
    quarter_match = re.match(r"(1st|first|2nd|second|3rd|third|4th|fourth|q1|q2|q3|q4)\s*(quarter)?\s*(of|in)?\s*(\d{4})", expression)
    if quarter_match:
        quarter_map = {
            "1st": (1, 3), "first": (1, 3), "q1": (1, 3),
            "2nd": (4, 6), "second": (4, 6), "q2": (4, 6),
            "3rd": (7, 9), "third": (7, 9), "q3": (7, 9),
            "4th": (10, 12), "fourth": (10, 12), "q4": (10, 12)
        }
        quarter_key = quarter_match.group(1)
        year = int(quarter_match.group(4))
        quarter = quarter_map[quarter_key]
        start_date = datetime(year, quarter[0], 1)
        end_date = datetime(year, quarter[1] + 1, 1) - timedelta(days=1) if quarter[1] < 12 else datetime(year + 1, 1, 1) - timedelta(days=1)
        return start_date.date(), end_date.date()

    # Handle week/month specific logic
    if expression == "yesterday":
        d = now - timedelta(days=1)
        return d.date(), d.date()

    if expression == "today":
        d = now
        return d.date(), d.date()

    if "last week" in expression:
        start = now - timedelta(days=now.weekday() + 7)
        end = start + timedelta(days=6)
        return start.date(), end.date()

    if "this week" in expression:
        start = now - timedelta(days=now.weekday())
        end = start + timedelta(days=6)
        return start.date(), end.date()

    if "last month" in expression:
        first_this_month = now.replace(day=1)
        last_month_end = first_this_month - timedelta(days=1)
        start = last_month_end.replace(day=1)
        end = last_month_end
        return start.date(), end.date()

    if "this month" in expression:
        start = now.replace(day=1)
        next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = next_month - timedelta(days=1)
        return start.date(), end.date()

    # Try parsing a single date (fallback)
    start = dateparser.parse(expression)
    if start:
        return start.date(), start.date()

    # If everything fails
    raise ValueError("Could not parse the time expression. Try expressions like 'last week', 'Q1 2024', or '10 July 2025'.")

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="🗓️ Date Expression Parser", layout="centered")
st.title("🧠 Natural Language Date Parser")
st.markdown("Enter a natural time expression (e.g., `last week`, `Q1 2023`, `yesterday`, `third quarter of 2024`)")

user_input = st.text_input("🗨️ Time Frame Expression")

if user_input:
    try:
        start_date, end_date = get_date_range_from_expression(user_input)
        st.success(f"✅ Start Date: **{start_date}**\n\n✅ End Date: **{end_date}**")
    except ValueError as e:
        st.error(str(e))
