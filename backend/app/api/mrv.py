from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ._deps import get_db
from ..models.database import MRVRecord
router=APIRouter(prefix="/api/mrv",tags=["mrv"])
@router.get("/{farm_id}")
def mrv(farm_id:int,db:Session=Depends(get_db)):
    rows=db.query(MRVRecord).filter(MRVRecord.farm_id==farm_id).order_by(MRVRecord.timestamp.desc()).limit(100).all()
    return [{"id":r.id,"measurement_type":r.measurement_type,"value":r.value,"unit":r.unit,"source":r.source,"timestamp":r.timestamp.isoformat(),"verification_status":r.verification_status} for r in rows]