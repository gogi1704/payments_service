import asyncio
import aiosqlite
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

BASE_DIR = Path(__file__).resolve().parents[1]
CREDS_PATH = BASE_DIR / "docs" / "anamnez-max-a04dd6899274.json"

DB_PATH = "payments.db"
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SPREADSHEET_NAME = "anamnez_db_max"


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
            paid_at TIMESTAMP,
            notify_send BOOLEAN DEFAULT 0
        )
        """)
        await db.commit()

def get_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME)
    return {
        "payments": sheet.worksheet("payments"),
    }

async def sync_from_google_sheets():
    sheets = get_sheet()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM payments")

        rows = sheets["payments"].get_all_values()[1:]
        for r in rows:
            id, payment_id, user_id, amount, status, created_at, paid_at, notify_send = r
            await db.execute(
                "INSERT INTO payments (id, payment_id, user_id, status, amount, created_at, paid_at, notify_send ) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (int(id), payment_id, user_id, status, amount, created_at, paid_at, notify_send )
            )

        await db.commit()
    print("[✅] Данные из Google Sheets payments загружены в SQLite")


async def sync_to_google_sheets():
    sheets = get_sheet()

    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
            SELECT
                id,
                payment_id,
                user_id,
                status,
                amount,
                created_at,
                paid_at,
                notify_send
            FROM payments
        """) as cur:
            rows = await cur.fetchall()

    sheets["payments"].clear()

    sheets["payments"].update(
        "A1",
        [
            ["id", "payment_id", "user_id", "status", "amount", "created_at", "paid_at", "notify_send"]
        ] + rows
    )

    print("[✅] Данные ANAMNEZ_DB выгружены в Google Sheets")
async def periodic_sync(interval: int = 60):
    while True:
        await asyncio.sleep(interval)
        try:
            await sync_to_google_sheets()
            print(f"Успешно выгрузил в гугл")
        except Exception as e:
            print(f"Ошибка при синхронизации в Google Sheets: {e}")


async def is_already_processed(payment_id: str, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT status FROM payments WHERE payment_id = ?
        """, (payment_id,))
        row = await cursor.fetchone()

        if not row:
            return False

        return row[0] == status

async def set_payment_notified(payment_id: str):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute("""
            UPDATE payments
            SET notify_send = 1
            WHERE payment_id = ?
        """, (payment_id,))

        await db.commit()
