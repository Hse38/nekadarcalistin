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

const baseUrl = () => getBaseUrl().replace(/\/$/, "");

const API_TIMEOUT_MS = 12000; // 12 saniye – backend uyuyorsa (Render) yeterli

const fetchWithTimeout = (url: string, options: RequestInit = {}, timeoutMs = API_TIMEOUT_MS): Promise<Response> => {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);
  return fetch(url, { ...options, signal: controller.signal }).finally(() => clearTimeout(id));
};

const api = (path: string, options?: RequestInit) => {
  const base = getBaseUrl();
  const url = base ? `${baseUrl()}${path}` : path;
  return fetchWithTimeout(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
};

/** FormData gönderir (Content-Type eklenmez, browser boundary ekler) */
const apiForm = (path: string, body: FormData, method = "POST") => {
  const base = getBaseUrl();
  const url = base ? `${baseUrl()}${path}` : path;
  return fetchWithTimeout(url, { method, body });
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
  async create(name: string, surname: string): Promise<Employee | null> {
    const form = new FormData();
    form.append("name", name);
    form.append("surname", surname);
    const res = await apiForm("/api/employees", form);
    if (!res.ok) return null;
    return res.json();
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
  async getById(id: number): Promise<Analysis | null> {
    const res = await api(`/api/analyses/${id}`);
    if (!res.ok) return null;
    const raw = await res.json();
    return mapAnalysis(raw);
  },
  async create(params: {
    employee_id: number;
    year: number;
    daily_working_hours: number;
    weekly_working_days: number;
    annual_leave_total?: number;
    annual_leave_used?: number;
    extra_leave_days?: number;
    holidays_data?: string;
    attendance_file?: File | null;
  }): Promise<Analysis | null> {
    const form = new FormData();
    form.append("employee_id", String(params.employee_id));
    form.append("year", String(params.year));
    form.append("daily_working_hours", String(params.daily_working_hours));
    form.append("weekly_working_days", String(params.weekly_working_days));
    form.append("annual_leave_total", String(params.annual_leave_total ?? 0));
    form.append("annual_leave_used", String(params.annual_leave_used ?? 0));
    form.append("extra_leave_days", String(params.extra_leave_days ?? 0));
    form.append("holidays_data", params.holidays_data ?? "[]");
    if (params.attendance_file) form.append("attendance_file", params.attendance_file);
    const res = await apiForm("/api/analyses", form);
    if (!res.ok) return null;
    const raw = await res.json();
    return mapAnalysis(raw);
  },
};

export function hasBackendUrl(): boolean {
  if (typeof window === "undefined") return false;
  return !!(process.env.NEXT_PUBLIC_API_URL?.trim());
}
