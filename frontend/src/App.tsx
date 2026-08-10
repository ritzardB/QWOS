import "./App.css";
import { AppShell } from "../layouts/AppShell";

function App() {
  return (
    <AppShell>
      <section className="qwos-dashboard">
        <header className="qwos-dashboard-header">
          <p className="qwos-eyebrow">Quantum Workforce OS</p>

          <h1 className="qwos-dashboard-title">
            Welcome to QWOS
          </h1>

          <p className="qwos-dashboard-description">
            Your workforce operations, connected in one intelligent
            system.
          </p>
        </header>

        <div className="qwos-metrics">
          <div className="qwos-card">
            <p className="qwos-card-label">Employees</p>
            <p className="qwos-card-value">—</p>
            <p className="qwos-card-description">
              Workforce data
            </p>
          </div>

          <div className="qwos-card">
            <p className="qwos-card-label">Attendance</p>
            <p className="qwos-card-value">—</p>
            <p className="qwos-card-description">
              Today's activity
            </p>
          </div>

          <div className="qwos-card">
            <p className="qwos-card-label">Leave</p>
            <p className="qwos-card-value">—</p>
            <p className="qwos-card-description">
              Pending requests
            </p>
          </div>

          <div className="qwos-card">
            <p className="qwos-card-label">Notifications</p>
            <p className="qwos-card-value">—</p>
            <p className="qwos-card-description">
              System updates
            </p>
          </div>
        </div>
      </section>
    </AppShell>
  );
}

export default App;