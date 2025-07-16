import { useEffect, useRef } from 'react';
import mapboxgl, { GeoJSONSource, Map as MapboxMap } from 'mapbox-gl';

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN as string;

interface Props {
  geojson: GeoJSON.FeatureCollection;
}

export function Map({ geojson }: Props) {
  const mapRef = useRef<MapboxMap | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);

  // initialise map only once
  useEffect(() => {
    if (containerRef.current && !mapRef.current) {
      mapRef.current = new mapboxgl.Map({
        container: containerRef.current,
        style: 'mapbox://styles/mapbox/light-v11',
        center: [0, 0],
        zoom: 1.3,
      });

      mapRef.current.on('load', () => {
        if (!mapRef.current?.getSource('farmers')) {
          mapRef.current?.addSource('farmers', {
            type: 'geojson',
            data: geojson,
          });

          mapRef.current?.addLayer({
            id: 'heat',
            type: 'heatmap',
            source: 'farmers',
            paint: {
              'heatmap-weight': ['get', 'weight'],
              'heatmap-radius': 20,
              'heatmap-intensity': 0.8,
              'heatmap-color': [
                'interpolate',
                ['linear'],
                ['heatmap-density'],
                0, 'rgba(33,102,172,0)',
                0.2, 'rgb(103,169,207)',
                0.4, 'rgb(209,229,240)',
                0.6, 'rgb(253,219,199)',
                0.8, 'rgb(239,138,98)',
                1, 'rgb(178,24,43)'
              ],
            },
          });
        }
      });
    }
  }, []);

  // update source when geojson changes
  useEffect(() => {
    const source = mapRef.current?.getSource('farmers') as GeoJSONSource | undefined;
    if (source) {
      source.setData(geojson);
    }
  }, [geojson]);

  return <div ref={containerRef} style={{ width: '100%', height: '500px' }} />;
}