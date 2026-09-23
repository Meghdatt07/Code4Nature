def potential_credits(reduction_tco2e: float) -> float: return max(0.0, reduction_tco2e)
def gross_value_usd(credits: float, price_usd: float) -> float: return max(0.0, credits) * max(0.0, price_usd)