from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(messages:str="success",data=None):
    content = {
        "code": 200,
        "messages": messages,
        "data": data
    }
    return JSONResponse(content=jsonable_encoder(content))