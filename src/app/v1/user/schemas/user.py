from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

from pydantic import BaseModel, Field

# from entity.accounts import BankNum, AccountType

#
# # Default Account
# class AccountBase(BaseModel):
#     account_number: str
#     bank_num: BankNum
#     account_number: AccountType
#     balance: Decimal = Field(decimal_places=2, ge=Decimal("0"))
#
#
# # Account Create
# class AccountCreate(AccountBase):
#     user_id: int
#
#
# # Account Update
# class AccountUpdate(BaseModel):
#     account_number: str | None = None
#     bank_num: BankNum | None = None
#     account_type: AccountType | None = None
#     balance: Decimal | None = Field(decimal_places=2, ge=Decimal("0"))
#
#
# # 데이터베이스에서 반환된 Account를 위한 스키마
# class Account(AccountBase):
#     model_config = ConfigDict(from_attributes=True)
#     account_id: int
#     user_id: int
#
#
# # Account의 공개 정보 (필요한 경우)
# class AccountPublic(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     account_id: int
#     account_number: str
#     bank_num: BankNum
#     account_type: AccountType


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    nickname: str
    birthday: str = ""
    phone_number: str = ""
    oauth_provider: str
    image_url: str = ""

    # 추가적인 필드를 여기에 추가할 수 있습니다.

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    nickname: Optional[str] = Field(None, description="사용자 닉네임")
    phone_number: Optional[str] = Field(None, description="전화번호")
    birthday: Optional[str] = Field(None, description="생일")
    image_url: Optional[str] = Field(None, description="프로필 이미지 URL")
    email: Optional[EmailStr] = Field(None, description="이메일 주소")
