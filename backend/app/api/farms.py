import json
from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from shapely.geometry import shape
from ._deps import get_db
from ..models.database import Farm
from ..schemas.farm import FarmCreate,FarmOut
router=APIRouter(prefix="/api/farms",tags=["farms"]); SQM_PER_HECTARE=10000.0; SQM_PER_ACRE=4046.8564224
def area_from_geojson(geometry:dict)->float:
    polygon=shape(geometry)
    if polygon.is_empty or not polygon.is_valid: raise ValueError("Invalid farm polygon")
    import pyproj
    from shapely.ops import transform
    fn=pyproj.Transformer.from_crs(4326,6933,always_xy=True).transform
    return max(0.0,transform(fn,polygon).area)
@router.post("",response_model=FarmOut)
def create_farm(payload:FarmCreate,db:Session=Depends(get_db)):
    try: sqm=area_from_geojson(payload.geometry)
    except Exception as exc: raise HTTPException(400,"Invalid geometry: "+str(exc))
    now=datetime.now(timezone.utc).replace(tzinfo=None)
    farm=Farm(name=payload.name,geometry_geojson=json.dumps(payload.geometry),latitude=payload.latitude,longitude=payload.longitude,area_hectares=sqm/SQM_PER_HECTARE,area_acres=sqm/SQM_PER_ACRE,soil_type=payload.soil_type,season=payload.season,crop_type=payload.crop_type,created_at=now,updated_at=now)
    db.add(farm); db.commit(); db.refresh(farm)
    return FarmOut(id=farm.id,name=farm.name,latitude=farm.latitude,longitude=farm.longitude,area_hectares=farm.area_hectares,area_acres=farm.area_acres,soil_type=farm.soil_type,crop_type=farm.crop_type,season=farm.season,geometry=payload.geometry)
@router.get("",response_model=list[FarmOut])
def list_farms(limit:int=100,db:Session=Depends(get_db)):
    rows=db.query(Farm).order_by(Farm.id).limit(min(limit,500)).all()
    return [FarmOut(id=f.id,name=f.name,latitude=f.latitude,longitude=f.longitude,area_hectares=f.area_hectares,area_acres=f.area_acres,soil_type=f.soil_type,crop_type=f.crop_type,season=f.season,geometry=json.loads(f.geometry_geojson),data_source="synthetic_demo") for f in rows]
@router.get("/{farm_id}",response_model=FarmOut)
def get_farm(farm_id:int,db:Session=Depends(get_db)):
    f=db.get(Farm,farm_id)
    if not f: raise HTTPException(404,"Farm not found")
    return FarmOut(id=f.id,name=f.name,latitude=f.latitude,longitude=f.longitude,area_hectares=f.area_hectares,area_acres=f.area_acres,soil_type=f.soil_type,crop_type=f.crop_type,season=f.season,geometry=json.loads(f.geometry_geojson),data_source="synthetic_demo")