from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class BaseResult:
    useFlag: bool
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }


class BaseParam(BaseModel):
    useFlag: bool = Field(True)
    schTxt: str = Field(None)
    listCount: int = Field(..., gt=0)
    skipCount: int = Field(0, ge=0)    