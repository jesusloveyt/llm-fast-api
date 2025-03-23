from fastapi import APIRouter
from fastapi import Query
from fastapi import Path

from common.api_result import ApiResult, ResultStatus
from models.account import AccountModel
from services import account as account_service
from dtos.account import AccountResult, AccountForm
from typing import Optional

router = APIRouter(
    prefix="/api/account"
)

@router.get("/", response_model=ApiResult[list[AccountResult]])
async def get_account_list(
    useFlag: Optional[bool] = Query(True),
    schTxt: Optional[str] = Query(None),
    joinType: Optional[str] = Query(None),
    listCount: Optional[int] = Query(0, gt=0),
    skipCount: Optional[int] = Query(0, ge=0)
) -> ApiResult[list[AccountResult]]:
    try:
        api_result = ApiResult[list[AccountResult]]()
        api_result.data = account_service.get_account_list(useFlag=useFlag, schTxt=schTxt, joinType=joinType, listCount=listCount, skipCount=skipCount)
    except Exception as e:
        print("get_account_list Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.get("/{accountId}", response_model=ApiResult[AccountResult])
async def get_account_by_id(accountId: int = Path(..., ge=1)) -> ApiResult[AccountResult]:
    try:
        api_result = ApiResult[AccountResult]()
        account_data = account_service.get_account_by_id(accountId)
        if account_data:
            api_result.data = account_data
        else:
            api_result.status = ResultStatus.FAIL
            api_result.reason = "AccountNotFound"
    except Exception as e:
        print("get_account_by_id Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.post("/", response_model=ApiResult[AccountResult])
async def add_account(accountForm: AccountForm) -> ApiResult[AccountModel]:
    try:
        api_result = ApiResult()
        account_data = account_service.add_account(accountForm)
        if account_data:
            api_result.data = account_data
        else:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("add_account Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.put("/", response_model=ApiResult)
async def update_account(accountForm: AccountForm) -> ApiResult:
    try:
        api_result = ApiResult()
        result = account_service.update_account(accountForm)
        if not result:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("update_account Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.delete("/{accountId}", response_model=ApiResult)
async def delete_account(accountId: int = Path(..., ge=1)) -> ApiResult:
    try:
        api_result = ApiResult()
        result = account_service.delete_account(accountId)
        if not result:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("delete_account Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result