from fastapi import APIRouter
from fastapi import Query
from fastapi import Path
from fastapi import HTTPException

from common.api_result import ApiResult, ResultStatus
from models.code import CodeModel
from services import code as code_service
from dtos.code import CodeResult, CodeSchema
from pydantic import Field
from typing import List, Optional

router = APIRouter(
    prefix="/api/code"
)

@router.get("/", response_model=ApiResult[list[CodeResult]])
async def get_code_list(
    useFlag: Optional[bool] = Query(True),
    schTxt: Optional[str] = Query(None),
    parentCode: Optional[str] = Query(None),
    listCount: Optional[int] = Query(0, gt=0),
    skipCount: Optional[int] = Query(0, ge=0)
) -> ApiResult[list[CodeModel]]:
    try:
        api_result = ApiResult[list[CodeModel]]()
        api_result.data = code_service.get_code_list(useFlag=useFlag, schTxt=schTxt, parentCode=parentCode, listCount=listCount, skipCount=skipCount)
    except Exception as e:
        print("get_code_list Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.get("/{codeId}", response_model=ApiResult[CodeResult])
async def get_code_by_id(codeId: int = Path(..., ge=1)) -> ApiResult[CodeModel]:
    try:
        api_result = ApiResult[CodeModel]()
        code_data = code_service.get_code_by_id(codeId)
        if code_data:
            api_result.data = code_data
        else:
            api_result.status = ResultStatus.FAIL
            api_result.reason = "CodeNotFound"
    except Exception as e:
        print("get_code_by_id Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.post("/", response_model=ApiResult[CodeResult])
async def add_code(codeForm: CodeSchema) -> ApiResult[CodeModel]:
    try:
        api_result = ApiResult()
        code_data = code_service.add_code(codeForm)
        if code_data:
            api_result.data = code_data
        else:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("add_code Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.put("/", response_model=ApiResult)
async def update_code(codeForm: CodeSchema) -> ApiResult:
    try:
        api_result = ApiResult()
        result = code_service.update_code(codeForm)
        if not result:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("update_code Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.delete("/{codeId}", response_model=ApiResult)
async def delete_code(codeId: int = Path(..., ge=1)) -> ApiResult:
    try:
        api_result = ApiResult()
        result = code_service.delete_code(codeId)
        if not result:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("delete_code Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result


# @router.get("/me", response_model=dto.GetUser)
# async def get_me(user: dependencies.user_dependency) -> db.User:
#     return user

# @router.get("/email/{email}", response_model=dto.GetUser)
# async def get_by_email(email: str) -> db.User | None:
#     user = user_service.get_by_email(email)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return user    