-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 032_attendance_records.sql
-- Version     : 1.0
-- Description : Daily employee attendance records
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- ATTENDANCE RECORDS
-- =============================================================================

CREATE TABLE attendance_records (

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
    -- Pay Period
    ---------------------------------------------------------------------------

    pay_period_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Attendance Date
    ---------------------------------------------------------------------------

    attendance_date DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Attendance Status
    --
    -- Examples:
    --
    --     present
    --     absent
    --     late
    --     on_leave
    --     holiday
    --     rest_day
    --     incomplete
    --
    ---------------------------------------------------------------------------

    status identifier_code
        NOT NULL
        DEFAULT 'present',

    ---------------------------------------------------------------------------
    -- Attendance Times
    ---------------------------------------------------------------------------

    clock_in_at TIMESTAMPTZ,

    clock_out_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Attendance Calculations
    ---------------------------------------------------------------------------

    worked_minutes INTEGER
        NOT NULL
        DEFAULT 0,

    late_minutes INTEGER
        NOT NULL
        DEFAULT 0,

    undertime_minutes INTEGER
        NOT NULL
        DEFAULT 0,

    overtime_minutes INTEGER
        NOT NULL
        DEFAULT 0,

    ---------------------------------------------------------------------------
    -- Notes
    ---------------------------------------------------------------------------

    notes TEXT,

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

    CONSTRAINT fk_attendance_records_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_attendance_records_pay_period
        FOREIGN KEY (pay_period_id)
        REFERENCES pay_periods(id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_attendance_records_employee_date
        UNIQUE (
            tenant_id,
            employee_id,
            attendance_date
        ),

    CONSTRAINT chk_attendance_records_worked_minutes
        CHECK (
            worked_minutes >= 0
        ),

    CONSTRAINT chk_attendance_records_late_minutes
        CHECK (
            late_minutes >= 0
        ),

    CONSTRAINT chk_attendance_records_undertime_minutes
        CHECK (
            undertime_minutes >= 0
        ),

    CONSTRAINT chk_attendance_records_overtime_minutes
        CHECK (
            overtime_minutes >= 0
        ),

    CONSTRAINT chk_attendance_records_clock_times
        CHECK (
            clock_out_at IS NULL
            OR clock_in_at IS NULL
            OR clock_out_at >= clock_in_at
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_attendance_records_employee
    ON attendance_records(employee_id);

CREATE INDEX idx_attendance_records_pay_period
    ON attendance_records(pay_period_id);

CREATE INDEX idx_attendance_records_date
    ON attendance_records(attendance_date);

CREATE INDEX idx_attendance_records_status
    ON attendance_records(status);

COMMIT;