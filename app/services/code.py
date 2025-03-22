from daos import code as code_dao

from models.code import CodeModel
from dtos.code import CodeSchema

def get_code_list(useFlag:bool=True, schTxt:str=None, parentCode:str=None, listCount:int=None, skipCount:int=None)-> list[CodeModel]:
    return code_dao.get_list(useFlag=useFlag, schTxt=schTxt, parentCode=parentCode, listCount=listCount, skipCount=skipCount)

def get_code_by_id(codeId:int)-> CodeModel:
    return code_dao.get_by_id(codeId)

def add_code(codeForm: CodeSchema)-> CodeModel:
    return code_dao.insert(codeForm.code, codeForm.parentCode, codeForm.codeLabel, codeForm.memo, codeForm.stringValue, codeForm.numberValue)

def update_code(codeForm: CodeSchema)-> bool:
    return code_dao.update(codeForm.codeId, codeForm.codeLabel, codeForm.memo, codeForm.stringValue, codeForm.numberValue)
    
def delete_code(codeId: int)-> bool:
    return code_dao.delete_using_flag(codeId)