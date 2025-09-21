import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users (async):")
            for row in results:
                print(row)
            return results

async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("Users older than 40 (async):")
            for row in results:
                print(row)
            return results

async def fetch_concurrently():
    # Execute both queries concurrently
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Run the async functions
if __name__ == "__main__":
    results = asyncio.run(fetch_concurrently())
    print("Concurrent fetch completed!")