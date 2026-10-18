

import os
from datetime import datetime, timezone

import mysql.connector
from mysql.connector import Error
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CareMate-MCP")


def get_db_connection():
    """Connect to the CareMate MySQL database."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "caremate"),
    )


@mcp.tool()
def add_reminder(task: str, time: str) -> dict:
    """Add a care reminder with a task and time."""
    if not task.strip() or not time.strip():
        return {
            "success": False,
            "message": "Task and time are required.",
        }

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            INSERT INTO reminders (task, reminder_time)
            VALUES (%s, %s)
            """,
            (task.strip(), time.strip()),
        )
        connection.commit()

        reminder_id = cursor.lastrowid
        cursor.execute(
            """
            SELECT id, task, reminder_time, created_at
            FROM reminders WHERE id = %s
            """,
            (reminder_id,),
        )
        reminder = cursor.fetchone()

        if reminder and reminder["created_at"]:
            reminder["created_at"] = reminder["created_at"].isoformat()

        return {"success": True, "reminder": reminder}

    except Error as exc:
        return {"success": False, "message": f"Database error: {exc}"}

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()


@mcp.tool()
def list_reminders() -> list:
    """List all saved care reminders."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, task, reminder_time, created_at
            FROM reminders ORDER BY id
            """
        )
        rows = cursor.fetchall()

        for row in rows:
            if row["created_at"]:
                row["created_at"] = row["created_at"].isoformat()

        return rows

    except Error as exc:
        return [{"success": False, "message": f"Database error: {exc}"}]

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()


@mcp.tool()
def delete_reminder(reminder_id: int) -> dict:
    """Delete a reminder by its ID."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM reminders WHERE id = %s",
            (reminder_id,),
        )
        connection.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "Reminder not found.",
            }

        return {"success": True, "message": "Reminder deleted."}

    except Error as exc:
        return {"success": False, "message": f"Database error: {exc}"}

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
ss