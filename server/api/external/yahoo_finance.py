from aiohttp import ClientSession
from fastapi import APIRouter, HTTPException, Request
from starlette.status import HTTP_424_FAILED_DEPENDENCY

from ...settings.external_services import YAHOO_SPARK_URL, YAHOO_SEARCH_URL

router = APIRouter()


@router.get('/info')
async def yahoo_stock_info(request: Request):
    params = request.query_params
    url = YAHOO_SPARK_URL

    async with ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status >= 400:
                raise HTTPException(
                    status_code=HTTP_424_FAILED_DEPENDENCY,
                    detail='Yahoo Finance is currently unavailable.'
                )

            return await response.json()


@router.get('/search')
async def yahoo_stock_search(request: Request):
    params = request.query_params
    url = YAHOO_SEARCH_URL

    async with ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status >= 400:
                raise HTTPException(
                    status_code=HTTP_424_FAILED_DEPENDENCY,
                    detail='Yahoo Finance is currently unavailable.'
                )

            return await response.json()
