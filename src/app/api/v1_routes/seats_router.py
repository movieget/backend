# src/app/v1/screen/api/seat_routes.py
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict
from src.app.v1.screen.entity.seat import Seat
from src.app.v1.book.schemas.book import SeatLayoutResponse, Row, SeatResponse
# from src.app.v1.user.dependencies import get_current_user
# from src.app.v1.user.entity.user import User

router = APIRouter()

@router.get("/{screen_id}", response_model=SeatLayoutResponse)
async def get_seat_layout(screen_id: int, user_id: int =Query(...)):
# async def get_seat_layout(screen_id: int, user: User = Depends(get_current_user)):
    seats = await Seat.filter(screen_id=screen_id).order_by("row", "column").all()

    if not seats:
        raise HTTPException(status_code=404, detail="지정한 화면 ID에 대한 좌석을 찾을 수 없습니다.")

    # 열(row)별로 좌석을 그룹화하여 배열 구성
    row_layout: Dict[str, List[SeatResponse]] = {}
    for seat in seats:
        seat_data = SeatResponse(
            seat_number=seat.seat_number,
            is_selected=seat.is_selected,
            row=seat.row,
            column=seat.column
        )
        if seat.row not in row_layout:
            row_layout[seat.row] = []
        row_layout[seat.row].append(seat_data)

    # 최종 좌석 배열을 반환할 형식으로 구성
    seat_layout = SeatLayoutResponse(
        screen_id=screen_id,
        rows=[Row(row=row, seats=seats) for row, seats in row_layout.items()]
    )

    return seat_layout
