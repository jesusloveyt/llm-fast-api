from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FileSchema(BaseModel):
    fileId: Optional[int] = 0
    linkInfo: str
    linkKey: int
    realName: Optional[str] = None
    fileUrl: Optional[str] = None
    fileSize: Optional[int] = None


class FileResult(FileSchema):
    savedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class FileForm(BaseModel):
    fileId: Optional[int] = 0
    linkInfo: Optional[str] = None
    realName: str
    fileUrl: Optional[str] = None
    base64String: Optional[str] = None
