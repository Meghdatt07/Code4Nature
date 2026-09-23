from datetime import datetime,timezone
class CarbonPriceProvider:
    def get_current_price(self)->float: raise NotImplementedError
class DemoCarbonPriceProvider(CarbonPriceProvider):
    def __init__(self,price:float=20.0): self.price=price
    def get_current_price(self)->float: return self.price
class FXProvider:
    def get_usd_inr(self)->float: raise NotImplementedError
class DemoFXProvider(FXProvider):
    def __init__(self,rate:float=83.0): self.rate=rate
    def get_usd_inr(self)->float: return self.rate
class SatelliteDataProvider:
    def get_imagery(self,*args,**kwargs): return {"status":"prototype_demo"}
    def get_soil_moisture(self,*args,**kwargs): return None
    def get_flooding_status(self,*args,**kwargs): return None
    def get_ndvi(self,*args,**kwargs): return None
    def get_field_history(self,*args,**kwargs): return []
class MockSatelliteProvider(SatelliteDataProvider): pass
class WeatherProvider:
    def get_weather(self,*args,**kwargs): return {"status":"prototype_demo"}
class MockWeatherProvider(WeatherProvider): pass
class SoilDataProvider:
    def get_soil(self,soil_type:str): return {"soil_type":soil_type,"status":"user_input"}
class UserSelectedSoilProvider(SoilDataProvider): pass
def timestamp(): return datetime.now(timezone.utc).isoformat()