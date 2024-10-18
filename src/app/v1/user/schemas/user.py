from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from entity.accounts import BankNum, AccountType


# Default Account
class AccountBase(BaseModel):
    account_number: str
    bank_num: BankNum
    account_number: AccountType
    balance: Decimal = Field(decimal_places=2, ge=Decimal("0"))


# Account Create
class AccountCreate(AccountBase):
    user_id: int


# Account Update
class AccountUpdate(BaseModel):
    account_number: str | None = None
    bank_num: BankNum | None = None
    account_type: AccountType | None = None
    balance: Decimal | None = Field(decimal_places=2, ge=Decimal("0"))


# 데이터베이스에서 반환된 Account를 위한 스키마
class Account(AccountBase):
    model_config = ConfigDict(from_attributes=True)
    account_id: int
    user_id: int


# Account의 공개 정보 (필요한 경우)
class AccountPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    account_id: int
    account_number: str
    bank_num: BankNum
    account_type: AccountType
