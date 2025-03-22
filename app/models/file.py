from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql.functions import current_timestamp

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class FileModel(Base):
    __tablename__ = 'tb_file'
    fileId = Column("file_id", Integer(), primary_key=True, autoincrement=True)
    linkInfo = Column("link_info", String(30))
    linkKey = Column("link_key", Integer())
    realName = Column("real_name", String(120))
    fileUrl = Column("file_url", String(120))
    fileSize = Column("file_size", Integer())
    savedAt = Column("saved_at", DateTime(), default=current_timestamp())
    deletedAt = Column("deleted_at", DateTime())