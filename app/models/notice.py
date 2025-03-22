from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.sql.functions import current_timestamp

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class NoticeModel(Base):
    __tablename__ = 'tb_notice'
    noticeId = Column("notice_id", Integer(), primary_key=True, autoincrement=True)
    noticeKind = Column("notice_kind", String(20))
    writerId = Column("writer_id", Integer())
    writerName = Column("writer_name", String(30))
    title = Column("title", String(90))
    contents = Column("contents", String(5000))
    readCount = Column("read_count", Integer())
    useFlag = Column("use_fg", Boolean)
    createdAt = Column("created_at", DateTime(), default=current_timestamp())
    updatedAt = Column("updated_at", DateTime(), default=current_timestamp())