import aiosqlite
import asyncio
import os

DB_NAME = 'ALX_prodev'

async def async_fetch_users():
    db = await aiosqlite.connect(DB_NAME)
    cursor = await db.execute('SELECT * FROM users')
    rows = await cursor.fetchall()
    await cursor.close()
    await db.close()
    return rows


async def async_fetch_older_users():
    db = await aiosqlite.connect(DB_NAME)
    cursor = await db.execute('SELECT * FROM users WHERE age > 40')
    rows = await cursor.fetchall()
    await cursor.close()
    await db.close()
    return rows

async def fetch_concurrently():
    users, old_users = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    
asyncio.run(fetch_concurrently())
