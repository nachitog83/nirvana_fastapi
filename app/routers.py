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
    """[summary]

    Args:
        url ([str]): [External API url]
        id ([int]): [member id]

    Returns:
        [json]: [API request response]
    """
    r = requests.get(url.format(id))
    return r.json()


@router.get("/", tags=["root"])
async def read_root():
    """[Root endpoint]

    Returns:
        [json]: [Welcome snippet]
    """
    return {'Hello': 'Challenge'}


@router.get("/insurance/", tags=["insurance"])
async def get_insurance(id: int = Query(None)):
    """[Calculate member's insurance true values]

    Args:
        id (int): [member id]. Defaults to Query(None).

    Returns:
        [Member object]: [Member instance with true health insurance values calculated]
    """
    #from .mock_api import data
    if id == None:
        return JSONResponse(content='Enter valid member id')

    results = []
    responses = []

    member = UserModel(id=id)
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

    member.true_deductible, member.true_stop_loss, member.true_oop_max, \
        = average_values(responses)
    member.insurance_data = results

    return member
