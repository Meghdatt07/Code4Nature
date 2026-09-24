'use client';

import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

type Geometry = { type: 'Polygon'; coordinates: number[][][] };
type Props = { value?: Geometry; onChange?: (geometry: Geometry | null, areaHa: number) => void };

const DEFAULT_CENTER: [number, number] = [23.2135, 72.6840];

export default function FarmMap({ value, onChange }: Props) {
  const ref = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<L.Map | null>(null);
  const polygonRef = useRef<L.Polygon | null>(null);
  const markersRef = useRef<L.CircleMarker[]>([]);
  const [points, setPoints] = useState<[number, number][]>(() =>
    value?.coordinates?.[0]?.map(([lng, lat]) => [lat, lng] as [number, number]) || []
  );

  useEffect(() => {
    if (!ref.current || mapRef.current) return;

    const map = L.map(ref.current, {
      center: DEFAULT_CENTER,
      zoom: 14,
      zoomControl: true,
      scrollWheelZoom: true,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map);

    map.on('click', (event) => {
      setPoints((previous) => [...previous, [event.latlng.lat, event.latlng.lng]]);
    });

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
      polygonRef.current = null;
      markersRef.current = [];
    };
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    polygonRef.current?.remove();
    polygonRef.current = null;
    markersRef.current.forEach((marker) => marker.remove());
    markersRef.current = [];

    points.forEach((point, index) => {
      const marker = L.circleMarker(point, {
        radius: 6,
        color: '#7ee2b1',
        weight: 2,
        fillColor: '#7ee2b1',
        fillOpacity: 0.9,
      }).addTo(map);

      marker.bindTooltip(String(index + 1), {
        permanent: false,
        direction: 'top',
      });

      markersRef.current.push(marker);
    });

    if (points.length >= 2) {
      polygonRef.current = L.polygon(points, {
        color: '#7ee2b1',
        weight: 3,
        fillColor: '#7ee2b1',
        fillOpacity: 0.18,
      }).addTo(map);

      map.fitBounds(polygonRef.current.getBounds(), { padding: [25, 25] });

      if (points.length >= 3) {
        const ring = points.map(([lat, lng]) => [lng, lat]);
        ring.push(ring[0]);

        onChange?.(
          {
            type: 'Polygon',
            coordinates: [ring],
          },
          areaHa(points)
        );
      }
    } else {
      onChange?.(null, 0);
    }
  }, [points, onChange]);

  useEffect(() => {
    if (!value?.coordinates?.[0]) return;
    const next = value.coordinates[0]
      .slice(0, -1)
      .map(([lng, lat]) => [lat, lng] as [number, number]);

    if (next.length >= 3) {
      setPoints(next);
    }
  }, [value]);

  const finish = () => {
    if (points.length < 3) return;

    const ring = points.map(([lat, lng]) => [lng, lat]);
    ring.push(ring[0]);

    onChange?.(
      {
        type: 'Polygon',
        coordinates: [ring],
      },
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

      <div className="absolute left-3 top-3 z-[500] rounded-xl border border-white/10 bg-[#07130f]/90 px-3 py-2 text-xs text-white/75">
        OpenStreetMap · click to add farm boundary points
      </div>

      <div className="absolute bottom-3 left-3 z-[500] flex gap-2">
        <button
          onClick={finish}
          className="rounded-lg bg-[#8bcfa6] px-3 py-2 text-xs font-bold text-[#07130f]"
        >
          Finish boundary
        </button>
        <button
          onClick={clear}
          className="rounded-lg border border-white/10 bg-[#07130f]/90 px-3 py-2 text-xs"
        >
          Clear
        </button>
      </div>

      <div className="absolute bottom-3 right-3 z-[500] rounded-lg bg-[#07130f]/90 px-3 py-2 text-xs">
        {points.length} points
      </div>
    </div>
  );
}

function areaHa(points: [number, number][]) {
  if (points.length < 3) return 0;

  const R = 6378137;
  const rad = (value: number) => (value * Math.PI) / 180;
  let sum = 0;

  for (let i = 0; i < points.length; i += 1) {
    const j = (i + 1) % points.length;
    sum +=
      (rad(points[j][1]) - rad(points[i][1])) *
      (2 + Math.sin(rad(points[i][0])) + Math.sin(rad(points[j][0])));
  }

  return Math.abs((sum * R * R) / 2) / 10000;
}
