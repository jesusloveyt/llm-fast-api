from typing import Optional

from fastapi import Query
from pydantic import BaseModel

from dtos.base import BaseParam, BaseResult
from dtos.file import FileSchema


class AccountSchema(BaseModel):
    accountId: Optional[int] = 0
    joinType: str
    accountKey: Optional[str] = None
    snsKey: Optional[str] = None
    userName: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    postcode: Optional[str] = None
    address: Optional[str] = None
    addressDetail: Optional[str] = None
    role: Optional[str] = None
    level: Optional[str] = None


class AccountResult(AccountSchema, BaseResult):
    profileImage: Optional[FileSchema] = None
    class Config:
        from_attributes = True


class AccountParam(BaseParam):
    joinType: str = Query(None)


class AccountForm(AccountSchema):
    password: Optional[str] = None
    fcmToken: Optional[str] = None
    refreshToken: Optional[str] = None
    profileImage: Optional[FileSchema] = None

    # loginAt = Column("login_at", DateTime())
    # passwordAt = Column("password_at", DateTime())