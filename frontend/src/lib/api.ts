/**
 * API client for HR Analysis backend.
 * Base URL: NEXT_PUBLIC_API_URL or fallback to relative /api (for rewrites).
 */

const getBaseUrl = () => {
  if (typeof window !== "undefined") {
    return process.env.NEXT_PUBLIC_API_URL ?? "";
  }
  return process.env.NEXT_PUBLIC_API_URL ?? "";
};

const api = (path: string, options?: RequestInit) => {
  const base = getBaseUrl();
  const url = base ? `${base.replace(/\/$/, "")}${path}` : path;
  return fetch(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
};

// --- Types (aligned with backend) ---

export interface Employee {
  id: number;
  name: string;
  surname: string;
  created_at?: string;
}

export interface Analysis {
  id: number;
  employee_id: number;
  year: number;
  theoretical_hours: number;
  actual_hours: number;
  efficiency_percentage: number;
  created_at?: string;
}

// Map backend response to frontend shape
function mapAnalysis(raw: {
  id: number;
  employee_id: number;
  year: number;
  theoretical_working_hours?: number | null;
  actual_working_hours?: number | null;
  [key: string]: unknown;
}): Analysis {
  const theoretical = raw.theoretical_working_hours ?? 0;
  const actual = raw.actual_working_hours ?? 0;
  const efficiency = theoretical > 0 ? (actual / theoretical) * 100 : 0;
  return {
    id: raw.id,
    employee_id: raw.employee_id,
    year: raw.year,
    theoretical_working_hours: raw.theoretical_working_hours,
    actual_working_hours: raw.actual_working_hours,
    theoretical_hours: theoretical,
    actual_hours: actual,
    efficiency_percentage: efficiency,
    created_at: raw.created_at as string | undefined,
  };
}

// --- Employees ---

export const employeeApi = {
  async getAll(): Promise<Employee[]> {
    const res = await api("/api/employees");
    if (!res.ok) return [];
    const data = await res.json();
    return data.employees ?? [];
  },
};

// --- Analyses ---

export const analysisApi = {
  async getAll(): Promise<Analysis[]> {
    const res = await api("/api/analyses");
    if (!res.ok) return [];
    const data = await res.json();
    const list = data.analyses ?? [];
    return list.map(mapAnalysis);
  },
};
