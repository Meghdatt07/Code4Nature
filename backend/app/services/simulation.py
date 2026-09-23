from .models import DemoWaterModel, DemoEmissionModel, DemoCarbonModel, DemoRevenueModel

MODEL_VERSION='demo-v1.0'

def validate_shares(farmer, company):
    if farmer < 0 or company < 0 or abs((farmer+company)-100)>1e-9:
        raise ValueError('Farmer and company shares must be non-negative and total 100%.')

def run_simulation(area_ha, soil_type='Loam', season='Kharif', crop_days=120,
                   baseline_water_l_per_acre=4_960_000, water_reduction_pct=36.7,
                   baseline_emission_tco2e_ha=6.0, emission_reduction_pct=41.6666667,
                   carbon_price_usd=20, farmer_share=60, company_share=40, fx=83):
    if area_ha <= 0: raise ValueError('Farm area must be greater than zero.')
    if baseline_emission_tco2e_ha < 0 or carbon_price_usd < 0: raise ValueError('Values cannot be negative.')
    validate_shares(farmer_share, company_share)
    water=DemoWaterModel().predict(soil_type,season,crop_days,baseline_water_l_per_acre,water_reduction_pct)
    b,p,r,project_per_ha=DemoEmissionModel().predict(area_ha,baseline_emission_tco2e_ha,emission_reduction_pct)
    credits,gross=DemoCarbonModel().calculate(r,carbon_price_usd)
    farmer,company=DemoRevenueModel().split(gross,farmer_share)
    acres=area_ha*2.47105381
    return {'model_version':MODEL_VERSION,'data_source':'synthetic_demo','data_type':'simulated','farm_area_ha':area_ha,'farm_area_acres':acres,'baseline_water_liters_per_acre':water.baseline_l_per_acre,'project_water_liters_per_acre':water.project_l_per_acre,'water_saved_liters_per_acre':water.saved_l_per_acre,'water_saving_percent':water.saving_pct,'baseline_emission_tco2e_per_ha':baseline_emission_tco2e_ha,'project_emission_tco2e_per_ha':project_per_ha,'baseline_emission_total_tco2e':b,'project_emission_total_tco2e':p,'emission_reduction_tco2e':r,'potential_credits':credits,'carbon_price_usd':carbon_price_usd,'gross_value_usd':gross,'gross_value_inr':gross*fx,'farmer_share_percent':farmer_share,'company_share_percent':company_share,'farmer_revenue_usd':farmer,'company_revenue_usd':company,'farmer_revenue_inr':farmer*fx,'company_revenue_inr':company*fx,'demo_fx_usd_inr':fx,'total_water_saved_liters':water.saved_l_per_acre*acres}
