import "./App.css";

import { AppShell } from "../layouts/AppShell";
import { ActivityPanel } from "../features/dashboard/components/ActivityPanel";
import { DashboardHeader } from "../features/dashboard/components/DashboardHeader";
import { MetricCard } from "../features/dashboard/components/MetricCard";
import { QuickActions } from "../features/dashboard/components/QuickActions";
import { dashboardMetrics } from "../features/dashboard/dashboardData";

function App() {
  return (
    <AppShell>
      <section className="qwos-dashboard">
        <DashboardHeader userName="Richard" />

        <section
          className="qwos-metrics"
          aria-label="Workforce overview"
        >
          {dashboardMetrics.map((metric) => (
            <MetricCard
              key={metric.label}
              label={metric.label}
              value={metric.value}
              description={metric.description}
              icon={metric.icon}
            />
          ))}
        </section>

        <section className="qwos-dashboard-grid">
          <QuickActions />
          <ActivityPanel />
        </section>
      </section>
    </AppShell>
  );
}

export default App;