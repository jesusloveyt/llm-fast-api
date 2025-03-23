from typing import Optional

from fastapi import Query
from pydantic import BaseModel

from dtos.base import BaseParam, BaseResult
from dtos.file import FileSchema


class NoticeSchema(BaseModel):
    noticeId: Optional[int] = 0
    noticeKind: str
    writerId: Optional[int] = None
    writerName: Optional[str] = None
    title: Optional[str] = None
    contents: Optional[str] = None


class NoticeResult(NoticeSchema, BaseResult):
    readCount: int = 0
    noticeKindTitle: Optional[str] = None
    mainImage: Optional[FileSchema] = None
    class Config:
        from_attributes = True


class NoticeParam(BaseParam):
    noticeKind: str = Query(None)


class NoticeForm(NoticeSchema):
    mainImage: Optional[FileSchema] = None