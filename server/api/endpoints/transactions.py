from fastapi import APIRouter, Depends, HTTPException, Response
from pymongo.client_session import ClientSession
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from ...crud import crud_stocks, crud_transactions
from ...models.transaction import Transaction, TransactionHistory
from ...models.user import User
from ..dependencies import get_current_user, get_db

router = APIRouter()


@router.get('/transactions', response_model=TransactionHistory)
def show_history(
    ticker: str = None,
    start: int = None,
    end: int = None,
    user: User = Depends(get_current_user),
    session: ClientSession = Depends(get_db),
):
    transactions = crud_transactions.index(
        username=user.username,
        ticker=ticker,
        start=start,
        end=end,
        session=session
    )

    return {'transactions': transactions}


@router.post('/transactions', status_code=HTTP_204_NO_CONTENT)
def new_transaction(
    transaction: Transaction,
    user: User = Depends(get_current_user),
    session: ClientSession = Depends(get_db)
):
    with session.start_transaction():
        crud_transactions.create(transaction, user.username, session=session)

        stock = crud_stocks.show_count(
            transaction.ticker, user.username, session=session
        )

        if stock.get('quantity') < 0:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Cannot sell more stocks than you own!'
            )

        if stock.get('quantity') == 0:
            crud_transactions.delete_all(
                transaction.ticker, user.username, session=session
            )

    return Response(status_code=HTTP_204_NO_CONTENT)
