-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 044_leave_request_days.sql
-- Version     : 1.0
-- Description : Individual day details for employee leave requests
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores the individual dates that make up a leave request.
--
-- Leave Request
--     = Overall leave request and requested date range
--
-- Leave Request Day
--     = Individual day within that request
--
-- This allows QWOS to distinguish:
--     - Working days
--     - Rest days
--     - Public holidays
--     - Full-day leave
--     - Half-day leave
--     - Partial-day leave
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE REQUEST DAYS
-- =============================================================================

CREATE TABLE leave_request_days (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Request
    ---------------------------------------------------------------------------

    leave_request_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Date
    ---------------------------------------------------------------------------

    leave_date DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Day Classification
    --
    -- working_day  = scheduled working day
    -- rest_day     = employee's scheduled day off
    -- holiday      = recognized public/company holiday
    ---------------------------------------------------------------------------

    day_type identifier_code NOT NULL DEFAULT 'working_day',

    ---------------------------------------------------------------------------
    -- Leave Duration
    --
    -- full_day = complete working day
    -- half_day = half working day
    -- partial  = partial working day
    ---------------------------------------------------------------------------

    duration_type identifier_code NOT NULL DEFAULT 'full_day',

    ---------------------------------------------------------------------------
    -- Leave Quantity
    --
    -- Normally:
    --     full_day = 1.00
    --     half_day = 0.50
    --
    -- Partial leave can use another approved fraction.
    ---------------------------------------------------------------------------

    leave_days NUMERIC(10,2) NOT NULL,

    ---------------------------------------------------------------------------
    -- Optional Time Details
    --
    -- Used when the employee takes partial-day leave.
    ---------------------------------------------------------------------------

    start_time TIME,

    end_time TIME,

    ---------------------------------------------------------------------------
    -- Reason / Notes
    ---------------------------------------------------------------------------

    notes TEXT,

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

    CONSTRAINT fk_leave_request_days_request
        FOREIGN KEY (leave_request_id)
        REFERENCES leave_requests(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_days_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_leave_request_days_leave_days
        CHECK (
            leave_days > 0
        ),

    CONSTRAINT chk_leave_request_days_day_type
        CHECK (
            day_type IN (
                'working_day',
                'rest_day',
                'holiday'
            )
        ),

    CONSTRAINT chk_leave_request_days_duration_type
        CHECK (
            duration_type IN (
                'full_day',
                'half_day',
                'partial'
            )
        ),

    CONSTRAINT chk_leave_request_days_time_range
        CHECK (
            (
                start_time IS NULL
                AND end_time IS NULL
            )
            OR
            (
                start_time IS NOT NULL
                AND end_time IS NOT NULL
                AND end_time > start_time
            )
        ),

    CONSTRAINT uq_leave_request_days_date
        UNIQUE (
            leave_request_id,
            leave_date
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_request_days_request
    ON leave_request_days(
        leave_request_id
    );

CREATE INDEX idx_leave_request_days_employee
    ON leave_request_days(
        employee_id
    );

CREATE INDEX idx_leave_request_days_date
    ON leave_request_days(
        employee_id,
        leave_date
    );

CREATE INDEX idx_leave_request_days_type
    ON leave_request_days(
        day_type
    );

CREATE INDEX idx_leave_request_days_active
    ON leave_request_days(
        is_active
    );

COMMIT;