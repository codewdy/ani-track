from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator, BeforeValidator
from datetime import datetime, timedelta
from pandas import Timedelta


def to_timedelta(x):
    return Timedelta(x).to_pytimedelta()


DateTimeWithTimeZone = Annotated[
    datetime,
    AfterValidator(lambda x: x.astimezone()),
]

TimeDelta = Annotated[
    timedelta,
    BeforeValidator(to_timedelta),
]
