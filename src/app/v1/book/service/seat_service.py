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


# 트랜잭션 블록 사용:
#
# in_transaction()을 사용하여 트랜잭션 내에서 좌석 상태 확인과 업데이트가 모두 이루어집니다. 트랜잭션이 완료되기 전까지는 좌석 상태를 다른 트랜잭션이 변경하지 못하도록 잠금 처리(for_update())를 사용합니다.
# 좌석 상태 확인:
#
# Seat.filter(id__in=seat_ids).for_update().all()은 트랜잭션 내에서 좌석을 잠금 처리하여, 다른 요청이 동시에 이 좌석을 선택하지 못하도록 합니다. 이 방식은 동시성 문제를 방지합니다.
# 중복 예약 방지:
#
# 좌석이 이미 예약되었는지 확인한 후, 예약이 가능한 좌석만 업데이트합니다. 하나라도 이미 예약된 좌석이 있다면 예외를 발생시킵니다.
# 좌석 업데이트:
#
# 좌석들이 모두 예약 가능할 경우, Seat.filter(id__in=seat_ids).update(is_selected=True)을 사용해 한꺼번에 좌석 상태를 업데이트합니다. 이 방식은 개별적으로 업데이트하는 것보다 효율적입니다.
# 트랜잭션 커밋:
#
# 모든 작업이 완료되면 트랜잭션을 커밋하여 좌석 상태 변경과 예약 정보가 실제로 데이터베이스에 반영됩니다. 만약 중간에 문제가 발생하면 트랜잭션은 자동으로 롤백됩니다.
# 결론:
# 동시성 문제 해결: 트랜잭션 내에서 좌석 상태를 확인하고 동시에 다른 사용자가 같은 좌석을 선택하지 못하게 잠금 처리합니다.
# 성능 최적화: 좌석 상태를 한꺼번에 확인하고 업데이트하여, 반복적인 데이터베이스 접근을 최소화합니다.
# 안정성: 트랜잭션을 통해 모든 작업이 원자적으로 처리되며, 중복 예약을 방지할 수 있습니다.
# 이 코드는 실시간 좌석 선택 및 예약 중 다른 사용자의 중복 예약을 방지하는 데 적합합니다.