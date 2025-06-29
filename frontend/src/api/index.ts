import type { WaterSystem } from '../types/WaterSystem';

const API_BASE_URL = 'https://3dd0-108-91-116-214.ngrok-free.app';

const apiFetch = async (url: string, options: RequestInit = {}) => {
  const headers = {
    ...options.headers,
    'ngrok-skip-browser-warning': 'true',
  };

  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const searchSystems = async (query: string): Promise<WaterSystem[]> => {
  return apiFetch(`${API_BASE_URL}/systems/search?query=${query}`);
};

export const getSystemById = async (pwsid: string): Promise<WaterSystem> => {
  const url = `${API_BASE_URL}/systems/by-id/${pwsid}`;
  console.log('Fetching system by ID from URL:', url);
  return apiFetch(url);
};

export const getSystemStatus = async (pwsid: string): Promise<string> => {
  return apiFetch(`${API_BASE_URL}/systems/${pwsid}/status`);
};

export const getStatistics = async (): Promise<any> => {
  return apiFetch(`${API_BASE_URL}/statistics`);
};

export const getSystemByLocation = async (lat: number, lon: number): Promise<WaterSystem> => {
  return apiFetch(`${API_BASE_URL}/systems/by-location?lat=${lat}&lon=${lon}`);
};

export const getSystemHistory = async (pwsid: string): Promise<any> => {
  return apiFetch(`${API_BASE_URL}/api/systems/${pwsid}/history`);
};

export const acknowledgeViolation = async (violationId: string): Promise<any> => {
  const token = localStorage.getItem('token');
  return apiFetch(`${API_BASE_URL}/api/violations/${violationId}/acknowledge`, {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};
