from daos import account as account_dao
from daos import file as file_dao

from models.account import AccountModel
from dtos.account import AccountResult, AccountForm

def query_account_list(useFlag:bool=True, schTxt:str=None, joinType:str=None, listCount:int=None, skipCount:int=None)-> list[AccountResult]:
    return account_dao.query_list(useFlag=useFlag, schTxt=schTxt, joinType=joinType, listCount=listCount, skipCount=skipCount)

def get_account_by_id(accountId:int)-> AccountModel:
    account = account_dao.get_by_id(accountId)
    if not account:
        return None
    account_data = AccountResult.model_validate(account)
    account_data.profileImage = file_dao.get_by_link("accountProfileImage", accountId)
    return account_data

def add_account(accountForm: AccountForm)-> AccountModel:
    account = account_dao.insert(accountForm.joinType, accountForm.accountKey,  accountForm.password, accountForm.snsKey, 
                                 accountForm.userName, accountForm.phone, accountForm.email, 
                                 accountForm.postcode,  accountForm.address, accountForm.addressDetail, 
                                 accountForm.role, accountForm.fcmToken, accountForm.refreshToken)
    if not account:
        return None
    if accountForm.profileImage:
        file_dao.insert("accountProfileImage", account.accountId, accountForm.profileImage.realName, accountForm.profileImage.fileUrl, accountForm.profileImage.fileSize)
    return account

def update_account(accountForm: AccountForm)-> bool:
    account_dao.update(accountForm.accountId, accountForm.joinType,
                       accountForm.userName, accountForm.phone, accountForm.email, 
                       accountForm.postcode,  accountForm.address, accountForm.addressDetail, 
                       accountForm.role, accountForm.fcmToken, accountForm.refreshToken)
    if accountForm.profileImage:
        fileId = accountForm.profileImage.fileId
        if not fileId or fileId == 0:
            file_dao.delete_using_flag(linkInfo="accountProfileImage", linkKey=accountForm.accountId)
        
        if accountForm.profileImage.realName and accountForm.profileImage.fileUrl:
            file_dao.insert("accountProfileImage", accountForm.accountId, accountForm.profileImage.realName, accountForm.profileImage.fileUrl, accountForm.profileImage.fileSize)
    else:
        file_dao.delete_using_flag(linkInfo="accountProfileImage", linkKey=accountForm.accountId)

    return True

def delete_account(accountId: int)-> bool:
    return account_dao.delete_using_flag(accountId)