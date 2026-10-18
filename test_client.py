

import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Add a reminder
            added = await session.call_tool(
                "add_reminder",
                {"task": "Test reminder", "time": "9:00 PM"},
            )
            print("ADD RESULT:")
            print(added)

            # List reminders
            listed = await session.call_tool("list_reminders", {})
            print("\nLIST RESULT:")
            print(listed)

            # Delete reminder ID 3 (change this if your new ID differs)
            deleted = await session.call_tool(
                "delete_reminder",
                {"reminder_id": 3},
            )
            print("\nDELETE RESULT:")
            print(deleted)

            # List reminders again
            after_delete = await session.call_tool("list_reminders", {})
            print("\nLIST AFTER DELETE:")
            print(after_delete)


if __name__ == "__main__":
    asyncio.run(main())
