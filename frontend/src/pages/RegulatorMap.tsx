import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Dummy data for water systems
const waterSystems = [
  { id: 1, name: 'Atlanta Water Works', position: [33.7490, -84.3880], status: 'compliant' },
  { id: 2, name: 'Savannah Public Water', position: [32.0809, -81.0912], status: 'non-compliant' },
  { id: 3, name: 'Athens-Clarke County Water', position: [33.9609, -83.3779], status: 'compliant' },
];

// Fix for default icon issue with webpack
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

const getMarkerColor = (status: string) => {
  return status === 'compliant' ? 'green' : 'red';
};

export const RegulatorMap: React.FC = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Regulator Field Kit - Georgia</h1>
      <MapContainer center={[32.1656, -82.9001]} zoom={7} style={{ height: '70vh', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {waterSystems.map(system => (
          <Marker
            key={system.id}
            position={system.position as L.LatLngExpression}
            icon={L.icon({
              iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${getMarkerColor(system.status)}.png`,
              shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            })}
          >
            <Popup>
              <div className="p-2">
                <h3 className="font-bold text-lg">{system.name}</h3>
                <p>Status: <span className={`font-semibold ${system.status === 'compliant' ? 'text-green-600' : 'text-red-600'}`}>{system.status}</span></p>
                <a href={`/report/${system.id}`} className="text-blue-500 hover:underline">View Report</a>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};
