from fastapi import APIRouter, Depends
from pymongo.client_session import ClientSession

from ...crud import crud_stocks
from ...models.stock import Stock, StocksResponse
from ...models.user import User
from ..dependencies import get_current_user, get_db

router = APIRouter()


@router.get('/stocks', response_model=StocksResponse)
def list_stocks(
    user: User = Depends(get_current_user),
    session: ClientSession = Depends(get_db)
):
    stocks = crud_stocks.index(user.username, session=session)

    return {'stocks': stocks}


@router.get('/stocks/{ticker}', response_model=Stock)
def show_stock(
    ticker: str,
    user: User = Depends(get_current_user),
    session: ClientSession = Depends(get_db)
):
    stock = crud_stocks.show(ticker, user.username, session=session)

    return stock
