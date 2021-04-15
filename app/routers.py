from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from pydantic import ValidationError
from .models import InsuranceModel, UserModel
from app import controller
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


@router.get("/insurance/", tags=["insurance"], response_model=UserModel)
async def get_insurance(id: int, method: Optional[str] = Query('most_repeated_values')):
    """[summary]

    Args:
        id (int): [member id]
        method (Optional[str], optional): [selector for calculation method]. Defaults to Query('most_repeated_values').

    Raises:
        HTTPException: [API values validation]

    Returns:
        [user object]: [user objet with results]
    """

    from .mock_api import data
    # if id == None:
    #     return JSONResponse(content='Enter valid member id')

    if method == 'most_repeated_values' or method == 'average_values':
        pass
    else:
        return JSONResponse(content='Enter valid calculation method')

    f = getattr(controller, method)

    results = []
    responses = []

    try:
        for url in settings.URLS:
            responses.append(get_api_results(url, id))
    except:
        responses = [b for a in data if a['member_id'] == id for \
            b in a['responses']]

    for url, response in zip(settings.URLS, responses):
        try:
            results.append(InsuranceModel(api=url.split('?')[0], **response))
        except ValueError as e:
            errors.append(json.loads(e.json()))
            raise HTTPException(status_code=400, detail=e)

    true_deductible, true_stop_loss, true_oop_max = f(responses)

    member = UserModel(id=id,
                       true_deductible=true_deductible,
                       true_stop_loss=true_stop_loss,
                       true_oop_max=true_oop_max,
                       insurance_data=results
                       )

    return member
