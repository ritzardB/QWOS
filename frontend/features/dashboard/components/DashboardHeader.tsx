type DashboardHeaderProps = {
  userName: string;
};

export function DashboardHeader({
  userName,
}: DashboardHeaderProps) {
  return (
    <header className="qwos-dashboard-header">
      <div>
        <p className="qwos-eyebrow">
          Quantum Workforce OS
        </p>

        <h1 className="qwos-dashboard-title">
          Welcome back, {userName}
        </h1>

        <p className="qwos-dashboard-description">
          Your workforce operations, connected in one intelligent
          system.
        </p>
      </div>

      <div className="qwos-dashboard-status">
        <span className="qwos-status-indicator" />
        <span>System operational</span>
      </div>
    </header>
  );
}