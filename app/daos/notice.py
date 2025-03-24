from sqlalchemy import Update
from sqlalchemy.sql.functions import current_timestamp

from common.db.context import session_maker
from models.notice import NoticeModel


def get_list(useFlag:bool=True, schTxt:str=None, noticeKind:str=None, listCount:int=None, skipCount:int=None)-> list[NoticeModel]:
    with session_maker() as session:
        notice_list_query = session.query(NoticeModel).filter(NoticeModel.useFlag == useFlag)
        if noticeKind:
            notice_list_query = notice_list_query.filter(NoticeModel.noticeKind == noticeKind)
        if schTxt:
            notice_list_query = notice_list_query.filter(
                NoticeModel.title.like(f'%{schTxt}%') |
                NoticeModel.writerName.like(f'%{schTxt}%') |
                NoticeModel.contents.like(f'%{schTxt}%')
            )
        if skipCount:
            notice_list_query = notice_list_query.offset(skipCount)
        if listCount:
            notice_list_query = notice_list_query.limit(listCount)
        
        notice_list = notice_list_query.all()
        return notice_list

def get_by_id(noticeId:int)-> NoticeModel:
    with session_maker() as session:
        notice = session.query(NoticeModel).filter(NoticeModel.noticeId == noticeId).first()
        return notice

def insert(noticeKind: str, writerId: int, writerName: str, title: str, contents: str)-> NoticeModel:
    with session_maker.begin() as session:
        new_notice = NoticeModel()
        new_notice.noticeKind = noticeKind
        new_notice.writerId = writerId
        new_notice.writerName = writerName
        new_notice.title = title
        new_notice.contents = contents
        new_notice.readCount = 0
        new_notice.useFlag = True
        new_notice.createdAt = current_timestamp()
        new_notice.updatedAt = current_timestamp()

        session.add(new_notice)
        session.flush()
        session.refresh(new_notice)
        return new_notice

def update(noticeId: int, noticeKind: str, writerId: int, writerName: str, title: str, contents: str) -> bool:
    with session_maker.begin() as session:
        update_values = {
            NoticeModel.writerId: writerId,
            NoticeModel.writerName: writerName,
            NoticeModel.title: title,
            NoticeModel.contents: contents,
            NoticeModel.updatedAt: current_timestamp()
        }

        if noticeKind is not None:
            update_values[NoticeModel.noticeKind] = noticeKind

        session.execute(Update(NoticeModel).where(NoticeModel.noticeId == noticeId).values(update_values))
        return True

def delete_using_flag(noticeId: int) -> bool:
    with session_maker.begin() as session:
        session.execute(Update(NoticeModel)
                        .where(NoticeModel.noticeId == noticeId)
                        .values({NoticeModel.useFlag: False}))
        return True