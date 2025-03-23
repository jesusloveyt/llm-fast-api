from sqlalchemy import Delete, Update
from sqlalchemy.sql.functions import current_timestamp

from common.db.context import session_maker
from models.file import FileModel


def get_list(schTxt:str=None, linkInfo:str=None, listCount:int=None, skipCount:int=None)-> list[FileModel]:
    with session_maker() as session:

        file_list_query = session.query(FileModel)
        if linkInfo:
            file_list_query = file_list_query.filter(FileModel.linkInfo == linkInfo)
        if schTxt:
            file_list_query = file_list_query.filter(
                FileModel.realName.like(f'%{schTxt}%') |
                FileModel.fileUrl.like(f'%{schTxt}%')
            )
        if skipCount:
            file_list_query = file_list_query.offset(skipCount)
        if listCount:
            file_list_query = file_list_query.limit(listCount)
        
        file_list = file_list_query.all()
        return file_list


def get_by_id(fileId:int)-> FileModel:
    with session_maker() as session:
        file = session.query(FileModel).filter(FileModel.fileId == fileId).first()
        return file


def get_list_by_link(linkInfo:str, linkKey:int)-> list[FileModel]:
    with session_maker() as session:
        file_list_query = session.query(FileModel).filter(
            FileModel.linkInfo == linkInfo,
            FileModel.linkKey == linkKey
            )        
        file_list = file_list_query.all()
        return file_list


def get_by_link(linkInfo:str, linkKey:int)-> FileModel:
    with session_maker() as session:
        file_list_query = session.query(FileModel).filter(
            FileModel.linkInfo == linkInfo,
            FileModel.linkKey == linkKey
            )        
        file = file_list_query.first()
        return file


def insert(linkInfo: str, linkKey: int, realName: str, fileUrl: str, fileSize:int)-> FileModel:
    with session_maker.begin() as session:
        new_file = FileModel()
        new_file.linkInfo = linkInfo
        new_file.linkKey = linkKey
        new_file.realName = realName
        new_file.fileUrl = fileUrl
        new_file.fileSize = fileSize
        new_file.savedAt = current_timestamp()

        session.add(new_file)
        session.flush()
        session.refresh(new_file)
        return new_file

def delete_using_flag(linkInfo: str=None, linkKey: int=0, fileId: int=0) -> bool:
    with session_maker.begin() as session:
        if linkInfo and linkKey > 0:
            session.execute(Update(FileModel)
                        .where(FileModel.linkInfo == linkInfo)
                        .where(FileModel.linkKey == linkKey)
                        .values({FileModel.deletedAt: current_timestamp()}))
        elif fileId and fileId > 0:
            session.execute(Update(FileModel)
                        .where(FileModel.fileId == fileId)
                        .values({FileModel.deletedAt: current_timestamp()}))
        else:
            return False
        return True

def delete(fileId: int) -> bool:
    with session_maker.begin() as session:
        session.execute(Delete(FileModel).where(FileModel.fileId == fileId))
        return True
