import type { KeyboardEvent } from "react";

import type { Employee } from "../types/employee";

type EmployeeListProps = {
  employees: Employee[];
};

function formatEmploymentType(value: string): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase(),
    );
}

function openEmployee(employeeId: string): void {
  window.history.pushState(
    {},
    "",
    `/employees/${employeeId}`,
  );

  window.dispatchEvent(
    new PopStateEvent("popstate"),
  );
}

function handleEmployeeKeyDown(
  event: KeyboardEvent<HTMLElement>,
  employeeId: string,
): void {
  if (
    event.key === "Enter" ||
    event.key === " "
  ) {
    event.preventDefault();
    openEmployee(employeeId);
  }
}

export function EmployeeList({
  employees,
}: EmployeeListProps) {
  if (employees.length === 0) {
    return (
      <section className="hr-empty-state">
        <h2>No employees found</h2>
        <p>
          There are no active employees in the current
          tenant.
        </p>
      </section>
    );
  }

  return (
    <section className="employee-list">
      {employees.map((employee) => (
        <article
          key={employee.id}
          className="employee-card"
          role="button"
          tabIndex={0}
          onClick={() => openEmployee(employee.id)}
          onKeyDown={(event) =>
            handleEmployeeKeyDown(
              event,
              employee.id,
            )
          }
        >
          <div className="employee-card-main">
            <div className="employee-avatar">
              {employee.employee_number
                .replace("QW-", "")
                .slice(-2)}
            </div>

            <div className="employee-identity">
              <h2>{employee.employee_number}</h2>

              <p className="employee-email">
                {employee.work_email ??
                  "No work email"}
              </p>
            </div>
          </div>

          <div className="employee-card-meta">
            <span
              className={`employee-status employee-status-${employee.employment_status}`}
            >
              {employee.employment_status}
            </span>

            <span>
              {formatEmploymentType(
                employee.employment_type,
              )}
            </span>
          </div>
        </article>
      ))}
    </section>
  );
}