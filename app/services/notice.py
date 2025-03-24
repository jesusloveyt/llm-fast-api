from daos import notice as notice_dao
from daos import file as file_dao

from models.notice import NoticeModel
from dtos.notice import NoticeForm, NoticeResult, NoticeSchema

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
    if not notice:
        return None
    notice_data = NoticeResult.model_validate(notice)
    notice_data.mainImage = file_dao.get_by_link("noticeMainImage", noticeId)
    return notice_data

def add_notice(noticeForm: NoticeForm)-> NoticeModel:
    notice = notice_dao.insert(noticeForm.noticeKind, noticeForm.writerId, noticeForm.writerName, noticeForm.title, noticeForm.contents)
    if not notice:
        return None
    if noticeForm.mainImage:
        file_dao.insert("noticeMainImage", noticeForm.noticeId, noticeForm.mainImage.realName, noticeForm.mainImage.fileUrl, noticeForm.mainImage.fileSize)
    return notice

def update_notice(noticeForm: NoticeForm)-> bool:
    notice_dao.update(noticeForm.noticeId, noticeForm.noticeKind, noticeForm.writerId, noticeForm.writerName, noticeForm.title, noticeForm.contents)
    if noticeForm.mainImage:
        fileId = noticeForm.mainImage.fileId
        if not fileId or fileId == 0:
            file_dao.delete_using_flag(linkInfo="noticeMainImage", linkKey=noticeForm.noticeId)
        
        if noticeForm.mainImage.realName and noticeForm.mainImage.fileUrl:
            file_dao.insert("noticeMainImage", noticeForm.noticeId, noticeForm.mainImage.realName, noticeForm.mainImage.fileUrl, noticeForm.mainImage.fileSize)
    else:
        file_dao.delete_using_flag(linkInfo="noticeMainImage", linkKey=noticeForm.noticeId)

    return True

def delete_notice(noticeId: int)-> bool:
    return notice_dao.delete_using_flag(noticeId)