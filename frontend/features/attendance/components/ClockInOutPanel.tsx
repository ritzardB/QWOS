import { useState } from "react";

import {
  clockIn,
  clockOut,
} from "../api/attendanceApi";

import type {
  ClockInResponse,
  ClockOutResponse,
} from "../types/attendance";

type ClockInOutPanelProps = {
  employeeId: string;
};

export function ClockInOutPanel({
  employeeId,
}: ClockInOutPanelProps) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [attendance, setAttendance] =
    useState<ClockInResponse | ClockOutResponse | null>(
      null,
    );

  async function handleClockIn(): Promise<void> {
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const response = await clockIn({
        employee_id: employeeId,
        event_source: "web",
      });

      setAttendance(response);
      setMessage(
        `Clocked in successfully at ${formatDateTime(
          response.event_at,
        )}.`,
      );
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  async function handleClockOut(): Promise<void> {
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const response = await clockOut({
        employee_id: employeeId,
        event_source: "web",
      });

      setAttendance(response);
      setMessage(
        `Clocked out successfully at ${formatDateTime(
          response.clock_out_at,
        )}.`,
      );
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="qwos-attendance-panel">
      <div className="qwos-attendance-panel-header">
        <div>
          <h2>Attendance</h2>
          <p>
            Record the employee's working time.
          </p>
        </div>

        <span className="qwos-attendance-status">
          {attendance?.status ?? "Not recorded"}
        </span>
      </div>

      <div className="qwos-attendance-actions">
        <button
          type="button"
          className="qwos-attendance-button qwos-attendance-button-clock-in"
          onClick={handleClockIn}
          disabled={loading}
        >
          {loading ? "Processing..." : "Clock In"}
        </button>

        <button
          type="button"
          className="qwos-attendance-button qwos-attendance-button-clock-out"
          onClick={handleClockOut}
          disabled={loading}
        >
          {loading ? "Processing..." : "Clock Out"}
        </button>
      </div>

      {message && (
        <p className="qwos-attendance-message">
          {message}
        </p>
      )}

      {error && (
        <p
          className="qwos-attendance-error"
          role="alert"
        >
          {error}
        </p>
      )}

      {attendance && (
        <div className="qwos-attendance-summary">
          <div>
            <span>Attendance date</span>
            <strong>
              {attendance.attendance_date}
            </strong>
          </div>

          <div>
            <span>Event</span>
            <strong>
              {attendance.event_type}
            </strong>
          </div>

          {isClockOutResponse(attendance) && (
            <div>
              <span>Worked time</span>
              <strong>
                {formatWorkedMinutes(
                  attendance.worked_minutes,
                )}
              </strong>
            </div>
          )}
        </div>
      )}
    </section>
  );
}

function isClockOutResponse(
  response: ClockInResponse | ClockOutResponse,
): response is ClockOutResponse {
  return "worked_minutes" in response;
}

function formatDateTime(
  value: string,
): string {
  return new Date(value).toLocaleString();
}

function formatWorkedMinutes(
  minutes: number,
): string {
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;

  if (hours === 0) {
    return `${remainingMinutes} min`;
  }

  return `${hours}h ${remainingMinutes}m`;
}

function getErrorMessage(
  error: unknown,
): string {
  if (error instanceof Error) {
    return error.message;
  }

  return "Unable to process attendance request.";
}