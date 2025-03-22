from daos import notice as notice_dao
from daos import file as file_dao

from models.notice import NoticeModel
from dtos.notice import NoticeResult, NoticeSchema

def get_notice_list(useFlag:bool=True, schTxt:str=None, noticeKind:str=None, listCount:int=None, skipCount:int=None)-> list[NoticeResult]:
    notice_list = notice_dao.get_list(useFlag=useFlag, schTxt=schTxt, noticeKind=noticeKind, listCount=listCount, skipCount=skipCount)
    notice_result_list = []
    for notice in notice_list:
        notice_data = NoticeResult.model_validate(notice)
        notice_data.mainImage = file_dao.get_by_link("noticeMainImage", notice.noticeId)
        notice_result_list.append(notice_data)
    return notice_result_list

def get_notice_by_id(noticeId:int)-> NoticeModel:
    notice = notice_dao.get_by_id(noticeId)
    notice_data = NoticeResult.model_validate(notice)
    notice_data.mainImage = file_dao.get_by_link("noticeMainImage", noticeId)
    return notice_data

def add_notice(noticeForm: NoticeSchema)-> NoticeModel:
    return notice_dao.insert(noticeForm.notice, noticeForm.parentNotice, noticeForm.noticeLabel, noticeForm.memo, noticeForm.stringValue, noticeForm.numberValue)

def update_notice(noticeForm: NoticeSchema)-> bool:
    return notice_dao.update(noticeForm.noticeId, noticeForm.noticeLabel, noticeForm.memo, noticeForm.stringValue, noticeForm.numberValue)
    
def delete_notice(noticeId:int)-> bool:
    return notice_dao.delete_using_flag(noticeId)