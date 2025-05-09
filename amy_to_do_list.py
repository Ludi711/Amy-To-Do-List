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

# Load task records
data = sheet.get_all_records()

# Convert to DataFrame
df = pd.DataFrame(data)

# Clean up dates and completed column
df['Due Date'] = pd.to_datetime(df['Due Date'], errors='coerce')
df['Completed?'] = df['Completed?'].astype(str).str.strip().str.upper() == 'TRUE'

df.head()

# Drop empty tasks
df = df.dropna(subset=['Task', 'Due Date'])

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


def format_tasks(df):
    # Sort by priority: High → Medium → Low
    priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
    df = df.copy()
    df['PriorityOrder'] = df['Priority'].map(priority_order)
    df = df.sort_values(by='PriorityOrder')

    return "\n".join(
        f"- {row['Task']} (Priority: {row['Priority']}, due {row['Due Date'].date()})"
        for _, row in df.iterrows()
    )


# Format each section
overdue_text = format_tasks(overdue)
today_text = format_tasks(due_today)
upcoming_text = format_tasks(upcoming)

# Add task counts
overdue_count = len(overdue)
today_count = len(due_today)
upcoming_count = len(upcoming)


# Final prompt for ChatGPT
prompt = f"""
You are "Pixel", Amy's AI personal assistant.

Write a concise, clear email summarizing her tasks for the day. Be warm and friendly, but keep the tone efficient — no unnecessary intro or fluff. Just a light greeting and helpful task summary.

At the top of the email, include a one-line summary like:
"You have 1 overdue task, 2 due today, and 3 coming up."

Then present the tasks by category, sorted by priority.

🟥 Overdue Tasks ({overdue_count}):
{overdue_text or '- None'}

🟩 Tasks Due Today ({today_count}):
{today_text or '- None'}

📅 Upcoming (next 3 days) ({upcoming_count}):
{upcoming_text or '- None'}

End with a single uplifting quote or affirmation. Sign off as Pixel.
"""

print(prompt)

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
send_task_email(email_body, "amy.lou.wils@gmail.com")







# In[ ]:





# In[ ]:




