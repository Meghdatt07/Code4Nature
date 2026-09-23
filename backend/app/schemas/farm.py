from typing import Any
from pydantic import BaseModel,Field,ConfigDict
class FarmCreate(BaseModel):
    name:str=Field(min_length=1,max_length=200); geometry:dict[str,Any]; latitude:float; longitude:float; soil_type:str="Loam"; crop_type:str="Rice"; season:str="Kharif"
class FarmOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; name:str; latitude:float; longitude:float; area_hectares:float; area_acres:float; soil_type:str; crop_type:str; season:str; geometry:dict[str,Any]; data_source:str="synthetic_demo"