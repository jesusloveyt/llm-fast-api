from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FileSchema(BaseModel):
    fileId: Optional[int] = 0
    linkInfo: Optional[str] = None
    linkKey: Optional[int] = None
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

class FileForm(FileSchema):
    base64String: Optional[str] = None
