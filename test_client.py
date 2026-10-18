
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

            # Add a sample reminder
            added = await session.call_tool(
                "add_reminder",
                {
                    "task": "Take medicine",
                    "time": "8:00 PM",
                },
            )
            print("Add reminder result:")
            print(added)

            # List all reminders
            listed = await session.call_tool("list_reminders", {})
            print("\nList reminders result:")
            print(listed)


if __name__ == "__main__":
    asyncio.run(main())

