# AI-Assisted Daily Task Email Assistant

A lightweight Python assistant that turns a user-maintained CSV task list into a clear daily email summary using structured ChatGPT prompts.

The tool reads an existing task list, groups items by urgency and due date, and emails the user a simple overview of what needs attention today, what is overdue and what can wait.

## Key Features

* Uses a simple CSV file as the source of truth
* Works with the user's existing task list format
* Groups tasks by overdue, due today, upcoming and later
* Uses ChatGPT prompts to generate a clear, supportive summary (includes motivational quotes)
* Sends the summary by email automatically
* Keeps the process lightweight without requiring a new task management app

## Tools Used

* Python
* pandas
* CSV input
* ChatGPT / LLM prompts
* Email automation
* Scheduled workflow automation

## Why I Built It

I built this to help my girlfriend manage a growing to do list that had become a bit overwhelming.

Rather than asking her to change how she tracked things, I designed the assistant around her existing CSV task list. The aim was to keep the input simple, then use automation and ChatGPT prompts to turn the list into a more helpful daily email.

The ChatGPT output makes the summary feel more encouraging and light hearted, while still giving a clear view of what needs doing first.

## How It Works

1. The user updates their CSV task list.
2. The Python script reads and processes the task data.
3. Tasks are grouped by urgency and due date.
4. A structured ChatGPT prompt generates a daily summary.
5. The summary is automatically emailed to the user.

## Example Use Case

Each day, the user receives an email showing:

* Overdue tasks
* Tasks due today
* Upcoming tasks
* Lower-priority items
* A short motivational note
