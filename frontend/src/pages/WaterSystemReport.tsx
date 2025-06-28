import React, { useState, useEffect, useMemo } from 'react';
import { useParams } from 'react-router-dom';
import { getSystemById, getSystemStatus, getSystemHistory, acknowledgeViolation } from '../api';
import type { WaterSystem } from '../types/WaterSystem';
import { DataTable } from '../components/shared/DataTable';
import { type ColumnDef } from '@tanstack/react-table';
import Button from '../components/shared/Button';
import { useAuth } from '../auth/AuthContext';

interface Violation {
  violation_id: string;
  violation_code: string;
  is_health_based_ind: string;
  contaminant_code: string;
  non_compl_per_begin_date: string;
  non_compl_per_end_date: string;
  violation_status: string;
}

interface SiteVisit {
  visit_id: string;
  visit_date: string;
  agency_type_code: string;
  visit_reason_code: string;
}

interface LcrSample {
  sample_id: string;
  sampling_end_date: string;
  result_sign_code: string;
  sample_measure: number;
}

interface EventMilestone {
  event_schedule_id: string;
  event_end_date: string;
  event_actual_date: string;
  event_milestone_code: string;
}

interface SystemHistory {
  violations: Violation[];
  site_visits: SiteVisit[];
  lcr_samples: LcrSample[];
  events_milestones: EventMilestone[];
}

const WaterSystemReport: React.FC = () => {
  const { pwsid } = useParams<{ pwsid: string }>();
  const [system, setSystem] = useState<WaterSystem | null>(null);
  const [status, setStatus] = useState('');
  const [history, setHistory] = useState<SystemHistory | null>(null);
  const [loading, setLoading] = useState(true);

  const handleAcknowledge = async (violationId: string) => {
    try {
      await acknowledgeViolation(violationId);
      // Refresh the history data
      if (pwsid) {
        const historyData = await getSystemHistory(pwsid);
        setHistory(historyData);
      }
    } catch (error) {
      console.error('Error acknowledging violation:', error);
    }
  };

  useEffect(() => {
    if (pwsid) {
      setLoading(true);
      const fetchSystemData = async () => {
        try {
          const [systemData, statusData, historyData] = await Promise.all([
            getSystemById(pwsid),
            getSystemStatus(pwsid),
            getSystemHistory(pwsid),
          ]);
          setSystem(systemData);
          setStatus(statusData);
          setHistory(historyData);
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

  const violationColumns = useMemo<ColumnDef<Violation>[]>(
    () => [
      { accessorKey: 'violation_id', header: 'ID' },
      { accessorKey: 'violation_code', header: 'Code' },
      { accessorKey: 'is_health_based_ind', header: 'Health-Based' },
      { accessorKey: 'contaminant_code', header: 'Contaminant' },
      { accessorKey: 'non_compl_per_begin_date', header: 'Start Date' },
      { accessorKey: 'non_compl_per_end_date', header: 'End Date' },
      { accessorKey: 'violation_status', header: 'Status' },
      {
        id: 'actions',
        cell: ({ row }) => {
          const { role } = useAuth();
          if (role !== 'Operator') {
            return null;
          }
          return (
            <Button
              onClick={() => handleAcknowledge(row.original.violation_id)}
              disabled={row.original.violation_status === 'Acknowledged'}
            >
              Acknowledge
            </Button>
          );
        },
      },
    ],
    []
  );

  const siteVisitColumns = useMemo<ColumnDef<SiteVisit>[]>(
    () => [
      { accessorKey: 'visit_id', header: 'ID' },
      { accessorKey: 'visit_date', header: 'Date' },
      { accessorKey: 'agency_type_code', header: 'Agency' },
      { accessorKey: 'visit_reason_code', header: 'Reason' },
    ],
    []
  );

  const lcrSampleColumns = useMemo<ColumnDef<LcrSample>[]>(
    () => [
      { accessorKey: 'sample_id', header: 'ID' },
      { accessorKey: 'sampling_end_date', header: 'Date' },
      { accessorKey: 'result_sign_code', header: 'Sign' },
      { accessorKey: 'sample_measure', header: 'Measure' },
    ],
    []
  );

  const eventMilestoneColumns = useMemo<ColumnDef<EventMilestone>[]>(
    () => [
      { accessorKey: 'event_schedule_id', header: 'ID' },
      { accessorKey: 'event_end_date', header: 'End Date' },
      { accessorKey: 'event_actual_date', header: 'Actual Date' },
      { accessorKey: 'event_milestone_code', header: 'Milestone' },
    ],
    []
  );

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
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
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

      {history && (
        <div className="space-y-8">
          <div>
            <h2 className="text-2xl font-semibold mb-4">Violations</h2>
            <DataTable columns={violationColumns} data={history.violations} />
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">Site Visits</h2>
            <DataTable columns={siteVisitColumns} data={history.site_visits} />
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">Lead & Copper Samples</h2>
            <DataTable columns={lcrSampleColumns} data={history.lcr_samples} />
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">Events & Milestones</h2>
            <DataTable columns={eventMilestoneColumns} data={history.events_milestones} />
          </div>
        </div>
      )}
    </div>
  );
};

export default WaterSystemReport;
