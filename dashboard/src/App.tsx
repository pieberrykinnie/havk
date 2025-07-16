import { useEffect, useState } from 'react';
import { supabase } from './supabase';

type Farmer = {
  phone: string;
  crop: string;
  area_m2: number;
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
    <main style={{ fontFamily: 'sans-serif', padding: '2rem' }}>
      <h1>IrrigaBot: Farmers ({farmers.length})</h1>
      <ul>
        {farmers.map((f) => (
          <li key={f.phone}>
            {f.phone}: {f.crop} — {f.area_m2} m²
          </li>
        ))}
      </ul>
    </main>
  );
}