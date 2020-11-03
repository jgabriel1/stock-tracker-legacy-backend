import os

MONGO_URL = os.getenv(
    'MONGO_URL',
    'mongodb://localhost:27017/stock_tracker_app'
)

TEST_MONGO_URL = os.getenv(
    'TEST_MONGO_URL',
    'mongodb://localhost:27017/stock_tracker_test'
)
