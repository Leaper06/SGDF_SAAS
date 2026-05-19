export interface Camp {
  id: string;
  unit_id: string | null;
  name: string;
  location: string | null;
  start_date: string; // ISO String (ex: 2026-05-23T14:32:02)
  end_date: string;
  created_at: string;
}

export interface ApiResponse<T> {
  status: string;
  count: number;
  data: T;
}