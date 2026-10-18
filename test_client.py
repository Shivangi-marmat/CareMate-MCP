
import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    async with streamablehttp_client(
        "http://127.0.0.1:8000/mcp"
    ) as (read_stream, write_stream, _):

        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Step 1: Add a reminder
            print("ADDING REMINDER...")

            added = await session.call_tool(
                "add_reminder",
                {
                    "task": "Test reminder",
                    "time": "9:00 PM",
                },
            )

            print("\nADD RESULT:")
            print(added)

            if added.isError or not added.content:
                print("Could not add reminder. Stopping test.")
                return

            # Step 2: Get the new reminder ID
            try:
                added_data = json.loads(added.content[0].text)
                new_id = added_data["reminder"]["id"]
            except (ValueError, KeyError, TypeError, AttributeError):
                print("Could not read reminder ID. Check ADD RESULT.")
                return

            print(f"\nNew reminder ID: {new_id}")

            # Step 3: List all reminders
            print("\nLISTING REMINDERS...")

            listed = await session.call_tool(
                "list_reminders",
                {},
            )

            print("\nLIST RESULT:")
            print(listed)

            # Step 4: Delete the reminder created by this test
            print(f"\nDELETING REMINDER ID {new_id}...")

            deleted = await session.call_tool(
                "delete_reminder",
                {"reminder_id": new_id},
            )

            print("\nDELETE RESULT:")
            print(deleted)

            # Step 5: List reminders after deletion
            print("\nCHECKING REMINDERS AFTER DELETE...")

            after_delete = await session.call_tool(
                "list_reminders",
                {},
            )

            print("\nLIST AFTER DELETE:")
            print(after_delete)


if __name__ == "__main__":
    asyncio.run(main())
