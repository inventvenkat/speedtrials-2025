import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import type { WaterSystem } from '../types/WaterSystem';
import { searchSystems, getStatistics, getSystemByLocation, getSystemStatus } from '../api';

const HomePage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState<WaterSystem[]>([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ total_systems: 0, total_systems_with_violations: 0, active_systems_with_violations: 0 });
  const [locationSystem, setLocationSystem] = useState<WaterSystem | null>(null);
  const [locationStatus, setLocationStatus] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await getStatistics();
        setStats(data);
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    };
    fetchStats();

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;
        try {
          const system = await getSystemByLocation(latitude, longitude);
          setLocationSystem(system);
          if (system) {
            const status = await getSystemStatus(system.pwsid);
            setLocationStatus(status);
          }
        } catch (error) {
          console.error('Error fetching location status:', error);
        }
      });
    }
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await searchSystems(searchQuery);
      setResults(data);
    } catch (error) {
      console.error('Error fetching search results:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold text-center my-8">
        Georgia Water Quality
      </h1>
      {locationSystem ? (
        <Link to={`/report/${locationSystem.pwsid}`}>
          <div className={`p-4 border rounded text-center mb-8 ${locationStatus === 'safe' ? 'bg-green-200' : 'bg-red-200'} hover:bg-gray-100 cursor-pointer`}>
            <h2 className="text-2xl font-bold">
              Based on your location, your local water is {locationStatus} to drink.
            </h2>
            <p>(Click to see the full report for {locationSystem.pws_name})</p>
          </div>
        </Link>
      ) : (
        <div className="p-4 border rounded text-center mb-8 bg-yellow-200">
          <h2 className="text-2xl font-bold">
            Location-based search is only available in Georgia.
          </h2>
        </div>
      )}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center mb-8">
        <div className="p-4 border rounded-lg shadow-md">
          <h2 className="text-2xl font-bold flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h6m-6 4h6m-6 4h6" />
            </svg>
            {stats.total_systems}
          </h2>
          <p>Total Water Systems</p>
        </div>
        <div className="p-4 border rounded-lg shadow-md">
          <h2 className="text-2xl font-bold flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            {stats.total_systems_with_violations}
          </h2>
          <p>Total Systems with Health-Based Violations</p>
        </div>
        <div className="p-4 border rounded-lg shadow-md">
          <h2 className="text-2xl font-bold flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            {stats.active_systems_with_violations}
          </h2>
          <p>Active Systems with Health-Based Violations</p>
        </div>
      </div>
      <form onSubmit={handleSearch} className="flex justify-center">
        <div className="relative w-1/2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="border border-gray-300 rounded-full p-2 pl-10 w-full"
            placeholder="Search by Water System Name, ID, or Zip Code"
          />
          <div className="absolute top-0 left-0 inline-flex items-center p-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white rounded-full p-2 ml-2"
          disabled={loading}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>
      <div className="mt-8">
        {results.map((system, index) => (
          <Link to={`/report/${system.pwsid}`} key={`${system.pwsid}-${index}`}>
            <div className="border-b p-4 hover:bg-gray-100 cursor-pointer">
              <h2 className="text-xl font-bold">{system.pws_name}</h2>
              <p>{system.pwsid} - {system.city_name}, {system.zip_code}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
