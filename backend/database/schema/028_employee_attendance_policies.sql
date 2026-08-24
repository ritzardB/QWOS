-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 028_employee_attendance_policies.sql
-- Version     : 1.0
-- Description : Effective-dated employee attendance policy assignments
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE ATTENDANCE POLICIES
-- =============================================================================

CREATE TABLE employee_attendance_policies (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Attendance Policy
    ---------------------------------------------------------------------------

    attendance_policy_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    effective_from DATE NOT NULL,

    effective_until DATE,

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    is_active BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    ---------------------------------------------------------------------------
    -- Audit
    ---------------------------------------------------------------------------

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    created_by CHAR(26),

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    updated_by CHAR(26),

    deleted_at TIMESTAMPTZ,

    deleted_by CHAR(26),

    ---------------------------------------------------------------------------
    -- Concurrency
    ---------------------------------------------------------------------------

    version INTEGER
        NOT NULL
        DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Constraints
    ---------------------------------------------------------------------------

    CONSTRAINT fk_employee_attendance_policies_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_employee_attendance_policies_policy
        FOREIGN KEY (attendance_policy_id)
        REFERENCES attendance_policies(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_attendance_policies_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        ),

    CONSTRAINT uq_employee_attendance_policies_start
        UNIQUE (
            tenant_id,
            employee_id,
            effective_from
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employee_attendance_policies_employee
    ON employee_attendance_policies(employee_id);

CREATE INDEX idx_employee_attendance_policies_policy
    ON employee_attendance_policies(attendance_policy_id);

CREATE INDEX idx_employee_attendance_policies_active
    ON employee_attendance_policies(is_active);

CREATE INDEX idx_employee_attendance_policies_effective
    ON employee_attendance_policies(
        employee_id,
        effective_from,
        effective_until
    );

COMMIT;