import os
import base64
import uuid

from common.util.aws_s3 import upload_file_on_s3
from daos import file as file_dao

from models.file import FileModel
from dtos.file import FileForm, FileSchema


def get_file_list(schTxt:str=None, linkInfo:str=None, listCount:int=None, skipCount:int=None)-> list[FileModel]:
    return file_dao.get_list(schTxt=schTxt, linkInfo=linkInfo, listCount=listCount, skipCount=skipCount)

def get_file_by_id(fileId:int)-> FileModel:
    return file_dao.get_by_id(fileId)

def upload_file(fileForm: FileForm)-> FileModel:
    if fileForm.fileUrl:
        fileForm.linkInfo = "direct" if fileForm.linkInfo is None else fileForm.linkInfo
        fileForm.linkKey = 0 if fileForm.linkKey is None else fileForm.linkKey
        fileForm.fileSize = 0 if fileForm.fileSize is None else fileForm.fileSize

        return file_dao.insert(fileForm.linkInfo, fileForm.linkKey, fileForm.realName, fileForm.fileUrl, fileForm.fileSize)
    
    if fileForm.base64String:
        file_bytes = base64.b64decode(fileForm.base64String)
        if not file_bytes:
            return None

        file_real_name = fileForm.realName
        if file_real_name:
            file_real_name = file_real_name.replace("C:\\fakepath", "").replace("C:fakepath", "")
            fidx = file_real_name.rfind(os.sep)
            if fidx > 0:
                file_real_name = file_real_name[fidx + 1:]
        else:
            file_real_name = "file"

        extension = ""
        fidx = file_real_name.rfind(".")
        if fidx > 0:
            extension = file_real_name[fidx + 1:].lower()

        # contentType = f"image/{extension}" if extension in ["png", "jpg", "gif", "bmp"] else "application/octet-stream"

        file_saved_name = str(uuid.uuid4()) # str(int(time.time()))
        if extension:
            file_saved_name = f"{file_saved_name}.{extension}"
        
        fileForm.fileSize = len(file_bytes)
        fileForm.fileUrl = upload_file_on_s3(file_saved_name, file_bytes)

        return file_dao.insert(fileForm.linkInfo, fileForm.linkKey, fileForm.realName, fileForm.fileUrl, fileForm.fileSize)
    
    return None

def delete_file(fileId: int)-> bool:
    return file_dao.delete(fileId)

def add_file(fileForm: FileSchema)-> FileModel:
    return file_dao.insert(fileForm.linkInfo, fileForm.linkKey, fileForm.realName, fileForm.fileUrl, fileForm.fileSize)