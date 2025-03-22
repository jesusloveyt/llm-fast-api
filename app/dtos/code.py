from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel

from dtos.base import BaseParam


class CodeSchema(BaseModel):
    codeId: Optional[int] = 0
    code: str
    parentCode: str
    codeLabel: str
    memo: Optional[str] = None
    stringValue: Optional[str] = None
    numberValue: Optional[float] = None


class CodeResult(CodeSchema):
    useFlag: bool
    editedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }


class CodeParam(BaseParam):
    code: str = Query(None)
    parentCode: str = Query(None)

