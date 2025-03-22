from fastapi import APIRouter
from fastapi import Query
from fastapi import Path

from common.api_result import ApiResult, ResultStatus
from models.notice import NoticeModel
from services import notice as notice_service
from dtos.notice import NoticeResult, NoticeSchema
from pydantic import Field
from typing import Optional

router = APIRouter(
    prefix="/api/notice"
)

@router.get("/", response_model=ApiResult[list[NoticeResult]])
async def get_notice_list(
    useFlag: Optional[bool] = Query(True),
    schTxt: Optional[str] = Query(None),
    noticeKind: Optional[str] = Query(None),
    listCount: Optional[int] = Query(0, ge=0),
    skipCount: Optional[int] = Query(0, ge=0)
) -> ApiResult[list[NoticeResult]]:
    try:
        api_result = ApiResult[list[NoticeResult]]()
        api_result.data = notice_service.get_notice_list(useFlag=useFlag, schTxt=schTxt, noticeKind=noticeKind, listCount=listCount, skipCount=skipCount)
    except Exception as e:
        print("get_notice_list Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.get("/{noticeId}", response_model=ApiResult[NoticeResult])
async def get_notice_by_id(noticeId: int = Path(..., ge=1)) -> ApiResult[NoticeResult]:
    try:
        api_result = ApiResult[NoticeResult]()
        notice_data = notice_service.get_notice_by_id(noticeId)
        if notice_data:
            api_result.data = notice_data
        else:
            api_result.status = ResultStatus.FAIL
            api_result.reason = "NoticeNotFound"
    except Exception as e:
        print("get_notice_by_id Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.post("/", response_model=ApiResult[NoticeResult])
async def add_notice(noticeForm: NoticeSchema) -> ApiResult[NoticeModel]:
    try:
        api_result = ApiResult()
        notice_data = notice_service.add_notice(noticeForm)
        if notice_data:
            api_result.data = notice_data
        else:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("add_notice Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.put("/", response_model=ApiResult)
async def update_notice(noticeForm: NoticeSchema) -> ApiResult:
    try:
        api_result = ApiResult()
        result = notice_service.update_notice(noticeForm)
        if not result:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("update_notice Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result

@router.delete("/{noticeId}", response_model=ApiResult)
async def delete_notice(noticeId: int = Path(..., ge=1)) -> ApiResult:
    try:
        api_result = ApiResult()
        result = notice_service.delete_notice(noticeId)
        if not result:
            api_result.status = ResultStatus.FAIL
    except Exception as e:
        print("delete_notice Exception", e)
        api_result.status = ResultStatus.ERROR
        api_result.reason = "Exception"
        api_result.message = str(e)
    return api_result