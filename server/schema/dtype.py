from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator
from datetime import datetime

DateTimeWithTimeZone = Annotated[
    datetime,
    AfterValidator(lambda x: x.astimezone()),
]
