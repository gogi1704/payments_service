import aiosqlite

DB_PATH = "payments.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_id TEXT UNIQUE,
            user_id INTEGER,
            amount REAL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            paid_at TIMESTAMP
        )
        """)
        await db.commit()

async def is_already_processed(payment_id: str, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT status FROM payments WHERE payment_id = ?
        """, (payment_id,))
        row = await cursor.fetchone()

        if not row:
            return False

        return row[0] == status