import { useEffect, useState } from 'react';
import { supabase } from './supabase';
import { Map } from './Map';

type Farmer = {
  phone: string;
  crop: string;
  area_m2: number;
  lat: number;
  lon: number;
};

export default function App() {
  const [farmers, setFarmers] = useState<Farmer[]>([]);

  useEffect(() => {
    const fetchInitial = async () => {
      const { data } = await supabase.from('farmers').select('*');
      if (data) setFarmers(data as Farmer[]);
    };

    fetchInitial();

    const channel = supabase
      .channel('public:farmers')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'farmers' },
        (payload) => {
          setFarmers((prev) => {
            const others = prev.filter((f) => f.phone !== (payload.new as Farmer).phone);
            return [...others, payload.new as Farmer];
          });
        },
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  return (
    <main style={{ padding: '2rem' }}>
      <h1>IrrigaBot: Farmers ({farmers.length})</h1>
      <ul>
        {farmers.map((f) => (
          <li key={f.phone} className="status-info">
            {f.phone}: {f.crop} — {f.area_m2} m²
          </li>
        ))}
      </ul>

      <h2>Water Savings Heatmap</h2>
      <Map
        geojson={{
          type: 'FeatureCollection',
          features: farmers.map((f) => ({
            type: 'Feature',
            geometry: {
              type: 'Point',
              coordinates: [f.lon ?? 0, f.lat ?? 0],
            },
            properties: {
              weight: f.area_m2 / 1000, // crude weight proxy
            },
          })),
        }}
      />
    </main>
  );
}