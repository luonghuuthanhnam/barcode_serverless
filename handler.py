import json
import asyncio
import base64

from requests.models import Response
from src.api.v1.services.barcode import BarcodeReader
from src.api.v1.services.barcode import read_barcode
barcode_reader = BarcodeReader()

def hello(event, context):
    loop = asyncio.get_event_loop()
    # barcode_reader = BarcodeReader()
    body = event['body']
    response = asyncio.ensure_future(read_barcode(body, barcode_reader))
    # response = read_barcode(body, barcode_reader)
    result = loop.run_until_complete(response)
    print(result)
    

    
    # print(type(event['body']), event['body'])
    return result

