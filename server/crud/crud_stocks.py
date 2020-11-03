from typing import Dict

from pymongo.client_session import ClientSession

from ..database.collections import get_users_collection


def index(username: str, session: ClientSession) -> Dict[str, dict]:
    users = get_users_collection(session=session)

    stocks = users.aggregate([
        {'$match': {'username': username}},
        {'$unwind': '$transactions'},
        {'$group': {
            '_id': '$transactions.ticker',

            'total_invested': {'$sum': {'$cond': [
                {'$gt': ['$transactions.total_value', 0]},
                '$transactions.total_value',
                0
            ]}},
            'total_shares_bought':{'$sum': {'$cond': [
                {'$gt': ['$transactions.total_value', 0]},
                '$transactions.quantity',
                0
            ]}},

            'total_sold':{'$sum': {'$cond': [
                {'$lt': ['$transactions.total_value', 0]},
                '$transactions.total_value',
                0
            ]}},
            'total_shares_sold':{'$sum': {'$cond': [
                {'$lt': ['$transactions.total_value', 0]},
                '$transactions.quantity',
                0
            ]}},
        }},
        {'$project': {
            '_id': 0,
            'ticker': '$_id',

            'total_invested': 1,
            'total_sold': 1,

            # Using add because selling transactions are negative:
            'currently_owned_shares': {'$add': [
                '$total_shares_bought',
                '$total_shares_sold',
            ]},

            'average_bought_price': {'$divide': [
                '$total_invested',
                '$total_shares_bought',
            ]},
        }}
    ], session=session)

    return {stock.get('ticker'): stock for stock in stocks}


def show(
        ticker: str, username: str, session: ClientSession) -> Dict[str, dict]:
    users = get_users_collection(session=session)

    stock, = users.aggregate([
        {'$match': {'username': username}},
        {'$unwind': '$transactions'},
        {'$match': {'transactions.ticker': ticker}},
        {'$group': {
            '_id': '$transactions.ticker',

            'total_invested': {'$sum': {'$cond': [
                {'$gt': ['$transactions.total_value', 0]},
                '$transactions.total_value',
                0
            ]}},
            'total_shares_bought':{'$sum': {'$cond': [
                {'$gt': ['$transactions.total_value', 0]},
                '$transactions.quantity',
                0
            ]}},

            'total_sold':{'$sum': {'$cond': [
                {'$lt': ['$transactions.total_value', 0]},
                '$transactions.total_value',
                0
            ]}},
            'total_shares_sold':{'$sum': {'$cond': [
                {'$lt': ['$transactions.total_value', 0]},
                '$transactions.quantity',
                0
            ]}},
        }},
        {'$project': {
            '_id': 0,
            'ticker': '$_id',

            'total_invested': 1,
            'total_sold': 1,

            # Using add because selling transactions are negative:
            'currently_owned_shares': {'$add': [
                '$total_shares_bought',
                '$total_shares_sold',
            ]},

            'average_bought_price': {'$divide': [
                '$total_invested',
                '$total_shares_bought',
            ]},
        }}
    ], session=session)

    return {'ticker': ticker, **stock}


def show_count(ticker: str, username: str,  session: ClientSession) -> dict:
    users = get_users_collection(session=session)

    stock, = users.aggregate([
        {'$match': {'username': username}},
        {'$unwind': '$transactions'},
        {'$match': {'transactions.ticker': ticker}},
        {'$group': {
            '_id': '$transactions.ticker',
            'quantity': {'$sum': '$transactions.quantity'},
        }},
        {'$project': {
            '_id': 0,
            'quantity': 1,
            'ticker': '$_id',
        }}
    ], session=session)

    return stock
