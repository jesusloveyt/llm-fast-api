from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.sql.functions import current_timestamp

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class AccountModel(Base):
    __tablename__ = 'tb_account'
    accountId = Column("account_id", Integer(), primary_key=True, autoincrement=True)
    joinType = Column("join_type", String(10))
    accountKey = Column("account_key", String(30))
    password = Column("password", String(256))
    snsKey = Column("sns_key", String(60))
    userName = Column("user_name", String(30))
    phone = Column("phone", String(20))
    email = Column("email", String(100))
    # language String(12)
    postcode = Column("postcode", String(6))
    address = Column("address", String(60))
    # addressRegion = Column("address_region", String(60))
    addressDetail = Column("address_detail", String(60))
    latitude = Column("latitude", Float())
    longitude = Column("longitude", Float())
    role = Column("role", String(30))
    level = Column("level", String(30))
    fcmToken = Column("fcm_token", String(256))
    # webSocketKey = Column("web_socket_key", String(120))
    refreshToken = Column("refresh_token", String(140))
    useFlag = Column("use_fg", Boolean)
    # approved = Column("approved", Boolean)
    createdAt = Column("created_at", DateTime(), default=current_timestamp())
    updatedAt = Column("updated_at", DateTime(), default=current_timestamp())
    loginAt = Column("login_at", DateTime())
    passwordAt = Column("password_at", DateTime())