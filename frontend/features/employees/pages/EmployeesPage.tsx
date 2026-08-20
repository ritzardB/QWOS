import { useEffect, useState } from "react";

import { AppShell } from "../../../layouts/AppShell";
import { listEmployees } from "../api/employeesApi";
import { EmployeeList } from "../components/EmployeeList";
import type { Employee } from "../types/employee";

type EmployeesPageProps = {
  onLogout: () => void;
};

export function EmployeesPage({
  onLogout,
}: EmployeesPageProps) {
  const [employees, setEmployees] = useState<Employee[]>(
    [],
  );

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(
    null,
  );

  useEffect(() => {
    let cancelled = false;

    async function loadEmployees(): Promise<void> {
      try {
        setLoading(true);
        setError(null);

        const data = await listEmployees();

        if (!cancelled) {
          setEmployees(data);
        }
      } catch (error) {
        if (!cancelled) {
          setError(
            error instanceof Error
              ? error.message
              : "Unable to load employees.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadEmployees();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <AppShell onLogout={onLogout}>
      <section className="employees-page">
        <header className="employees-page-header">
          <div>
            <p className="employees-eyebrow">
              Workforce
            </p>

            <h1>Employees</h1>

            <p>
              Manage your workforce and employee records.
            </p>
          </div>

          <div className="employees-page-summary">
            <strong>
              {loading ? "—" : employees.length}
            </strong>
            <span>Active employees</span>
          </div>
        </header>

        {loading && (
          <section className="hr-loading-state">
            <div className="hr-loading-spinner" />
            <p>Loading employees...</p>
          </section>
        )}

        {error && (
          <section className="hr-error-state">
            <h2>Unable to load employees</h2>
            <p>{error}</p>
          </section>
        )}

        {!loading && !error && (
          <EmployeeList employees={employees} />
        )}
      </section>
    </AppShell>
  );
}