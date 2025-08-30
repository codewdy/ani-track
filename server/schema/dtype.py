from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator, BeforeValidator
from datetime import datetime, timedelta
from pandas import Timedelta

DateTimeWithTimeZone = Annotated[
    datetime,
    AfterValidator(lambda x: x.astimezone()),
]

TimeDelta = Annotated[
    timedelta,
    BeforeValidator(lambda x: Timedelta(x).to_pytimedelta()),
]
