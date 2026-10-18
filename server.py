
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timezone

mcp = FastMCP("CareMate-MCP")

# Temporary storage for reminders
reminders = []
next_id = 1


@mcp.tool()
def add_reminder(task: str, time: str) -> dict:
    """Add a care reminder with a task and time."""
    global next_id

    if not task.strip() or not time.strip():
        return {
            "success": False,
            "message": "Task and time are required."
        }

    reminder = {
        "id": next_id,
        "task": task.strip(),
        "time": time.strip(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    reminders.append(reminder)
    next_id += 1

    return {
        "success": True,
        "reminder": reminder
    }


@mcp.tool()
def list_reminders() -> list:
    """List all saved care reminders."""
    return reminders.copy()


@mcp.tool()
def delete_reminder(reminder_id: int) -> dict:
    """Delete a reminder by its ID."""
    for reminder in reminders:
        if reminder["id"] == reminder_id:
            reminders.remove(reminder)
            return {
                "success": True,
                "message": "Reminder deleted."
            }

    return {
        "success": False,
        "message": "Reminder not found."
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
