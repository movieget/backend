from tortoise.expressions import Q
from datetime import date, time
from src.app.v1.screen.entity.screen_info import ScreenInfo


class ScreenInfoRepository:
    async def get_screen_info_id(self, screen_id: int, screening_date: date, start_time: time) -> int:
        return await ScreenInfo.get_or_none(Q(screen_id=screen_id) & Q(screening_date=screening_date) & Q(start_time=start_time))
