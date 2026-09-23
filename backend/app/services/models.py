from dataclasses import dataclass

@dataclass
class WaterResult:
    baseline_l_per_acre: float
    project_l_per_acre: float
    saved_l_per_acre: float
    saving_pct: float

class BaseWaterModel:
    def predict(self, soil_type:str, season:str, crop_days:int, baseline_l_per_acre:float, reduction_pct:float)->WaterResult: raise NotImplementedError

class DemoWaterModel(BaseWaterModel):
    def predict(self, soil_type, season, crop_days, baseline_l_per_acre=4_960_000, reduction_pct=36.7):
        reduction_pct=max(0,min(90,float(reduction_pct)))
        project=baseline_l_per_acre*(1-reduction_pct/100)
        return WaterResult(baseline_l_per_acre,project,baseline_l_per_acre-project,reduction_pct)

class BaseEmissionModel:
    def predict(self, area_ha:float, baseline_tco2e_ha:float, reduction_pct:float): raise NotImplementedError

class DemoEmissionModel(BaseEmissionModel):
    def predict(self, area_ha, baseline_tco2e_ha, reduction_pct):
        reduction_pct=max(0,min(70,float(reduction_pct)))
        baseline_total=area_ha*baseline_tco2e_ha
        project_per_ha=baseline_tco2e_ha*(1-reduction_pct/100)
        project_total=area_ha*project_per_ha
        return baseline_total,project_total,baseline_total-project_total,project_per_ha

class BaseCarbonModel:
    def calculate(self, reduction_tco2e, price): raise NotImplementedError
class DemoCarbonModel(BaseCarbonModel):
    def calculate(self, reduction_tco2e, price): return max(0,reduction_tco2e),max(0,reduction_tco2e)*price

class BaseRevenueModel:
    def split(self, gross, farmer_share): raise NotImplementedError
class DemoRevenueModel(BaseRevenueModel):
    def split(self, gross, farmer_share):
        farmer=gross*farmer_share/100
        return farmer,gross-farmer
