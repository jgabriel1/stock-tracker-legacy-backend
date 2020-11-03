from fastapi import APIRouter

from .endpoints import auth, stocks, transactions, users
from .external import yahoo_finance

router = APIRouter()

router.include_router(auth.router, prefix='/auth')
router.include_router(users.router)
router.include_router(stocks.router)
router.include_router(transactions.router)

router.include_router(yahoo_finance.router, prefix='/yahoo-proxy')
