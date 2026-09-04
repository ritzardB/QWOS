-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 059_leave_balance_reservation_days.sql
-- Version     : 1.0
-- Description : Leave balance reservation day details
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records the individual dates and amounts reserved against an employee's
-- leave balance.
--
-- 058 Leave Balance Reservations
--     = Reservation header / aggregate
--
-- 059 Leave Balance Reservation Days
--     = Date-level reservation detail
--
-- 044 Leave Request Days
--     = Actual leave request date classification
--
-- 043 Leave Balance Transactions
--     = Permanent balance movements
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE BALANCE RESERVATION DAYS
-- =============================================================================

CREATE TABLE leave_balance_reservation_days (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Reservation
    ---------------------------------------------------------------------------

    leave_balance_reservation_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Request Day
    --
    -- Links the reservation detail to the corresponding requested leave day.
    ---------------------------------------------------------------------------

    leave_request_day_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Reserved Date
    ---------------------------------------------------------------------------

    reservation_date DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Day Classification
    --
    -- working_day
    -- rest_day
    -- holiday
    ---------------------------------------------------------------------------

    day_type identifier_code NOT NULL DEFAULT 'working_day',

    ---------------------------------------------------------------------------
    -- Duration
    --
    -- full_day
    -- half_day
    -- partial
    ---------------------------------------------------------------------------

    duration_type identifier_code NOT NULL DEFAULT 'full_day',

    ---------------------------------------------------------------------------
    -- Reserved Amount
    ---------------------------------------------------------------------------

    reserved_days NUMERIC(10,2) NOT NULL,

    ---------------------------------------------------------------------------
    -- Optional Time Range
    --
    -- Used for partial-day reservations.
    ---------------------------------------------------------------------------

    start_time TIME,

    end_time TIME,

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    ---------------------------------------------------------------------------
    -- Audit
    ---------------------------------------------------------------------------

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    created_by CHAR(26),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_by CHAR(26),

    deleted_at TIMESTAMPTZ,

    deleted_by CHAR(26),

    ---------------------------------------------------------------------------
    -- Concurrency
    ---------------------------------------------------------------------------

    version INTEGER NOT NULL DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Foreign Keys
    ---------------------------------------------------------------------------

    CONSTRAINT fk_leave_balance_reservation_days_reservation
        FOREIGN KEY (leave_balance_reservation_id)
        REFERENCES leave_balance_reservations(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_reservation_days_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_reservation_days_request_day
        FOREIGN KEY (leave_request_day_id)
        REFERENCES leave_request_days(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Amount
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservation_days_amount
        CHECK (
            reserved_days > 0
        ),

    ---------------------------------------------------------------------------
    -- Day Type
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservation_days_type
        CHECK (
            day_type IN (
                'working_day',
                'rest_day',
                'holiday'
            )
        ),

    ---------------------------------------------------------------------------
    -- Duration Type
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservation_days_duration
        CHECK (
            duration_type IN (
                'full_day',
                'half_day',
                'partial'
            )
        ),

    ---------------------------------------------------------------------------
    -- Time Range
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservation_days_time
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

    ---------------------------------------------------------------------------
    -- Full-day reservations do not require a time range.
    -- Partial reservations must provide a time range.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservation_days_partial_time
        CHECK (
            (
                duration_type <> 'partial'
            )
            OR
            (
                start_time IS NOT NULL
                AND end_time IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- One reservation detail per request day.
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_balance_reservation_days_date
        UNIQUE (
            tenant_id,
            leave_balance_reservation_id,
            reservation_date
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_balance_reservation_days_reservation
    ON leave_balance_reservation_days(
        leave_balance_reservation_id
    );

CREATE INDEX idx_leave_balance_reservation_days_employee
    ON leave_balance_reservation_days(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_balance_reservation_days_request_day
    ON leave_balance_reservation_days(
        leave_request_day_id
    );

CREATE INDEX idx_leave_balance_reservation_days_date
    ON leave_balance_reservation_days(
        tenant_id,
        reservation_date
    );

CREATE INDEX idx_leave_balance_reservation_days_type
    ON leave_balance_reservation_days(
        day_type,
        duration_type
    );

CREATE INDEX idx_leave_balance_reservation_days_active
    ON leave_balance_reservation_days(
        tenant_id,
        is_active
    );

COMMIT;