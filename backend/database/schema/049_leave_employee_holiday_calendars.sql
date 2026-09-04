-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 049_leave_employee_holiday_calendars.sql
-- Version     : 1.0
-- Description : Effective-dated employee holiday calendar assignments
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Assigns a holiday calendar to an employee for a defined effective period.
--
-- This allows QWOS to determine which holidays apply to an employee when
-- calculating leave request days.
--
-- Example:
--
--     Employee
--          │
--          └── Holiday Calendar Assignment
--                    │
--                    └── UAE Abu Dhabi Calendar
--
-- The assignment is effective-dated so historical calendar assignments remain
-- auditable.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE HOLIDAY CALENDAR ASSIGNMENTS
-- =============================================================================

CREATE TABLE leave_employee_holiday_calendars (

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
    -- Holiday Calendar
    ---------------------------------------------------------------------------

    holiday_calendar_id CHAR(26) NOT NULL,

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

    CONSTRAINT fk_leave_employee_holiday_calendars_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_employee_holiday_calendars_calendar
        FOREIGN KEY (holiday_calendar_id)
        REFERENCES leave_holiday_calendars(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_leave_employee_holiday_calendars_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        ),

    CONSTRAINT uq_leave_employee_holiday_calendars_start
        UNIQUE (
            tenant_id,
            employee_id,
            effective_from
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_employee_holiday_calendars_employee
    ON leave_employee_holiday_calendars(
        employee_id
    );

CREATE INDEX idx_leave_employee_holiday_calendars_calendar
    ON leave_employee_holiday_calendars(
        holiday_calendar_id
    );

CREATE INDEX idx_leave_employee_holiday_calendars_effective
    ON leave_employee_holiday_calendars(
        employee_id,
        effective_from,
        effective_until
    );

CREATE INDEX idx_leave_employee_holiday_calendars_active
    ON leave_employee_holiday_calendars(
        is_active
    );

COMMIT;