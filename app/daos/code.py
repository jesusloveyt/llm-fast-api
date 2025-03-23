from sqlalchemy import Update
from sqlalchemy.sql.functions import current_timestamp

from common.db.context import session_maker
from models.code import CodeModel


def get_list(useFlag:bool=True, schTxt:str=None, parentCode:str=None, listCount:int=None, skipCount:int=None)-> list[CodeModel]:
    with session_maker() as session:

        code_list_query = session.query(CodeModel).filter(CodeModel.useFlag == useFlag)
        if parentCode:
            code_list_query = code_list_query.filter(CodeModel.parentCode == parentCode)
        if schTxt:
            code_list_query = code_list_query.filter(
                CodeModel.code.like(f'%{schTxt}%') |
                CodeModel.parentCode.like(f'%{schTxt}%') |
                CodeModel.codeLabel.like(f'%{schTxt}%')
            )
        if skipCount:
            code_list_query = code_list_query.offset(skipCount)
        if listCount:
            code_list_query = code_list_query.limit(listCount)
        
        code_list = code_list_query.all()
        return code_list

def get_by_id(codeId:int)-> CodeModel:
    with session_maker() as session:
        code = session.query(CodeModel).filter(CodeModel.codeId == codeId).first()
        return code

def get_by_code_keys(parentCode:str, code:str)-> CodeModel:
    with session_maker() as session:
        code = session.query(CodeModel).filter(CodeModel.parentCode == parentCode, CodeModel.code == code, CodeModel.useFlag == True).first()
        return code

def insert(code: str, parentCode: str, codeLabel: str, memo: str, stringValue: str, numberValue:float)-> CodeModel:
    with session_maker.begin() as session:
        new_code = CodeModel()
        new_code.code = code
        new_code.parentCode = parentCode
        new_code.codeLabel = codeLabel
        new_code.memo = memo
        new_code.stringValue = stringValue
        new_code.numberValue = numberValue
        new_code.useFlag = True
        new_code.editedAt = current_timestamp()

        session.add(new_code)
        session.flush()
        session.refresh(new_code)
        return new_code

def update(codeId: int, codeLabel: str, memo: str, stringValue: str, numberValue:float) -> bool:
    with session_maker.begin() as session:
        update_values = {
            CodeModel.memo: memo,
            CodeModel.stringValue: stringValue,
            CodeModel.numberValue: numberValue,
            CodeModel.editedAt: current_timestamp()
        }

        if codeLabel is not None:
            update_values[CodeModel.codeLabel] = codeLabel

        session.execute(Update(CodeModel).where(CodeModel.codeId == codeId).values(update_values))
        return True

def delete_using_flag(codeId: int) -> bool:
    with session_maker.begin() as session:
        session.execute(Update(CodeModel)
                        .where(CodeModel.codeId == codeId)
                        .values({CodeModel.useFlag: False}))
        return True