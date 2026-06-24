# Amy-To-Do-List

# AI-Assisted Personal Task Assistant

A lightweight Python-based task assistant that uses a user-maintained CSV template and structured ChatGPT prompts to generate clear daily task summaries.

The project was built to explore how simple structured data, prompt design and automation can be combined to reduce manual admin. The user keeps their tasks updated in a basic CSV file, and the assistant processes that data into a more useful daily summary, highlighting overdue tasks, tasks due today, upcoming items and lower-priority later actions.

## Key Features

* Uses a simple CSV template as the source of truth
* Allows the user to maintain their own task list without needing a complex app
* Groups tasks into overdue, due today, upcoming and later categories
* Uses ChatGPT prompts to generate a clear, human-readable daily summary
* Highlights urgent actions and short-term priorities
* Produces a more supportive and readable output than a standard task table
* Designed to be extendable into email delivery, dashboard views or calendar integration

## Tools Used

* Python
* pandas
* CSV-based data input
* ChatGPT / LLM prompt design
* datetime logic
* Automated message generation

## Why I Built It

I built this project to help my girlfriend get on top of a growing to do list that had become a bit overwhelming.

Rather than creating a full task management app or asking her to change how she already kept track of things, I designed it around the format of her existing task list. The idea was to keep the input simple, just a CSV file she could continue updating in the same way, and use the automation to turn that long list into a clearer daily plan.

ChatGPT prompts are used to make the output feel more encouraging and less like reading a spreadsheet. Alongside prioritising tasks, the assistant generates a light hearted summary to help keep motivation up and make the whole process feel less daunting.

It was a fun project that combined automation, AI and a real world problem, while exploring how simple tools can make everyday admin a little easier to manage without adding extra process.

## How It Works

1. The user updates a CSV file with their current tasks, due dates and any relevant notes.
2. The Python script reads and processes the CSV data.
3. Tasks are grouped based on due date and urgency.
4. A structured ChatGPT prompt is generated using the processed task data.
5. The AI response is used to create a concise daily task summary and motivational information to help start the users day!
6. The final output can be reviewed, copied, emailed or adapted for future delivery methods.

## Example Use Case

A user has a list of personal admin tasks stored in a CSV file. Instead of manually reviewing the full list each day, the assistant generates a short summary showing:

* What is overdue
* What needs attention today
* What is coming up soon
* What can wait until later
* A short motivational or supportive closing note
