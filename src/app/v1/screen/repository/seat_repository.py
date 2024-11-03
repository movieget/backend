# from typing import List
# from tortoise.exceptions import DoesNotExist
# from src.app.v1.screen.entity.seat import Seat
# from src.app.v1.screen.entity.screen import Screen
# from src.common.handlers.exception_handler import BusinessException, ErrorCode


# class SeatRepository:

#     async def check_seats_existence(self, screen_number: str, seat_numbers: List[str]) -> List[str]:
#         non_existent_seats = []
#         try:
#             screen = await Screen.get(screen_number=screen_number)
#             for seat_number in seat_numbers:
#                 row = seat_number[0]
#                 column = int(seat_number[1:])
#                 seat = await Seat.get_or_none(screen_id=screen.id, row=row, column=column)
#                 if not seat:
#                     non_existent_seats.append(seat_number)
#         except DoesNotExist:
#             raise BusinessException(ErrorCode.NOT_FOUND, detail=f"Screen number {screen_number} does not exist")
#         return non_existent_seats

#     async def update_seats_selection(self, screen_number: int, seat_numbers: List[str]):
#         updated_seats = []
#         errors = []

#         for seat_number in seat_numbers:
#             row = seat_number[0]
#             column = int(seat_number[1:])

#             try:
#                 seat = await Seat.get(screen__number=screen_number, row=row, column=column)
#                 seat.is_selected = True
#                 await seat.save()
#                 updated_seats.append(seat)
#             except DoesNotExist:
#                 errors.append(f"Seat {seat_number} in screen {screen_number} does not exist")

#         return updated_seats, errors

#     async def get_seats_by_screen_and_numbers(self, screen_number: int, seat_numbers: List[str]):
#         seats = []
#         for seat_number in seat_numbers:
#             row = seat_number[0]
#             column = int(seat_number[1:])
#             seat = await Seat.get_or_none(screen__number=screen_number, row=row, column=column)
#             if seat:
#                 seats.append(seat)
#         return seats
