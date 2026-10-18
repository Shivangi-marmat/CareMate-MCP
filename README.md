# CareMate-MCP

CareMate-MCP is an AI-powered care reminder project built using the **Model Context Protocol (MCP)**. It provides tools to add, view, and delete care reminders stored in a MySQL database.

## Features

- **Add reminders** — save a task and its reminder time.
- **List reminders** — view saved reminders.
- **Delete reminders** — remove a reminder by its ID.
- **Persistent storage** — reminders are stored in MySQL.
- **MCP server** — exposes the tools through Streamable HTTP.

## Technology Stack

- Python
- MCP Python SDK
- MySQL
- MySQL Connector/Python

## Project Files

- `server.py` — MCP server and reminder tools.
- `test_client.py` — Python client for testing the MCP tools.
- `requirements.txt` — Python dependencies.
- `README.md` — project documentation.

## Requirements

Install the following before starting:

- Python 3.11 or newer
- MySQL Server
- Git

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Shivangi-marmat/CareMate-MCP.git
cd CareMate-MCP
```

If your cloned repository contains another folder named `CareMate-MCP`, enter that inner folder before continuing.

### 2. Create and activate a virtual environment

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Create the MySQL database

Open MySQL Workbench and execute:

```sql
CREATE DATABASE IF NOT EXISTS caremate;

USE caremate;

CREATE TABLE IF NOT EXISTS reminders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    reminder_time VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Configure the database connection

Set these environment variables in the same terminal where you will run the server.

For Windows PowerShell:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = "YOUR_MYSQL_PASSWORD"
$env:DB_NAME = "caremate"
```

Replace `YOUR_MYSQL_PASSWORD` with your own local MySQL password. Do not commit your password to GitHub.

If your MySQL account uses a different username or port, adjust the values accordingly.

### 6. Start the MCP server

```powershell
python server.py
```

The server uses Streamable HTTP at:

`http://127.0.0.1:8000/mcp`

Keep the server terminal open while testing.

### 7. Test the MCP tools

Open a second terminal in the project folder and activate the virtual environment:

```powershell
.venv\Scripts\activate
python test_client.py
```

The test client checks adding, listing, and deleting a reminder.

## Available MCP Tools

| Tool | Purpose |
|---|---|
| `add_reminder` | Saves a care task and its time. |
| `list_reminders` | Returns saved reminders. |
| `delete_reminder` | Deletes a reminder by ID. |

## Important Notes

- The server URL above is local to your computer. It is not publicly accessible for remote integrations.
- Each developer needs a configured MySQL database unless the team sets up a shared database.
- Alexa+ integration and public deployment are separate steps; this README does not claim they are already complete.

## Team

Built by the CareMate-MCP team for the Amazon Alexa+ Hackathon.
