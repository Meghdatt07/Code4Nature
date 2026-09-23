def validate_split(farmer_share: float, company_share: float) -> None:
    if abs((farmer_share + company_share) - 100.0) > 1e-6: raise ValueError("Farmer share + company share must equal 100%.")
def allocate(gross_value: float, farmer_share: float, company_share: float):
    validate_split(farmer_share, company_share)
    return gross_value * farmer_share / 100.0, gross_value * company_share / 100.0