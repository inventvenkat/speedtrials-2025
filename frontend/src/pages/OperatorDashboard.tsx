import React, { useMemo } from 'react';
import { DataTable } from '../components/shared/DataTable';
import { type ColumnDef } from '@tanstack/react-table';

type Violation = {
  id: string;
  type: string;
  date: string;
  status: string;
};

const violationsData: Violation[] = [
  { id: 'V001', type: 'Health-Based', date: '2024-05-20', status: 'Active' },
  { id: 'V002', type: 'Monitoring', date: '2024-05-15', status: 'Resolved' },
];

type Inspection = {
  id: string;
  date: string;
  type: string;
  result: string;
};

const inspectionsData: Inspection[] = [
  { id: 'I001', date: '2024-04-10', type: 'Routine', result: 'Passed' },
  { id: 'I002', date: '2024-02-22', type: 'Follow-up', result: 'Failed' },
];

export const OperatorDashboard: React.FC = () => {
  const violationColumns = useMemo<ColumnDef<Violation>[]>(
    () => [
      { accessorKey: 'id', header: 'ID' },
      { accessorKey: 'type', header: 'Type' },
      { accessorKey: 'date', header: 'Date' },
      { accessorKey: 'status', header: 'Status' },
    ],
    []
  );

  const inspectionColumns = useMemo<ColumnDef<Inspection>[]>(
    () => [
      { accessorKey: 'id', header: 'ID' },
      { accessorKey: 'date', header: 'Date' },
      { accessorKey: 'type', header: 'Type' },
      { accessorKey: 'result', header: 'Result' },
    ],
    []
  );

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Operator Dashboard</h1>
      <div className="space-y-8">
        <div>
          <h2 className="text-2xl font-semibold mb-4">Active Violations</h2>
          <DataTable columns={violationColumns} data={violationsData} />
        </div>
        <div>
          <h2 className="text-2xl font-semibold mb-4">Inspection History</h2>
          <DataTable columns={inspectionColumns} data={inspectionsData} />
        </div>
      </div>
    </div>
  );
};
