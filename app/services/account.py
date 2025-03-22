from daos import account as account_dao
from daos import file as file_dao

from models.account import AccountModel
from dtos.account import AccountResult, AccountForm

def get_account_list(useFlag:bool=True, schTxt:str=None, joinType:str=None, listCount:int=None, skipCount:int=None)-> list[AccountResult]:
    account_list = account_dao.query_list(useFlag=useFlag, schTxt=schTxt, joinType=joinType, listCount=listCount, skipCount=skipCount)
    return account_list

def get_account_by_id(accountId:int)-> AccountModel:
    account = account_dao.get_by_id(accountId)
    account_data = AccountResult.model_validate(account)
    account_data.profileImage = file_dao.get_by_link("accountProfileImage", accountId)
    return account_data

def add_account(accountForm: AccountForm)-> AccountModel:
    return account_dao.insert(accountForm.joinType, accountForm.accountKey,  accountForm.password, accountForm.snsKey, 
                              accountForm.userName, accountForm.phone, accountForm.email, 
                              accountForm.postcode,  accountForm.address, accountForm.addressDetail, 
                              accountForm.role, accountForm.fcmToken, accountForm.refreshToken)

def update_account(accountForm: AccountForm)-> bool:
    return account_dao.update(accountForm.accountId, accountForm.joinType,
                              accountForm.userName, accountForm.phone, accountForm.email, 
                              accountForm.postcode,  accountForm.address, accountForm.addressDetail, 
                              accountForm.role, accountForm.fcmToken, accountForm.refreshToken)

def delete_account(accountId:int)-> bool:
    return account_dao.delete_using_flag(accountId)