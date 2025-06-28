import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getSystemById, getSystemStatus } from '../api';
import type { WaterSystem } from '../types/WaterSystem';

const WaterSystemReport: React.FC = () => {
  const { pwsid } = useParams<{ pwsid: string }>();
  const [system, setSystem] = useState<WaterSystem | null>(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (pwsid) {
      setLoading(true);
      const fetchSystemData = async () => {
        try {
          const [systemData, statusData] = await Promise.all([
            getSystemById(pwsid),
            getSystemStatus(pwsid),
          ]);
          setSystem(systemData);
          setStatus(statusData);
        } catch (error) {
          console.error('Error fetching water system data:', error);
        } finally {
          setLoading(false);
        }
      };
      fetchSystemData();
    } else {
      setLoading(false);
    }
  }, [pwsid]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!system) {
    return <div>Water system not found.</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold text-center my-8">{system.pws_name}</h1>
      <div className={`p-4 border rounded text-center mb-8 ${status === 'safe' ? 'bg-green-200' : 'bg-red-200'}`}>
        <h2 className="text-2xl font-bold">
          {status === 'safe' ? 'Safe to Drink' : 'Not Safe to Drink'}
        </h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="p-4 border rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">System Details</h2>
          <p><strong>PWSID:</strong> {system.pwsid}</p>
          <p><strong>City:</strong> {system.city_name}</p>
          <p><strong>Zip Code:</strong> {system.zip_code}</p>
        </div>
        <div className="p-4 border rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">Contact Information</h2>
          {system.org_name && <p><strong>Organization:</strong> {system.org_name}</p>}
          {system.admin_name && system.admin_name !== system.org_name && <p><strong>Administrator:</strong> {system.admin_name}</p>}
          {system.email_addr && <p><strong>Email:</strong> <a href={`mailto:${system.email_addr}`} className="text-blue-500 hover:underline">{system.email_addr}</a></p>}
          {system.phone_number && <p><strong>Phone:</strong> <a href={`tel:${system.phone_number}`} className="text-blue-500 hover:underline">{system.phone_number}</a></p>}
          {system.alt_phone_number && <p><strong>Alternate Phone:</strong> <a href={`tel:${system.alt_phone_number}`} className="text-blue-500 hover:underline">{system.alt_phone_number}</a></p>}
          {system.fax_number && <p><strong>Fax:</strong> {system.fax_number}</p>}
          {!system.org_name && !system.admin_name && !system.email_addr && !system.phone_number && !system.alt_phone_number && !system.fax_number && <p>No contact information available.</p>}
        </div>
      </div>
    </div>
  );
};

export default WaterSystemReport;
