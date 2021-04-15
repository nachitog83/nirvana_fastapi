from typing import List
from pydantic import BaseModel, root_validator
import logging

logger = logging.getLogger(__name__)


class InsuranceModel(BaseModel):
    """[Insurance values model]

    Raises:
        ValueError: [Validate that deductible is not larger than oop_max]
        ValueError: [Validate that oop_max is not larger than stop_loss]
    """
    api: str
    deductible: float
    stop_loss: float
    oop_max: float

    @root_validator
    def validate_insurance(cls, values):
        deductible, stop_loss, oop_max = values.get('deductible'), \
            values.get('stop_loss'), values.get('oop_max')
        if deductible > oop_max:
            raise ValueError('Deductible cannot be larger than OOP Max')
        elif oop_max > stop_loss:
            raise ValueError('OOP Max cannot be larger than Stop Loss')
        return values


class UserModel(BaseModel):
    """[User Model]

    """
    id: int
    true_deductible: float
    true_stop_loss: float
    true_oop_max: float
    insurance_data: List[InsuranceModel]
