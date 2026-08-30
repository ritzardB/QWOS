type AttendanceHeaderProps = {
  onRefresh: () => void;
};

export function AttendanceHeader({
  onRefresh,
}: AttendanceHeaderProps) {
  return (
    <header className="qwos-page-header">
      <div>
        <p className="qwos-page-eyebrow">Workforce</p>
        <h1>Attendance</h1>
        <p>
          Manage employee attendance, clock-in, and clock-out activity.
        </p>
      </div>

      <button
        type="button"
        className="qwos-button qwos-button-secondary"
        onClick={onRefresh}
      >
        Refresh
      </button>
    </header>
  );
}