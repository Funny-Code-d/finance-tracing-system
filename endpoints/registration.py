import json
from fastapi import routing


@routing.post('/')
async def registation_token():
    request = json # getting data from json
    
    
    