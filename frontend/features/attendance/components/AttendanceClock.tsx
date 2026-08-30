import { useState } from "react";

import {
  clockIn,
  clockOut,
} from "../api/attendanceApi";

type AttendanceClockProps = {
  onAttendanceChange: () => void;
};

export function AttendanceClock({
  onAttendanceChange,
}: AttendanceClockProps) {
  const [employeeId, setEmployeeId] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(
    null,
  );
  const [error, setError] = useState<string | null>(
    null,
  );

  async function handleClockIn(): Promise<void> {
    if (!employeeId.trim()) {
      setError("Please enter an employee ID.");
      return;
    }

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      const response = await clockIn({
        employee_id: employeeId.trim(),
        event_source: "web",
      });

      setMessage(
        `Clocked in successfully at ${formatDateTime(
          response.clock_in_at,
        )}.`,
      );

      onAttendanceChange();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  async function handleClockOut(): Promise<void> {
    if (!employeeId.trim()) {
      setError("Please enter an employee ID.");
      return;
    }

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      const response = await clockOut({
        employee_id: employeeId.trim(),
        event_source: "web",
      });

      setMessage(
        `Clocked out successfully. Worked ${formatWorkedMinutes(
          response.worked_minutes,
        )}.`,
      );

      onAttendanceChange();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="qwos-card">
      <div className="qwos-card-header">
        <div>
          <h2>Clock In / Clock Out</h2>
          <p>
            Record an employee attendance event.
          </p>
        </div>
      </div>

      <div className="qwos-attendance-clock">
        <label htmlFor="attendance-employee-id">
          Employee ID
        </label>

        <input
          id="attendance-employee-id"
          type="text"
          value={employeeId}
          onChange={(event) =>
            setEmployeeId(event.target.value)
          }
          placeholder="Enter employee ULID"
          disabled={loading}
        />

        <div className="qwos-attendance-actions">
          <button
            type="button"
            className="qwos-button qwos-button-primary"
            onClick={handleClockIn}
            disabled={loading}
          >
            {loading ? "Processing..." : "Clock In"}
          </button>

          <button
            type="button"
            className="qwos-button qwos-button-secondary"
            onClick={handleClockOut}
            disabled={loading}
          >
            {loading ? "Processing..." : "Clock Out"}
          </button>
        </div>

        {message && (
          <p className="qwos-success-message">
            {message}
          </p>
        )}

        {error && (
          <p className="qwos-error-message">
            {error}
          </p>
        )}
      </div>
    </section>
  );
}

function formatDateTime(
  value: string | null,
): string {
  if (!value) {
    return "the recorded time";
  }

  return new Date(value).toLocaleString();
}

function formatWorkedMinutes(
  minutes: number,
): string {
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;

  if (hours === 0) {
    return `${remainingMinutes} minutes`;
  }

  return `${hours}h ${remainingMinutes}m`;
}

function getErrorMessage(
  error: unknown,
): string {
  if (error instanceof Error) {
    return error.message;
  }

  return "Unable to process the attendance request.";
}