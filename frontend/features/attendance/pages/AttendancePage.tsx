import { useEffect, useState } from "react";

import {
  listWorkSchedules,
} from "../api/attendanceApi";

import { ClockInOutPanel } from "../components/ClockInOutPanel";

import type {
  WorkSchedule,
} from "../types/attendance";

import { AppShell } from "../../../layouts/AppShell";

type AttendancePageProps = {
  onLogout: () => void;
};

export function AttendancePage({
  onLogout,
}: AttendancePageProps) {
  const [employeeId, setEmployeeId] = useState("");
  const [schedules, setSchedules] = useState<
    WorkSchedule[]
  >([]);
  const [loadingSchedules, setLoadingSchedules] =
    useState(true);
  const [scheduleError, setScheduleError] =
    useState("");

  useEffect(() => {
    async function loadSchedules(): Promise<void> {
      setLoadingSchedules(true);
      setScheduleError("");

      try {
        const data = await listWorkSchedules();
        setSchedules(data);
      } catch (error) {
        if (error instanceof Error) {
          setScheduleError(error.message);
        } else {
          setScheduleError(
            "Unable to load work schedules.",
          );
        }
      } finally {
        setLoadingSchedules(false);
      }
    }

    void loadSchedules();
  }, []);

  return (
    <AppShell onLogout={onLogout}>
      <section className="qwos-dashboard">
        <header className="qwos-page-header">
          <div>
            <p className="qwos-page-eyebrow">
              Workforce
            </p>

            <h1>Attendance</h1>

            <p>
              Manage employee attendance, clock events,
              and work schedules.
            </p>
          </div>
        </header>

        <section className="qwos-attendance-content">
          <div className="qwos-attendance-card">
            <div className="qwos-attendance-card-header">
              <div>
                <h2>Employee Attendance</h2>

                <p>
                  Enter an employee ID to record
                  attendance.
                </p>
              </div>
            </div>

            <div className="qwos-attendance-form">
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
              />
            </div>

            {employeeId.trim() ? (
              <ClockInOutPanel
                employeeId={employeeId.trim()}
              />
            ) : (
              <div className="qwos-attendance-empty">
                Enter an employee ID to enable
                Clock In and Clock Out.
              </div>
            )}
          </div>

          <div className="qwos-attendance-card">
            <div className="qwos-attendance-card-header">
              <div>
                <h2>Work Schedules</h2>

                <p>
                  Work schedules configured for the
                  current tenant.
                </p>
              </div>
            </div>

            {loadingSchedules && (
              <div className="qwos-attendance-empty">
                Loading work schedules...
              </div>
            )}

            {scheduleError && (
              <div
                className="qwos-attendance-error"
                role="alert"
              >
                {scheduleError}
              </div>
            )}

            {!loadingSchedules &&
              !scheduleError &&
              schedules.length === 0 && (
                <div className="qwos-attendance-empty">
                  No work schedules have been configured.
                </div>
              )}

            {!loadingSchedules &&
              !scheduleError &&
              schedules.length > 0 && (
                <div className="qwos-schedule-list">
                  {schedules.map((schedule) => (
                    <article
                      key={schedule.id}
                      className="qwos-schedule-item"
                    >
                      <div>
                        <strong>
                          {schedule.schedule_name}
                        </strong>

                        <span>
                          {schedule.schedule_code}
                        </span>
                      </div>

                      <div>
                        <span>
                          {schedule.timezone}
                        </span>

                        <span>
                          {schedule.is_active
                            ? "Active"
                            : "Inactive"}
                        </span>
                      </div>
                    </article>
                  ))}
                </div>
              )}
          </div>
        </section>
      </section>
    </AppShell>
  );
}