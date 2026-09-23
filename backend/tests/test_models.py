from app.services.simulation import run_simulation

def test_primary_demo():
    result = run_simulation(
        10,
        baseline_emission_tco2e_ha=6,
        emission_reduction_pct=41.6666667,
        carbon_price_usd=20,
        farmer_share=60,
        company_share=40,
    )
    assert round(result["baseline_emission_total_tco2e"], 2) == 60
    assert round(result["project_emission_total_tco2e"], 2) == 35
    assert round(result["emission_reduction_tco2e"], 2) == 25
    assert round(result["potential_credits"], 2) == 25
    assert round(result["farmer_revenue_usd"], 2) == 300

def test_share_validation():
    try:
        run_simulation(1, farmer_share=70, company_share=20)
    except ValueError:
        return
    raise AssertionError("Invalid shares were accepted")

def test_area_validation():
    try:
        run_simulation(0)
    except ValueError:
        return
    raise AssertionError("Zero area was accepted")
