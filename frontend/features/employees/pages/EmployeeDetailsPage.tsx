import { useEffect, useState } from "react";

import { AppShell } from "../../../layouts/AppShell";
import { EmployeeDocuments } from "../components/EmployeeDocuments";
import {
  getEmployee,
  getEmployeeManager,
  getEmployeePosition,
  getEmployeeProfile,
  listEmployeeImmigration,
} from "../api/employeesApi";
import type {
  Employee,
  EmployeeImmigration,
  EmployeeManager,
  EmployeePosition,
  EmployeeProfile,
} from "../types/employee";

type EmployeeDetailsPageProps = {
  employeeId: string;
  onLogout: () => void;
};

function formatDate(value: string | null): string {
  if (!value) {
    return "—";
  }

  return new Intl.DateTimeFormat("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(new Date(`${value}T00:00:00`));
}

function formatEmploymentType(value: string): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase(),
    );
}

function formatLabel(value: string): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase(),
    );
}

function displayValue(value: string | null): string {
  return value ?? "—";
}

function formatImmigrationType(value: string): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase(),
    );
}

function getImmigrationState(
  expiryDate: string | null,
): "active" | "expiring" | "expired" {
  if (!expiryDate) {
    return "active";
  }

  const today = new Date();
  const expiry = new Date(
    `${expiryDate}T00:00:00`,
  );

  const difference =
    expiry.getTime() - today.getTime();

  const daysRemaining = Math.ceil(
    difference / (1000 * 60 * 60 * 24),
  );

  if (daysRemaining < 0) {
    return "expired";
  }

  if (daysRemaining <= 30) {
    return "expiring";
  }

  return "active";
}

function getDaysUntilExpiry(
  expiryDate: string | null,
): number | null {
  if (!expiryDate) {
    return null;
  }

  const today = new Date();
  const expiry = new Date(
    `${expiryDate}T00:00:00`,
  );

  return Math.ceil(
    (expiry.getTime() - today.getTime()) /
      (1000 * 60 * 60 * 24),
  );
}

