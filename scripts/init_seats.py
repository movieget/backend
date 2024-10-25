import asyncio
from src.core.configs.seat_layouts import screen_rules
from src.app.v1.screen.service.seat_service import generate_seat_layout_by_rules
from src.core.database.connection import init_db
from tortoise import Tortoise


async def init_seats():
    await init_db()  # 데이터베이스 연결 초기화

    # 좌석 생성 작업을 순차적으로 수행
    for screen_id, rules in screen_rules.items():
        await generate_seat_layout_by_rules(screen_id=screen_id, rules=rules)

    print("All seat layouts initialized in the database.")
    await Tortoise.close_connections()  # 모든 작업이 끝난 후 데이터베이스 연결 닫기


# 스크립트 실행
if __name__ == "__main__":
    asyncio.run(init_seats())
