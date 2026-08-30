import {
  getAuthenticatedHeaders,
  handleAuthenticationFailure,
} from "../../../api/apiClient";

import type {
  ClockInRequest,
  ClockInResponse,
  ClockOutRequest,
  ClockOutResponse,
  CreateEmployeeWorkArrangementRequest,
  CreateEmployeeWorkArrangementResponse,
  CreateEmployeeWorkScheduleRequest,
  CreateEmployeeWorkScheduleResponse,
  CreateWorkScheduleDayRequest,
  CreateWorkScheduleDayResponse,
  WorkSchedule,
  WorkScheduleDay,
} from "../types/attendance";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "http://localhost:8000/api/v1";

async function attendanceRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(
    `${API_BASE_URL}/attendance${path}`,
    {
      ...options,
      headers: {
        ...getAuthenticatedHeaders(),
        "Content-Type": "application/json",
        ...options.headers,
      },
    },
  );

  handleAuthenticationFailure(response);

  const contentType = response.headers.get(
    "content-type",
  );

  const data = contentType?.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    const message =
      data?.detail?.message ??
      data?.detail ??
      data?.message ??
      `Attendance request failed (${response.status})`;

    throw new Error(message);
  }

  return data as T;
}

export async function clockIn(
  request: ClockInRequest,
): Promise<ClockInResponse> {
  return attendanceRequest<ClockInResponse>(
    "/clock-in",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export async function clockOut(
  request: ClockOutRequest,
): Promise<ClockOutResponse> {
  return attendanceRequest<ClockOutResponse>(
    "/clock-out",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export async function listWorkSchedules(): Promise<
  WorkSchedule[]
> {
  const response =
    await attendanceRequest<{
      items: WorkSchedule[];
      total: number;
    }>("/work-schedules");

  return response.items;
}

export async function getWorkSchedule(
  workScheduleId: string,
): Promise<WorkSchedule> {
  return attendanceRequest<WorkSchedule>(
    `/work-schedules/${workScheduleId}`,
  );
}

export async function listWorkScheduleDays(
  workScheduleId: string,
): Promise<WorkScheduleDay[]> {
  const response =
    await attendanceRequest<{
      items: WorkScheduleDay[];
      total: number;
    }>(
      `/work-schedules/${workScheduleId}/days`,
    );

  return response.items;
}

export async function createEmployeeWorkArrangement(
  employeeId: string,
  request: CreateEmployeeWorkArrangementRequest,
): Promise<CreateEmployeeWorkArrangementResponse> {
  return attendanceRequest<CreateEmployeeWorkArrangementResponse>(
    `/employees/${employeeId}/work-arrangements`,
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export async function createEmployeeWorkSchedule(
  employeeId: string,
  request: CreateEmployeeWorkScheduleRequest,
): Promise<CreateEmployeeWorkScheduleResponse> {
  return attendanceRequest<CreateEmployeeWorkScheduleResponse>(
    `/employees/${employeeId}/work-schedules`,
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export async function createWorkScheduleDay(
  workScheduleId: string,
  request: CreateWorkScheduleDayRequest,
): Promise<CreateWorkScheduleDayResponse> {
  return attendanceRequest<CreateWorkScheduleDayResponse>(
    `/work-schedules/${workScheduleId}/days`,
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}