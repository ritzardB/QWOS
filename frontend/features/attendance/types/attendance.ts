export type ClockInRequest = {
  clock_in_at?: string | null;
  event_source?: string;
  notes?: string | null;
};

export type ClockOutRequest = {
  clock_out_at?: string | null;
  event_source?: string;
  notes?: string | null;
};

export type ClockInResponse = {
  attendance_record_id: string;
  attendance_event_id: string;
  employee_id: string;
  attendance_date: string;
  clock_in_at: string | null;
  status: string;
  event_type: string;
  event_at: string;
};

export type ClockOutResponse = {
  attendance_record_id: string;
  attendance_event_id: string;
  employee_id: string;
  attendance_date: string;
  clock_in_at: string | null;
  clock_out_at: string;
  worked_minutes: number;
  status: string;
  event_type: string;
  event_at: string;
};

export type WorkSchedule = {
  id: string;
  schedule_code: string;
  schedule_name: string;
  timezone: string;
  is_active: boolean;
  created_at: string;
};

export type WorkScheduleDay = {
  id: string;
  work_schedule_id: string;
  day_of_week: number;
  day_type: string;
  start_time: string | null;
  end_time: string | null;
  break_minutes: number;
  is_overnight: boolean;
  created_at: string;
};

export type CreateEmployeeWorkArrangementRequest = {
  work_arrangement?: string;
  effective_from: string;
  effective_until?: string | null;
  is_active?: boolean;
};

export type CreateEmployeeWorkArrangementResponse = {
  id: string;
  employee_id: string;
  work_arrangement: string;
  effective_from: string;
  effective_until: string | null;
  is_active: boolean;
  created_at: string;
};

export type CreateEmployeeWorkScheduleRequest = {
  work_schedule_id: string;
  effective_from: string;
  effective_until?: string | null;
  is_active?: boolean;
};

export type CreateEmployeeWorkScheduleResponse = {
  id: string;
  employee_id: string;
  work_schedule_id: string;
  effective_from: string;
  effective_until: string | null;
  is_active: boolean;
  created_at: string;
};

export type CreateWorkScheduleDayRequest = {
  day_of_week: number;
  day_type?: string;
  start_time?: string | null;
  end_time?: string | null;
  break_minutes?: number;
  is_overnight?: boolean;
};

export type CreateWorkScheduleDayResponse = {
  id: string;
  work_schedule_id: string;
  day_of_week: number;
  day_type: string;
  start_time: string | null;
  end_time: string | null;
  break_minutes: number;
  is_overnight: boolean;
  created_at: string;
};

export interface AttendanceHistoryItem {
  attendance_record_id: string;
  employee_id: string;
  attendance_date: string;
  status: string;
  clock_in_at: string | null;
  clock_out_at: string | null;
  worked_minutes: number;
  late_minutes: number;
  undertime_minutes: number;
  overtime_minutes: number;
  notes: string | null;
}
export interface ListAttendanceHistoryResponse {
  items: AttendanceHistoryItem[];
  total: number;
}
