import { useEffect, useState } from "react";

import {
  clockInMe,
  clockOutMe,
  getMyAttendanceHistory,
} from "../api/attendanceApi";

import type {
  AttendanceHistoryItem,
  ClockInResponse,
  ClockOutResponse,
} from "../types/attendance";

export function ClockInOutPanel() {
  const [loading, setLoading] = useState(false);
  const [loadingAttendance, setLoadingAttendance] =
    useState(true);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [attendance, setAttendance] =
    useState<ClockInResponse | ClockOutResponse | AttendanceHistoryItem | null>(
      null,
    );

  useEffect(() => {
    async function loadAttendance(): Promise<void> {
      setLoadingAttendance(true);
      setError("");

      try {
        const response = await getMyAttendanceHistory();

        if (response.items.length > 0) {
          const latest = [...response.items].sort(
            (a, b) =>
              new Date(b.attendance_date).getTime() -
              new Date(a.attendance_date).getTime(),
          )[0];

          setAttendance(latest);
        } else {
          setAttendance(null);
        }
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setLoadingAttendance(false);
      }
    }

    void loadAttendance();
  }, []);

  async function refreshAttendance(): Promise<void> {
    try {
      const response = await getMyAttendanceHistory();

      if (response.items.length > 0) {
        const latest = [...response.items].sort(
          (a, b) =>
            new Date(b.attendance_date).getTime() -
            new Date(a.attendance_date).getTime(),
        )[0];

        setAttendance(latest);
      } else {
        setAttendance(null);
      }
    } catch (err) {
      setError(getErrorMessage(err));
    }
  }

  async function handleClockIn(): Promise<void> {
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const response = await clockInMe({
        event_source: "web",
      });

      setAttendance(response);

      setMessage(
        `Clocked in successfully at ${formatDateTime(
          response.event_at,
        )}.`,
      );

      await refreshAttendance();
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
      const response = await clockOutMe({
        event_source: "web",
      });

      setAttendance(response);

      setMessage(
        `Clocked out successfully at ${formatDateTime(
          response.clock_out_at,
        )}.`,
      );

      await refreshAttendance();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  if (loadingAttendance) {
    return (
      <section className="qwos-attendance-panel">
        <div className="qwos-attendance-panel-header">
          <div>
            <h2>Attendance</h2>
            <p>
              Record your working time.
            </p>
          </div>

          <span className="qwos-attendance-status">
            Loading...
          </span>
        </div>
      </section>
    );
  }

  return (
    <section className="qwos-attendance-panel">
      <div className="qwos-attendance-panel-header">
        <div>
          <h2>Attendance</h2>

          <p>
            Record your working time.
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
            <span>Clock In</span>
            <strong>
              {attendance.clock_in_at
                ? formatDateTime(attendance.clock_in_at)
                : "—"}
            </strong>
          </div>

          <div>
            <span>Status</span>
            <strong>
              {attendance.status}
            </strong>
          </div>

          {"clock_out_at" in attendance && (
            <div>
              <span>Clock Out</span>
              <strong>
                {attendance.clock_out_at
                  ? formatDateTime(
                      attendance.clock_out_at,
                    )
                  : "—"}
              </strong>
            </div>
          )}

          {"worked_minutes" in attendance && (
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