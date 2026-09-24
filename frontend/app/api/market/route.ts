export async function GET() {
  try {
    const response = await fetch(
      'https://api.coingecko.com/api/v3/simple/price?ids=toucan-protocol-base-carbon-tonne&vs_currencies=usd&include_24hr_change=true',
      { cache: 'no-store', headers: { Accept: 'application/json' } }
    );

    if (!response.ok) {
      throw new Error(`Market feed returned ${response.status}`);
    }

    const data = await response.json();
    const item = data['toucan-protocol-base-carbon-tonne'];
    const price = Number(item?.usd);

    if (!Number.isFinite(price) || price <= 0) {
      throw new Error('Live VCM price was unavailable');
    }

    return Response.json({
      priceUsd: price,
      change24hPct: Number(item?.usd_24h_change ?? 0),
      source: 'CoinGecko / Toucan Base Carbon Tonne',
      dataType: 'live_vcm_proxy',
      fetchedAt: new Date().toISOString(),
    });
  } catch (error) {
    return Response.json(
      {
        error: 'Live carbon market feed unavailable',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 503 }
    );
  }
}
