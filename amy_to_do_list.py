#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Define Google Sheets API scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials
creds_dict = json.loads(os.environ["GOOGLE_CREDS_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)

# Open your Google Sheet (sheet name must match exactly)
sheet = client.open("Amy - To Do List").sheet1

# Load all raw rows
data = sheet.get_all_values()

# Detect header row (where Task and Due Date are present)
header_row_idx = None
for idx, row in enumerate(data):
    row_stripped = [cell.strip().lower() for cell in row]
    if "task" in row_stripped and "due date" in row_stripped:
        header_row_idx = idx
        break

if header_row_idx is None:
    raise ValueError("Could not find header row with 'Task' and 'Due Date'.")

# Extract headers and data
headers = data[header_row_idx]
rows = data[header_row_idx + 1:]
df = pd.DataFrame(rows, columns=headers)

# Clean column names and cell values
df.columns = [col.strip() for col in df.columns]
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

# Parse dates and convert completion flag
df['Due Date'] = pd.to_datetime(df['Due Date'], dayfirst=True, errors='coerce')
df['Completed?'] = df['Completed?'].astype(str).str.strip().str.upper() == 'TRUE'

# Drop rows missing task name or date
df = df[df['Task'].notna() & (df['Task'].str.strip() != '')]

# Today
today = pd.Timestamp(datetime.now().date())

# Filter incomplete tasks
incomplete_df = df[df['Completed?'] == False]

# Grouping
overdue = incomplete_df[incomplete_df['Due Date'] < today]
due_today = incomplete_df[incomplete_df['Due Date'] == today]
upcoming = incomplete_df[
    (incomplete_df['Due Date'] > today) &
    (incomplete_df['Due Date'] <= today + pd.Timedelta(days=3))
]


def format_detailed_tasks(df, sort_oldest_first=True):
    priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
    df = df.copy()
    df['PriorityOrder'] = df['Priority'].map(priority_order)
    sort_order = ['Due Date', 'PriorityOrder'] if sort_oldest_first else ['PriorityOrder']
    df = df.sort_values(by=sort_order)

    return "\n".join(
        f"🔸 {row['Task']} ({row['Priority']} priority, due {row['Due Date'].date()})"
        for _, row in df.iterrows()
    )

def format_summary_section(df, label):
    if df.empty:
        return f"{label}: No tasks."
    summary = df['Priority'].value_counts().to_dict()
    parts = [f"{label} ({len(df)} task{'s' if len(df) != 1 else ''}):"]
    for level in ['High', 'Medium', 'Low']:
        if level in summary:
            parts.append(f"• {summary[level]} {level}")
    return "\n".join(parts)


# Format each section
overdue_text = format_tasks(overdue)
today_text = format_tasks(due_today)
upcoming_text = format_tasks(upcoming)

# Add task counts
overdue_count = len(overdue)
today_count = len(due_today)
upcoming_count = len(upcoming)
later = incomplete_df[incomplete_df['Due Date'] > today + pd.Timedelta(days=3)]
later_text = format_tasks(later)
later_count = len(later)



# 🟨 CREATE GPT PROMPT

# Base summary
summary_line = (
    f"You have {overdue_count} overdue task(s), "
    f"{today_count} due today, "
    f"{upcoming_count} coming up soon, "
    f"and {later_count} scheduled for later."
)


# Task sections
task_sections = f"""
🟥 Overdue Tasks ({overdue_count}):
{overdue_text or '- None'}

🟩 Tasks Due Today ({today_count}):
{today_text or '- None'}

📅 Upcoming (next 3 days) ({upcoming_count}):
{upcoming_text or '- None'}

📆 Later Tasks (beyond 3 days) ({later_count}):
{later_text or '- None'}
"""


# Strict prompt to avoid hallucination
if overdue_count == 0 and today_count == 0 and upcoming_count == 0 and later_count == 0:

    instruction = """
There are no outstanding tasks today. Do not fabricate or imagine any. 
Just write a warm, cheerful greeting to Amy and include a short uplifting quote. 
Sign off as Pixel."""
else:
    instruction = """
Only use the actual tasks provided below — do not create or invent any tasks. 
Structure the message as a warm, efficient daily update.
Sign off as Pixel."""

# Final prompt
summary_line = (
    f"You have {len(overdue)} overdue, {len(due_today)} due today, "
    f"{len(upcoming)} upcoming soon, and {len(later)} scheduled later."
)

prompt = f"""
You are Pixel, Amy's AI task assistant. Write a short, kind, uplifting and useful summary email for her day.

Start with this summary line:
"{summary_line}"

Then show the following:

🔴 Overdue Tasks:
{format_detailed_tasks(overdue)}

🟢 Tasks Due Today:
{format_detailed_tasks(due_today, sort_oldest_first=False)}

📅 Upcoming Tasks (within 3 days):
{format_summary_section(upcoming, 'Upcoming (within 3 days)')}

📆 Later Tasks (beyond 3 days):
{format_summary_section(later, 'Later (beyond 3 days)')}

End the email with a single motivational quote or affirmation. Sign off as Pixel.

"""


from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

email_body = response.choices[0].message.content
print(email_body)


import smtplib
from email.message import EmailMessage

# Compose the email
def send_task_email(email_body, to_address):
    msg = EmailMessage()
    msg['Subject'] = "To Do List! 🧠"
    msg['From'] = "goodhewwill@gmail.com"
    msg['To'] = to_address
    msg.set_content(email_body)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login("goodhewwill@gmail.com", os.getenv("GMAIL_APP_PASSWORD"))
        smtp.send_message(msg)

# Then call:
send_task_email(email_body, "Amy.wilson@ricardslodge.merton.sch.uk")

















# In[ ]:





# In[ ]:




