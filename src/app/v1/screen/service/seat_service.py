from src.app.v1.screen.entity.seat import Seat
import asyncio


from src.app.v1.screen.entity.seat import Seat
import asyncio

async def generate_seat_layout_by_rules(screen_id: int, rules: dict):
    rows = rules["rows"]
    seats_per_row = rules["seats_per_row"]
    skip_seats_per_row = rules.get("skip_seats_per_row", {})

    tasks = []
    for row in rows:
        for seat_number in range(seats_per_row):
            if seat_number not in skip_seats_per_row.get(row, []):

                tasks.append(
                    Seat.create(
                        screen_id=screen_id,
                        seat_number=seat_number + 1,
                        is_selected=False,
                        row=row,
                        column=seat_number + 1
                    )
                )

    await asyncio.gather(*tasks)
