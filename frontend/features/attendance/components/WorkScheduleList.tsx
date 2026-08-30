import type { WorkSchedule } from "../types/attendance";

type WorkScheduleListProps = {
  schedules: WorkSchedule[];
  loading: boolean;
  error: string | null;
  onSelect: (schedule: WorkSchedule) => void;
};

export function WorkScheduleList({
  schedules,
  loading,
  error,
  onSelect,
}: WorkScheduleListProps) {
  return (
    <section className="qwos-card">
      <div className="qwos-card-header">
        <div>
          <h2>Work Schedules</h2>
          <p>
            View the work schedules configured for this tenant.
          </p>
        </div>
      </div>

      {loading && (
        <p className="qwos-loading-message">
          Loading work schedules...
        </p>
      )}

      {error && (
        <p className="qwos-error-message">
          {error}
        </p>
      )}

      {!loading && !error && schedules.length === 0 && (
        <div className="qwos-empty-state">
          <h3>No work schedules</h3>
          <p>
            No work schedules have been configured yet.
          </p>
        </div>
      )}

      {!loading && !error && schedules.length > 0 && (
        <div className="qwos-table-wrapper">
          <table className="qwos-table">
            <thead>
              <tr>
                <th>Code</th>
                <th>Name</th>
                <th>Timezone</th>
                <th>Status</th>
                <th />
              </tr>
            </thead>

            <tbody>
              {schedules.map((schedule) => (
                <tr key={schedule.id}>
                  <td>{schedule.schedule_code}</td>
                  <td>{schedule.schedule_name}</td>
                  <td>{schedule.timezone}</td>
                  <td>
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
                  </td>
                  <td>
                    <button
                      type="button"
                      className="qwos-button qwos-button-small"
                      onClick={() =>
                        onSelect(schedule)
                      }
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}