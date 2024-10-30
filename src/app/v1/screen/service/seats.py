from fastapi import HTTPException
from tortoise.transactions import in_transaction
from typing import List

from src.app.v1.book.repository import book_repository
from src.app.v1.screen.entity.seat import Seat


# 좌석 상태 확인
async def check_seat_availability(screen_info_id: int):
    available_seats, reserved_seats = await book_repository.get_seat_availability(screen_info_id)
    if not available_seats and not reserved_seats:
        raise HTTPException(status_code=404, detail="No seats found for the selected screen info.")
    return {"available_seats": available_seats, "reserved_seats": reserved_seats}


# 좌석 예약 처리
async def reserve_seats(seat_ids: List[int], book_id: int):
    async with in_transaction() as transaction:
        # 좌석들이 이미 예약되어 있는지 확인
        seats = await Seat.filter(id__in=seat_ids).for_update().all()  # 트랜잭션 내에서 좌석을 잠금

        for seat in seats:
            if seat.is_selected:
                raise HTTPException(status_code=400, detail=f"{seat.id} 이미 예약 되었습니다.")

        # 좌석 예약 처리 (모두 예약 가능할 경우)
        await Seat.filter(id__in=seat_ids).update(is_selected=True)

        # 예약 정보를 업데이트
        await book_repository.reserve_seats(book_id, seat_ids)

        # 트랜잭션 커밋
        await transaction.commit()
