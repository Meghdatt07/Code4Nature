from pydantic import BaseModel,Field
class CarbonPriceOut(BaseModel):
    price_usd:float; source:str; data_type:str; timestamp:str
class CarbonPriceIn(BaseModel):
    price_usd:float=Field(gt=0); fx_rate:float=Field(gt=0)