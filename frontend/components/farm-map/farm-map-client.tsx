'use client';

import { useEffect, useRef, useState } from 'react';
import { importLibrary, setOptions } from '@googlemaps/js-api-loader';

type Geometry = { type: 'Polygon'; coordinates: number[][][] };
type Props = { value?: Geometry; onChange?: (geometry: Geometry | null, areaHa: number) => void };

const DEFAULT_CENTER = { lat: 23.2135, lng: 72.6840 };

export default function FarmMap({ value, onChange }: Props) {
  const ref = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<google.maps.Map | null>(null);
  const polygonRef = useRef<google.maps.Polygon | null>(null);
  const centerMarkerRef = useRef<google.maps.Circle | null>(null);
  const listenersRef = useRef<google.maps.MapsEventListener[]>([]);
  const [points, setPoints] = useState<[number, number][]>(() =>
    value?.coordinates?.[0]?.map(([lng, lat]) => [lat, lng] as [number, number]) || []
  );
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;

    async function initMap() {
      const key = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
      if (!key) {
        setError('Google Maps is not configured. Add NEXT_PUBLIC_GOOGLE_MAPS_API_KEY to the deployment environment.');
        return;
      }

      try {
        setOptions({ key, v: 'weekly' });
        const { Map } = await importLibrary('maps') as google.maps.MapsLibrary;

        if (cancelled || !ref.current) return;

        const map = new Map(ref.current, {
          center: DEFAULT_CENTER,
          zoom: 14,
          mapTypeId: 'satellite',
          mapTypeControl: true,
          streetViewControl: false,
          fullscreenControl: true,
          clickableIcons: true,
          gestureHandling: 'greedy',
        });

        mapRef.current = map;

        const listener = map.addListener('click', (event: google.maps.MapMouseEvent) => {
          if (!event.latLng) return;
          setPoints((prev) => [...prev, [event.latLng.lat(), event.latLng.lng()]]);
        });
        listenersRef.current.push(listener);
      } catch (e) {
        console.error(e);
        setError('Google Maps could not be loaded. Check the API key, billing, API restrictions, and allowed website referrers.');
      }
    }

    void initMap();

    return () => {
      cancelled = true;
      listenersRef.current.forEach((listener) => listener.remove());
      listenersRef.current = [];
      polygonRef.current?.setMap(null);
      centerMarkerRef.current?.setMap(null);
      mapRef.current = null;
    };
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    polygonRef.current?.setMap(null);
    centerMarkerRef.current?.setMap(null);

    if (points.length === 0) {
      onChange?.(null, 0);
      return;
    }

    const path = points.map(([lat, lng]) => ({ lat, lng }));
    const center = path.reduce(
      (sum, point) => ({ lat: sum.lat + point.lat, lng: sum.lng + point.lng }),
      { lat: 0, lng: 0 }
    );
    center.lat /= path.length;
    center.lng /= path.length;

    centerMarkerRef.current = new google.maps.Circle({
      map,
      center,
      radius: 7,
      strokeColor: '#7ee2b1',
      strokeOpacity: 1,
      strokeWeight: 2,
      fillColor: '#7ee2b1',
      fillOpacity: 0.9,
      clickable: false,
    });

    if (points.length >= 3) {
      polygonRef.current = new google.maps.Polygon({
        map,
        paths: path,
        strokeColor: '#7ee2b1',
        strokeOpacity: 1,
        strokeWeight: 3,
        fillColor: '#7ee2b1',
        fillOpacity: 0.2,
        clickable: false,
      });

      const ring = points.map(([lat, lng]) => [lng, lat]);
      ring.push(ring[0]);

      const geometry: Geometry = {
        type: 'Polygon',
        coordinates: [ring],
      };

      onChange?.(geometry, areaHa(points));
    } else {
      onChange?.(null, 0);
    }
  }, [points, onChange]);

  const finish = () => {
    if (points.length < 3 || !onChange) return;
    const ring = points.map(([lat, lng]) => [lng, lat]);
    ring.push(ring[0]);
    onChange(
      { type: 'Polygon', coordinates: [ring] },
      areaHa(points)
    );
  };

  const clear = () => {
    setPoints([]);
    onChange?.(null, 0);
  };

  return (
    <div className="relative h-[520px]">
      <div ref={ref} className="h-full w-full rounded-2xl" />
      {error ? (
        <div className="absolute inset-0 z-[500] grid place-items-center rounded-2xl bg-[#07130f]/95 p-6 text-center">
          <div className="max-w-xl">
            <div className="text-sm font-bold text-[#ffcf8b]">Google Maps configuration required</div>
            <p className="mt-2 text-sm text-white/65">{error}</p>
            <p className="mt-3 text-xs text-white/40">
              Required environment variable: NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
            </p>
          </div>
        </div>
      ) : null}
      {!error && (
        <>
          <div className="absolute left-3 top-3 z-[500] rounded-xl border border-white/10 bg-[#07130f]/90 px-3 py-2 text-xs text-white/75">
            Google Maps Satellite · click to add farm boundary points
          </div>
          <div className="absolute bottom-3 left-3 z-[500] flex gap-2">
            <button onClick={finish} className="rounded-lg bg-[#8bcfa6] px-3 py-2 text-xs font-bold text-[#07130f]">
              Finish boundary
            </button>
            <button onClick={clear} className="rounded-lg border border-white/10 bg-[#07130f]/90 px-3 py-2 text-xs">
              Clear
            </button>
          </div>
          <div className="absolute bottom-3 right-3 z-[500] rounded-lg bg-[#07130f]/90 px-3 py-2 text-xs">
            {points.length} points
          </div>
        </>
      )}
    </div>
  );
}

function areaHa(points: [number, number][]) {
  if (points.length < 3) return 0;
  const R = 6378137;
  const rad = (x: number) => (x * Math.PI) / 180;
  let s = 0;

  for (let i = 0; i < points.length; i += 1) {
    const j = (i + 1) % points.length;
    s +=
      (rad(points[j][1]) - rad(points[i][1])) *
      (2 + Math.sin(rad(points[i][0])) + Math.sin(rad(points[j][0])));
  }

  return Math.abs((s * R * R) / 2) / 10000;
}
