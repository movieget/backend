from src.app.v1.screen.entity.seat import Seat
import asyncio

async def generate_seat_layout_by_rules(screen_id: int, rules: dict):
    rows = rules["rows"]
    seats_per_row = rules["seats_per_row"]
    skip_seats_per_row = rules.get("skip_seats_per_row", {})

    # 리스트 컴프리헨션을 사용해 좌석을 비동기적으로 생성하고 저장
    tasks = [
        Seat.create(
            screen_id=screen_id,
            seat_number=seat_number + 1,
            is_selected=False,
            row=row,
            column=seat_number + 1
        )
        for row in rows
        for seat_number in range(seats_per_row)
        if seat_number not in skip_seats_per_row.get(row, [])
    ]

    # 모든 좌석 생성 작업을 비동기적으로 수행
    await asyncio.gather(*tasks)
