from fastapi import APIRouter
from fastapi import Query
from fastapi import Path

from pydantic import Field
from typing import Optional

from common.api_result import ApiResult, ResultStatus
from models.file import FileModel
from services import file as file_service
from dtos.file import FileForm, FileResult, FileSchema


router = APIRouter(
    prefix="/api/file"
)

@router.get("/", response_model=ApiResult[list[FileResult]])
async def get_file_list(
    schTxt: Optional[str] = Query(None),
    linkInfo: Optional[str] = Query(None),
    listCount: Optional[int] = Query(0, ge=0),
    skipCount: Optional[int] = Query(0, ge=0)
) -> ApiResult[list[FileModel]]:
    try:
        api_result = ApiResult[list[FileModel]]()
        api_result.data = file_service.get_file_list(schTxt=schTxt, linkInfo=linkInfo, listCount=listCount, skipCount=skipCount)
    except Exception as e:
        print("get_file_list Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.get("/{fileId}", response_model=ApiResult[FileResult])
async def get_file_by_id(fileId: int = Path(..., ge=1)) -> ApiResult[FileModel]:
    try:
        api_result = ApiResult[FileModel]()
        file_data = file_service.get_file_by_id(fileId)
        if file_data:
            api_result.data = file_data
        else:
            api_result.status = ResultStatus.FAIL
            api_result.reason = "FileNotFound"
    except Exception as e:
        print("get_file_by_id Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.post("/", response_model=ApiResult[FileResult])
async def upload_file(fileForm: FileForm) -> ApiResult[FileModel]:
    try:
        api_result = ApiResult()
        file_data = file_service.upload_file(fileForm)
        if file_data:
            api_result.data = file_data
        else:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("add_file Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.delete("/{fileId}", response_model=ApiResult)
async def delete_file(fileId: int = Path(..., ge=1)) -> ApiResult:
    try:
        api_result = ApiResult()
        result = file_service.delete_file(fileId)
        if not result:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("delete_file Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.post("/add", response_model=ApiResult[FileResult])
async def add_file(fileForm: FileSchema) -> ApiResult[FileModel]:
    try:
        api_result = ApiResult()
        file_data = file_service.add_file(fileForm)
        if file_data:
            api_result.data = file_data
        else:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("add_file Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result