export const ACRE_TO_SQM=4046.8564224;
export const HA_TO_ACRE=2.47105381;

/**
 * Code4Nature rice-MRV reference standard.
 *
 * The Digital MRV page uses:
 *   120 kg CH4 abatement / ha / season
 *   28 kg CO2e / kg CH4 (GWP100)
 *
 * Therefore one hectare represents 3.36 tCO2e of potential
 * methane-abatement impact per season.
 */
export const RICE_CH4_ABATEMENT_KG_PER_HA=120;
export const CH4_GWP100=28;
export const RICE_CO2E_T_PER_HA_PER_SEASON=
  (RICE_CH4_ABATEMENT_KG_PER_HA*CH4_GWP100)/1000;

export function demoWater(areaHa:number,baselineLPerAcre=4_960_000,optimizedLPerAcre=3_140_000){
  const acres=areaHa*HA_TO_ACRE;
  const baseline=acres*baselineLPerAcre;
  const project=acres*optimizedLPerAcre;
  return{baseline,project,saved:baseline-project,pct:baseline?((baseline-project)/baseline)*100:0};
}

/**
 * Standard rice-MRV emission opportunity.
 * This is deliberately methane-based so it stays aligned with Digital MRV.
 */
export function standardRiceEmission(areaHa:number){
  const methaneKg=areaHa*RICE_CH4_ABATEMENT_KG_PER_HA;
  const reduction=methaneKg*CH4_GWP100/1000;
  return{
    methaneKg,
    baseline:areaHa*RICE_CO2E_T_PER_HA_PER_SEASON,
    project:0,
    reduction
  };
}

/**
 * Legacy configurable demo calculation retained for other scenarios.
 */
export function demoEmission(areaHa:number,baseline=6,reductionPct=41.6666667){
  const b=areaHa*baseline;
  const p=b*(1-reductionPct/100);
  return{baseline:b,project:p,reduction:b-p};
}

export function revenue(credits:number,price:number,farmerPct:number){
  const gross=credits*price;
  return{gross,farmer:gross*farmerPct/100,company:gross*(1-farmerPct/100)};
}
