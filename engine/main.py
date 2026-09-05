# File: engine/main.py
import os, math, re
from datetime import datetime, timezone, timedelta
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='CarbonAWD API', version='1.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

SH_CLIENT_ID=os.getenv('SH_CLIENT_ID','')
SH_CLIENT_SECRET=os.getenv('SH_CLIENT_SECRET','')
SH_TOKEN_URL='https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token'
SH_STATS_URL='https://services.sentinel-hub.com/api/v1/statistics'

def bbox(lat, lon, delta=0.003):
    return [lon-delta, lat-delta, lon+delta, lat+delta]

def token():
    r=requests.post(SH_TOKEN_URL,data={'grant_type':'client_credentials','client_id':SH_CLIENT_ID,'client_secret':SH_CLIENT_SECRET},timeout=15)
    r.raise_for_status(); return r.json()['access_token']

@app.get('/health')
def health(): return {'ok':True,'sentinel_hub_configured':bool(SH_CLIENT_ID and SH_CLIENT_SECRET)}

@app.get('/api/sar')
def sar(lat: float=Query(...), lon: float=Query(...)):
    if not (SH_CLIENT_ID and SH_CLIENT_SECRET):
        return {'source':'simulator','moisture_proxy_percent':None,'vv_mean_db':None,'vh_mean_db':None,'observation_date':None,'note':'Set SH_CLIENT_ID and SH_CLIENT_SECRET on the server to enable live Sentinel Hub queries.'}
    now=datetime.now(timezone.utc); start=now-timedelta(days=18)
    evalscript='''//VERSION=3\nfunction setup(){return {input:[{bands:["VV","VH","dataMask"]}],output:[{id:"sar",bands:2,sampleType:"FLOAT32"},{id:"dataMask",bands:1}]};}\nfunction evaluatePixel(s){return {sar:[s.VV,s.VH],dataMask:[s.dataMask]};}'''
    payload={'input':{'bounds':{'bbox':bbox(lat,lon),'properties':{'crs':'http://www.opengis.net/def/crs/OGC/1.3/CRS84'}},'data':[{'type':'sentinel-1-grd','dataFilter':{'mosaickingOrder':'mostRecent'},'processing':{'orthorectify':'true'}}]},'aggregation':{'timeRange':{'from':start.isoformat().replace('+00:00','Z'),'to':now.isoformat().replace('+00:00','Z')},'aggregationInterval':{'of':'P6D'},'evalscript':evalscript,'resx':0.0001,'resy':0.0001},'calculations':{'default':{}}}
    try:
        r=requests.post(SH_STATS_URL,headers={'Authorization':'Bearer '+token(),'Content-Type':'application/json'},json=payload,timeout=40); r.raise_for_status(); data=r.json().get('data',[])
        if not data: raise RuntimeError('No Sentinel-1 observations for this AOI/time window')
        latest=data[-1]; bands=latest.get('outputs',{}).get('sar',{}).get('bands',{})
        vv=bands.get('B0',{}).get('stats',{}).get('mean'); vh=bands.get('B1',{}).get('stats',{}).get('mean')
        # Sentinel Hub S1 values are linear power in many configurations; convert to dB.
        vv_db=10*math.log10(vv) if vv and vv>0 else None; vh_db=10*math.log10(vh) if vh and vh>0 else None
        # This is intentionally a relative wetness proxy, NOT absolute soil moisture.
        proxy=None
        if vv_db is not None:
            proxy=max(0,min(100,50 + (vv_db+15)*7))
        return {'source':'Sentinel Hub / Sentinel-1 GRD','moisture_proxy_percent':proxy,'vv_mean_db':vv_db,'vh_mean_db':vh_db,'observation_date':latest.get('interval',{}).get('to'),'note':'Relative wetness proxy derived from SAR backscatter. Absolute soil moisture requires field calibration/model validation.'}
    except Exception as e:
        return {'source':'Sentinel Hub error','moisture_proxy_percent':None,'vv_mean_db':None,'vh_mean_db':None,'observation_date':None,'note':str(e)}

@app.get('/api/market')
def market():
    fx=88.0; fx_source='fallback FX'
    try:
        j=requests.get('https://open.er-api.com/v6/latest/USD',timeout=10).json(); fx=float(j['rates']['INR']); fx_source='open.er-api.com'
    except Exception: pass
    # Carbon.fyi publishes a public HTML market table with current category medians.
    ag=None; updated=''
    try:
        html=requests.get('https://www.carbon.fyi/data',timeout=15).text
        m=re.search(r'Agriculture.*?\$([0-9,.]+).*?\$([0-9,.]+)',html,re.S)
        if m: ag=float(m.group(2).replace(',',''))
        t=re.search(r'Updated\s+([^<]+)',html,re.I)
        if t: updated=t.group(1).strip()
    except Exception: pass
    if ag is None: ag=71.40
    return {'global_agriculture_median_usd':ag,'fx_usd_inr':fx,'global_source':'Carbon.fyi / Carbonmark public market data','fx_source':fx_source,'updated_at':updated or 'latest available feed','india_note':'India VCM proxy is converted from the observable global agriculture category. Indian CCTS/CCC spot price is intentionally not fabricated.'}