export function EmployeeDetailsPage({
  employeeId,
  onLogout,
}: EmployeeDetailsPageProps) {
  const [employee, setEmployee] =
    useState<Employee | null>(null);

  const [profile, setProfile] =
    useState<EmployeeProfile | null>(null);

  const [position, setPosition] =
    useState<EmployeePosition | null>(null);

  const [manager, setManager] =
    useState<EmployeeManager | null>(null);

  const [immigration, setImmigration] =
    useState<EmployeeImmigration[]>([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState<string | null>(
    null,
  );

  useEffect(() => {
    let cancelled = false;

    async function loadEmployeeDetails(): Promise<void> {
      try {
        setLoading(true);
        setError(null);

        const [
          employeeData,
          profileData,
          positionData,
          managerData,
          immigrationData,
        ] = await Promise.all([
          getEmployee(employeeId),
          getEmployeeProfile(employeeId),
          getEmployeePosition(employeeId),
          getEmployeeManager(employeeId),
          listEmployeeImmigration(employeeId),
        ]);

        if (!cancelled) {
          setEmployee(employeeData);
          setProfile(profileData);
          setPosition(positionData);
          setManager(managerData);
          setImmigration(immigrationData);
        }
      } catch (error) {
        if (!cancelled) {
          setError(
            error instanceof Error
              ? error.message
              : "Unable to load employee details.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadEmployeeDetails();

    return () => {
      cancelled = true;
    };
  }, [employeeId]);

  function goBack(): void {
    window.history.pushState(
      {},
      "",
      "/employees",
    );

    window.dispatchEvent(
      new PopStateEvent("popstate"),
    );
  }

  const isTopLevelEmployee =
    !manager?.manager_employee_id &&
    position?.organizational_level === "executive";

  return (
    <AppShell onLogout={onLogout}>
      <section className="employee-details-page">
        <button
          type="button"
          className="employee-back-button"
          onClick={goBack}
        >
          ← Back to Employees
        </button>

        {loading && (
          <section className="hr-loading-state">
            <div className="hr-loading-spinner" />
            <p>Loading employee details...</p>
          </section>
        )}

        {error && (
          <section className="hr-error-state">
            <h2>Unable to load employee</h2>
            <p>{error}</p>
          </section>
        )}

        {!loading &&
          !error &&
          employee && (
            <>
              <header className="employee-details-header">
                <div>
                  <p className="employees-eyebrow">
                    Employee
                  </p>

                  <h1>
                    {employee.employee_number}
                  </h1>

                  <p>
                    {employee.work_email ??
                      "No work email"}
                  </p>
                </div>

                <div className="employee-details-status">
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
              </header>

              <section className="employee-detail-grid">
                {/* -----------------------------------------------------------------
                    Employment
                ------------------------------------------------------------------ */}
                <article className="employee-detail-panel">
                  <h2>Employment</h2>

                  <div className="employee-detail-row">
                    <span>Employee Number</span>
                    <strong>
                      {employee.employee_number}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Hire Date</span>
                    <strong>
                      {formatDate(
                        employee.hire_date,
                      )}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Status</span>
                    <strong>
                      {employee.employment_status}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Employment Type</span>
                    <strong>
                      {formatEmploymentType(
                        employee.employment_type,
                      )}
                    </strong>
                  </div>
                </article>

                {/* -----------------------------------------------------------------
                    Position
                ------------------------------------------------------------------ */}
                <article className="employee-detail-panel">
                  <h2>Position</h2>

                  <div className="employee-detail-row">
                    <span>Job Title</span>
                    <strong>
                      {position?.job_title ?? "—"}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Organizational Level</span>
                    <strong>
                      {position
                        ? formatLabel(
                            position.organizational_level,
                          )
                        : "—"}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Effective From</span>
                    <strong>
                      {position
                        ? formatDate(
                            position.effective_from,
                          )
                        : "—"}
                    </strong>
                  </div>
                </article>

                {/* -----------------------------------------------------------------
                    Work Contact
                ------------------------------------------------------------------ */}
                <article className="employee-detail-panel">
                  <h2>Work Contact</h2>

                  <div className="employee-detail-row">
                    <span>Email</span>
                    <strong>
                      {displayValue(
                        employee.work_email,
                      )}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Phone</span>
                    <strong>
                      {displayValue(
                        employee.work_phone,
                      )}
                    </strong>
                  </div>
                </article>

                {/* -----------------------------------------------------------------
                    Personal Profile
                ------------------------------------------------------------------ */}
                <article className="employee-detail-panel">
                  <h2>Personal Profile</h2>

                  <div className="employee-detail-row">
                    <span>Date of Birth</span>
                    <strong>
                      {formatDate(
                        profile?.date_of_birth ??
                          null,
                      )}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Gender</span>
                    <strong>
                      {displayValue(
                        profile?.gender ?? null,
                      )}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Nationality</span>
                    <strong>
                      {displayValue(
                        profile?.nationality ?? null,
                      )}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Marital Status</span>
                    <strong>
                      {displayValue(
                        profile?.marital_status ??
                          null,
                      )}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Personal Email</span>
                    <strong>
                      {displayValue(
                        profile?.personal_email ??
                          null,
                      )}
                    </strong>
                  </div>

                  <div className="employee-detail-row">
                    <span>Personal Phone</span>
                    <strong>
                      {displayValue(
                        profile?.personal_phone ??
                          null,
                      )}
                    </strong>
                  </div>
                </article>

                {/* -----------------------------------------------------------------
                    Reporting
                ------------------------------------------------------------------ */}
                <article className="employee-detail-panel">
                  <h2>Reporting</h2>

                  {isTopLevelEmployee ? (
                    <div className="employee-top-level">
                      <strong>
                        Top-Level Executive
                      </strong>

                      <span>
                        No manager relationship
                      </span>
                    </div>
                  ) : (
                    <>
                      <div className="employee-detail-row">
                        <span>Manager</span>
                        <strong>
                          {manager
                            ?.manager_employee_number ??
                            "—"}
                        </strong>
                      </div>

                      <div className="employee-detail-row">
                        <span>Relationship</span>
                        <strong>
                          {manager
                            ? formatLabel(
                                manager.relationship_type ??
                                  "",
                              )
                            : "—"}
                        </strong>
                      </div>

                      <div className="employee-detail-row">
                        <span>Effective From</span>
                        <strong>
                          {manager
                            ? formatDate(
                                manager.effective_from,
                              )
                            : "—"}
                        </strong>
                      </div>
                    </>
                  )}
                </article>

                {/* -----------------------------------------------------------------
                    Immigration
                ------------------------------------------------------------------ */}
                <article className="employee-detail-panel employee-immigration-panel">
                  <div className="employee-panel-heading">
                    <div>
                      <h2>Immigration</h2>

                      <p className="employee-panel-description">
                        Immigration and work
                        authorization records.
                      </p>
                    </div>

                    <span className="employee-record-count">
                      {immigration.length}
                    </span>
                  </div>

                  {immigration.length === 0 ? (
                    <div className="employee-inline-empty">
                      <strong>
                        No immigration records
                      </strong>

                      <span>
                        No immigration information
                        is currently available for
                        this employee.
                      </span>
                    </div>
                  ) : (
                    <div className="employee-immigration-list">
                      {immigration.map((record) => {
                        const state =
                          getImmigrationState(
                            record.expiry_date,
                          );

                        const daysUntilExpiry =
                          getDaysUntilExpiry(
                            record.expiry_date,
                          );

                        return (
                          <div
                            key={record.id}
                            className="employee-immigration-item"
                          >
                            <div className="employee-immigration-header">
                              <div>
                                <h3>
                                  {formatImmigrationType(
                                    record.immigration_type,
                                  )}
                                </h3>

                                {record.document_number && (
                                  <p>
                                    {
                                      record.document_number
                                    }
                                  </p>
                                )}
                              </div>

                              <span
                                className={`employee-immigration-status employee-immigration-status-${state}`}
                              >
                                {state ===
                                  "expired" &&
                                  "Expired"}

                                {state ===
                                  "expiring" &&
                                  "Expiring Soon"}

                                {state ===
                                  "active" &&
                                  "Active"}
                              </span>
                            </div>

                            <div className="employee-detail-row">
                              <span>
                                Issue Date
                              </span>

                              <strong>
                                {formatDate(
                                  record.issue_date,
                                )}
                              </strong>
                            </div>

                            <div className="employee-detail-row">
                              <span>
                                Expiry Date
                              </span>

                              <strong>
                                {formatDate(
                                  record.expiry_date,
                                )}
                              </strong>
                            </div>

                            {daysUntilExpiry !==
                              null &&
                              state ===
                                "expiring" && (
                                <div className="employee-immigration-warning">
                                  ⚠ Expires in{" "}
                                  {
                                    daysUntilExpiry
                                  }{" "}
                                  {daysUntilExpiry ===
                                  1
                                    ? "day"
                                    : "days"}
                                </div>
                              )}

                            {record.sponsor_name && (
                              <div className="employee-detail-row">
                                <span>
                                  Sponsor
                                </span>

                                <strong>
                                  {
                                    record.sponsor_name
                                  }
                                </strong>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </article>

                {/* -----------------------------------------------------------------
                    Documents
                    Full-width panel directly below Immigration
                ------------------------------------------------------------------ */}
                <EmployeeDocuments
                  employeeId={employeeId}
                  immigration={immigration}
                />
              </section>
            </>
          )}
      </section>
    </AppShell>
  );
}