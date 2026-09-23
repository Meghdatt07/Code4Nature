from fastapi import APIRouter
from datetime import datetime,timezone
from ..schemas.carbon import CarbonPriceOut,CarbonPriceIn
from ..services.providers import DemoCarbonPriceProvider,DemoFXProvider
router=APIRouter(prefix="/api/carbon",tags=["carbon"]); provider=DemoCarbonPriceProvider(20.0); fx=DemoFXProvider(83.0)
@router.get("/price",response_model=CarbonPriceOut)
def get_price(): return CarbonPriceOut(price_usd=provider.get_current_price(),source="demo_config",data_type="simulated",timestamp=datetime.now(timezone.utc).isoformat())
@router.post("/price")
def set_price(payload:CarbonPriceIn): provider.price=payload.price_usd; fx.rate=payload.fx_rate; return {"price_usd":provider.price,"fx_rate":fx.rate,"data_type":"simulated"}