import asyncio
import aiosqlite


# Setup function to prepare demo database
async def setup_demo_data():
    async with aiosqlite.connect("example.db") as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """
        )
        await db.execute("DELETE FROM users")  # Clear table before inserting
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [("Alice", 25), ("Bob", 45), ("Charlie", 35), ("Diana", 60), ("Eve", 22)],
        )
        await db.commit()


# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All Users:")
            for user in users:
                print(user)
            return users


# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in users:
                print(user)
            return users


# Run both queries concurrently
async def fetch_concurrently():
    await setup_demo_data()
    await asyncio.gather(async_fetch_users(), async_fetch_older_users())


# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
