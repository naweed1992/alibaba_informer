from pydantic import BaseModel, Field


class Limits(BaseModel):
    lower_limit: str = Field(default='08:14', description="08:14")
    higher_limit: str = Field(default='23:00', description="23:00")


class SearchConfig(BaseModel):
    origin_city_code: str = Field(default='26310000', description="26310000")
    destination_city_code: str = Field(default='11320000', description="11320000")
    request_dates: list = Field(default='["2023-03-24"]', description="['2023-03-24']")
    expected_time: Limits
    target_mail: str = Field(default='alibabainformer@gmail.com', description="alibabainformer@gmail.com")
