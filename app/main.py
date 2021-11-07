"""
Simple fastapi app

Functions:
    pong()
        Simple fastapi test function
"""

from fastapi import FastAPI


app = FastAPI()


@app.get('/ping')
def pong():
    """Simple fastapi test function"""
    return {'ping': 'pong!'}
