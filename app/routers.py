from fastapi import APIRouter, Query
from pydantic import ValidationError
from .models import InsuranceModel, UserModel
from .controller import average_values, most_repeated_values
from fastapi.responses import JSONResponse
from app.config import settings
import requests
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_api_results(url, id):
    r = requests.get(url.format(id))
    return r.json()


@router.get("/", tags=["root"])
async def read_root():
    return {'Hello': 'Challenge'}


@router.get("/insurance/", tags=["insurance"])
async def get_insurance(id: int = Query(None)):
    #from .mock_api import data
    results = []
    responses = []

    user = UserModel(id=id)
    for url in settings.URLS:
        responses.append(get_api_results(url, id))

    # responses = [b for a in data if a['member_id'] == id for \
    #     b in a['responses']]

    for url, response in zip(settings.URLS, responses):
        try:
            results.append(InsuranceModel(api=url.split('?')[0], **response))
        except ValidationError as e:
            e = json.loads(e.json())
            return JSONResponse(
                    content=e
                )

    user.true_deductible, user.true_stop_loss, user.true_oop_max, \
        = average_values(responses)
    user.insurance_data = results

    return user
