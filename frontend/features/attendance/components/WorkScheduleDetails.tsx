import type {
  WorkSchedule,
  WorkScheduleDay,
} from "../types/attendance";

type WorkScheduleDetailsProps = {
  schedule: WorkSchedule | null;
  days: WorkScheduleDay[];
  loading: boolean;
  error: string | null;
};

const dayNames = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];

export function WorkScheduleDetails({
  schedule,
  days,
  loading,
  error,
}: WorkScheduleDetailsProps) {
  if (!schedule) {
    return (
      <section className="qwos-card">
        <div className="qwos-empty-state">
          <h3>Select a work schedule</h3>
          <p>
            Choose a schedule from the list to view its
            weekly configuration.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="qwos-card">
      <div className="qwos-card-header">
        <div>
          <p className="qwos-page-eyebrow">
            Schedule
          </p>

          <h2>{schedule.schedule_name}</h2>

          <p>
            {schedule.schedule_code} ·{" "}
            {schedule.timezone}
          </p>
        </div>

        <span
          className={
            schedule.is_active
              ? "qwos-status qwos-status-active"
              : "qwos-status"
          }
        >
          {schedule.is_active
            ? "Active"
            : "Inactive"}
        </span>
      </div>

      {loading && (
        <p className="qwos-loading-message">
          Loading schedule days...
        </p>
      )}

      {error && (
        <p className="qwos-error-message">
          {error}
        </p>
      )}

      {!loading && !error && (
        <div className="qwos-schedule-days">
          {dayNames.map((dayName, index) => {
            const day = days.find(
              (item) =>
                item.day_of_week === index + 1,
            );

            return (
              <div
                key={dayName}
                className="qwos-schedule-day"
              >
                <div>
                  <strong>{dayName}</strong>
                </div>

                {!day && (
                  <span className="qwos-muted">
                    Not configured
                  </span>
                )}

                {day && (
                  <div className="qwos-schedule-day-details">
                    <span>{day.day_type}</span>

                    {day.start_time &&
                      day.end_time && (
                        <span>
                          {day.start_time} –{" "}
                          {day.end_time}
                        </span>
                      )}

                    <span>
                      Break: {day.break_minutes} min
                    </span>

                    {day.is_overnight && (
                      <span>Overnight</span>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}