import aiosqlite
from db.database import DB_PATH


async def create_payment_record(payment_id: str, user_id: int, amount: float, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO payments (payment_id, user_id, amount, status)
            VALUES (?, ?, ?, ?)
        """, (payment_id, user_id, amount, status))
        await db.commit()


async def get_payment(payment_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT payment_id, user_id, amount, status
            FROM payments
            WHERE payment_id = ?
        """, (payment_id,))
        return await cursor.fetchone()


async def update_payment_status(payment_id: str, status: str, paid_at=None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE payments
            SET status = ?, paid_at = ?
            WHERE payment_id = ?
        """, (status, paid_at, payment_id))
        await db.commit()