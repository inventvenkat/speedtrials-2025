import type { WaterSystem } from '../types/WaterSystem';

const API_BASE_URL = 'http://localhost:8000';

export const searchSystems = async (query: string): Promise<WaterSystem[]> => {
  const response = await fetch(`${API_BASE_URL}/systems/search?query=${query}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const getSystemById = async (pwsid: string): Promise<WaterSystem> => {
  const url = `${API_BASE_URL}/systems/by-id/${pwsid}`;
  console.log('Fetching system by ID from URL:', url);
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const getSystemStatus = async (pwsid: string): Promise<string> => {
  const response = await fetch(`${API_BASE_URL}/systems/${pwsid}/status`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const getStatistics = async (): Promise<any> => {
  const response = await fetch(`${API_BASE_URL}/statistics`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const getSystemByLocation = async (lat: number, lon: number): Promise<WaterSystem> => {
  const response = await fetch(`${API_BASE_URL}/systems/by-location?lat=${lat}&lon=${lon}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};
