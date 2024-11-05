import asyncio
from src.core.configs.seat_layouts import screen_rules
from src.app.v1.screen.service.seat_service import generate_seat_layout_by_rules
from src.core.database.connection import database_initialize
from tortoise import Tortoise

from src.main import app


async def init_seats():
    await database_initialize(app)

    for screen_id, rules in screen_rules.items():
        print(f"Initializing seats for screen {screen_id}")

        await generate_seat_layout_by_rules(screen_id=screen_id, rules=rules)

    print("All seat layouts initialized in the database.")
    await Tortoise.close_connections()

# 스크립트 실행
if __name__ == "__main__":
    asyncio.run(init_seats())
