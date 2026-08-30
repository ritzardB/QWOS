import { useEffect, useState } from "react";

import "./App.css";

import { ActivityPanel } from "../features/dashboard/components/ActivityPanel";
import { DashboardHeader } from "../features/dashboard/components/DashboardHeader";
import { MetricCard } from "../features/dashboard/components/MetricCard";
import { QuickActions } from "../features/dashboard/components/QuickActions";
import { dashboardMetrics } from "../features/dashboard/dashboardData";
import { LoginPage } from "../features/auth/components/LoginPage";
import { EmployeesPage } from "../features/employees/pages/EmployeesPage";
import { AppShell } from "../layouts/AppShell";
import { EmployeeDetailsPage } from "../features/employees/pages/EmployeeDetailsPage";
import { AttendancePage } from "../features/attendance/pages/AttendancePage";

import {
  clearAuthentication,
  getRefreshToken,
  isAuthenticated,
} from "../features/auth/authStorage";

import { logout } from "../api/identity";

function Dashboard({
  onLogout,
}: {
  onLogout: () => void;
}) {
  return (
    <AppShell onLogout={onLogout}>
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

function App() {
  const [authenticated, setAuthenticated] =
    useState(isAuthenticated);

  const [pathname, setPathname] = useState(
    window.location.pathname,
  );

  useEffect(() => {
    function handlePopState(): void {
      setPathname(window.location.pathname);
    }

    window.addEventListener(
      "popstate",
      handlePopState,
    );

    return () => {
      window.removeEventListener(
        "popstate",
        handlePopState,
      );
    };
  }, []);

  async function handleLogout(): Promise<void> {
    const refreshToken = getRefreshToken();

    try {
      if (refreshToken) {
        await logout({
          refresh_token: refreshToken,
        });
      }
    } catch (error) {
      console.error("Logout request failed:", error);
    } finally {
      clearAuthentication();
      setAuthenticated(false);
    }
  }

  if (!authenticated) {
    return (
      <LoginPage
        onLoginSuccess={() => setAuthenticated(true)}
      />
    );
  }

  if (pathname === "/employees") {
  return (
    <EmployeesPage onLogout={handleLogout} />
  );
}

if (pathname === "/attendance") {
  return (
    <AttendancePage onLogout={handleLogout} />
  );
}

if (pathname.startsWith("/employees/")) {
  const employeeId = pathname.split("/")[2];

  if (employeeId) {
    return (
      <EmployeeDetailsPage
        employeeId={employeeId}
        onLogout={handleLogout}
      />
    );
  }
}

  return <Dashboard onLogout={handleLogout} />;
}

export default App;