import asyncio

from src.app.v1.user.entity.user import User


async def schedule_account_deletion(id: int):
    # 7일 후에 사용자 정보 삭제
    await asyncio.sleep(60 * 60 * 24 * 7)   # 7일을 초 로 변환
    await delete_user_from_db(id)


async def delete_user_from_db(id: int):
    user = await User.get(id=id)
    if user:
        await user.delete()
