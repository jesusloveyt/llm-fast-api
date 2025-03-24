from sqlalchemy import Update
from sqlalchemy.sql.functions import current_timestamp

from common.db.query_worker import query_data
from common.db.context import session_maker
from models.account import AccountModel
from models.file import FileModel

def query_list(useFlag:bool=True, schTxt:str=None, joinType:str=None, listCount:int=None, skipCount:int=None)-> list[AccountModel]:
    where_sql = "WHERE 1 = 1"
    params = {}
    if useFlag:
        where_sql += " AND acnt.use_fg = %(useFlag)s"
        params["useFlag"] = useFlag
    if joinType:
        where_sql += " AND acnt.join_type = %(joinType)s"
        params["joinType"] = joinType
    if schTxt:
        where_sql += """ AND (
            ( acnt.user_name   LIKE concat('%%', %(schTxt)s, '%%') ) OR
            ( acnt.account_key LIKE concat('%%', %(schTxt)s, '%%') ) OR
            ( acnt.phone       LIKE concat('%%', %(schTxt)s, '%%') )
            )"""
        params["schTxt"] = schTxt

    list_sql = f"""
        SELECT acnt.*
            ,fle.file_url
        FROM tb_account acnt
        LEFT JOIN tb_file fle ON fle.link_info = 'accountProfileImage' AND fle.link_key = acnt.account_id AND fle.deleted_at is NULL
        {where_sql}
        ORDER BY acnt.account_id DESC
    """
    if listCount:
        list_sql += f" LIMIT {skipCount or 0}, {listCount}"

    rows = query_data(list_sql, params)
    if not rows or len(rows) == 0:
        return []
    
    account_list:list[AccountModel] = []
    for row in rows:
        account = AccountModel()
        account.accountId = row["account_id"]
        account.joinType = row["join_type"]
        account.accountKey = row["account_key"]
        account.snsKey = row["sns_key"]
        account.userName = row["user_name"]
        account.phone = row["phone"]
        account.email = row["email"]
        account.role = row["role"]
        account.updatedAt = row["updated_at"]
        account.loginAt = row["login_at"]
        if "file_url" in row:
            account.profileImage = FileModel()
            account.profileImage.fileUrl = row["file_url"]

        account_list.append(account)

    return account_list
    
def get_list(useFlag:bool=True, schTxt:str=None, joinType:str=None, listCount:int=None, skipCount:int=None)-> list[AccountModel]:
    with session_maker() as session:
        account_list_query = session.query(AccountModel).filter(AccountModel.useFlag == useFlag)
        if joinType:
            account_list_query = account_list_query.filter(AccountModel.joinType == joinType)
        if schTxt:
            account_list_query = account_list_query.filter(
                AccountModel.accountKey.like(f'%{schTxt}%') |
                AccountModel.userName.like(f'%{schTxt}%') |
                AccountModel.phone.like(f'%{schTxt}%')
            )
        if skipCount:
            account_list_query = account_list_query.offset(skipCount)
        if listCount:
            account_list_query = account_list_query.limit(listCount)
        
        account_list = account_list_query.all()
        return account_list

def get_by_id(accountId:int)-> AccountModel:
    with session_maker() as session:
        account = session.query(AccountModel).filter(AccountModel.accountId == accountId).first()
        return account

def insert(joinType: str, accountKey: str, password: str, snsKey: str, userName: str, phone: str, email: str,
              postcode: str, address: str, addressDetail: str, role: str, fcmToken: str, refreshToken: str
           )-> AccountModel:
    with session_maker.begin() as session:
        new_account = AccountModel()
        new_account.joinType = joinType
        new_account.accountKey = accountKey
        new_account.password = password
        new_account.snsKey = snsKey
        new_account.userName = userName
        new_account.phone = phone
        new_account.email = email
        new_account.postcode = postcode
        new_account.address = address
        new_account.addressDetail = addressDetail
        new_account.role = role
        new_account.fcmToken = fcmToken
        new_account.refreshToken = refreshToken
        new_account.useFlag = True
        new_account.createdAt = current_timestamp()
        new_account.updatedAt = current_timestamp()
        new_account.passwordAt = current_timestamp()

        session.add(new_account)
        session.flush()
        session.refresh(new_account)
        return new_account

def update(accountId: int, joinType: str, userName: str, phone: str, email: str, postcode: str, address: str, addressDetail: str, role: str, fcmToken: str, refreshToken: str)-> bool:
    with session_maker.begin() as session:
        update_values = {
            AccountModel.userName: userName,
            AccountModel.phone: phone,
            AccountModel.email: email,
            AccountModel.postcode: postcode,
            AccountModel.address: address,
            AccountModel.addressDetail: addressDetail,
            AccountModel.role: role,
            AccountModel.fcmToken: fcmToken,
            AccountModel.refreshToken: refreshToken,
            AccountModel.updatedAt: current_timestamp()
        }

        if joinType is not None:
            update_values[AccountModel.joinType] = joinType

        session.execute(Update(AccountModel).where(AccountModel.accountId == accountId).values(update_values))
        return True

def delete_using_flag(accountId: int) -> bool:
    with session_maker.begin() as session:
        session.execute(Update(AccountModel)
                        .where(AccountModel.accountId == accountId)
                        .values({AccountModel.useFlag: False}))
        return True