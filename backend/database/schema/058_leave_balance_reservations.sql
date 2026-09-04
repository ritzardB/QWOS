-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 058_leave_balance_reservations.sql
-- Version     : 1.0
-- Description : Leave balance reservations
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Reserves employee leave balance for submitted leave requests.
--
-- Reservation is NOT a balance transaction.
--
-- 040 Employee Leave Balances
--     = Aggregate balance
--
-- 041 Leave Requests
--     = Employee leave request
--
-- 058 Leave Balance Reservations
--     = Temporarily reserves available balance
--
-- 043 Leave Balance Transactions
--     = Permanent balance movement after approval/application
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE BALANCE RESERVATIONS
-- =============================================================================

CREATE TABLE leave_balance_reservations (

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
    -- Employee Leave Assignment
    ---------------------------------------------------------------------------

    employee_leave_assignment_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee Leave Balance
    ---------------------------------------------------------------------------

    employee_leave_balance_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Request
    ---------------------------------------------------------------------------

    leave_request_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Reserved Amount
    ---------------------------------------------------------------------------

    reserved_days NUMERIC(10,2) NOT NULL,

    ---------------------------------------------------------------------------
    -- Reservation Period
    ---------------------------------------------------------------------------

    reservation_start_date DATE NOT NULL,

    reservation_end_date DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Lifecycle
    --
    -- pending
    -- active
    -- released
    -- consumed
    -- expired
    -- cancelled
    ---------------------------------------------------------------------------

    status identifier_code NOT NULL DEFAULT 'pending',

    ---------------------------------------------------------------------------
    -- Reservation Timestamps
    ---------------------------------------------------------------------------

    reserved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    released_at TIMESTAMPTZ,

    consumed_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Optional Expiration
    ---------------------------------------------------------------------------

    expires_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Explanation
    ---------------------------------------------------------------------------

    notes TEXT,

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

    CONSTRAINT fk_leave_balance_reservations_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_reservations_assignment
        FOREIGN KEY (employee_leave_assignment_id)
        REFERENCES employee_leave_assignments(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_reservations_balance
        FOREIGN KEY (employee_leave_balance_id)
        REFERENCES employee_leave_balances(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_reservations_request
        FOREIGN KEY (leave_request_id)
        REFERENCES leave_requests(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Amount
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservations_days
        CHECK (
            reserved_days > 0
        ),

    ---------------------------------------------------------------------------
    -- Reservation dates
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservations_dates
        CHECK (
            reservation_end_date >= reservation_start_date
        ),

    ---------------------------------------------------------------------------
    -- Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservations_status
        CHECK (
            status IN (
                'pending',
                'active',
                'released',
                'consumed',
                'expired',
                'cancelled'
            )
        ),

    ---------------------------------------------------------------------------
    -- Release timestamp consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservations_released
        CHECK (
            (
                status IN (
                    'pending',
                    'active',
                    'consumed',
                    'expired'
                )
                AND released_at IS NULL
            )
            OR
            (
                status IN (
                    'released',
                    'cancelled'
                )
                AND released_at IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Consumed timestamp consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservations_consumed
        CHECK (
            (
                status <> 'consumed'
                AND consumed_at IS NULL
            )
            OR
            (
                status = 'consumed'
                AND consumed_at IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Expiration must occur after reservation.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_reservations_expiration
        CHECK (
            expires_at IS NULL
            OR expires_at >= reserved_at
        ),

    ---------------------------------------------------------------------------
    -- One active reservation per request.
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_balance_reservations_request
        UNIQUE (
            tenant_id,
            leave_request_id
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_balance_reservations_employee
    ON leave_balance_reservations(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_balance_reservations_assignment
    ON leave_balance_reservations(
        employee_leave_assignment_id
    );

CREATE INDEX idx_leave_balance_reservations_balance
    ON leave_balance_reservations(
        employee_leave_balance_id
    );

CREATE INDEX idx_leave_balance_reservations_request
    ON leave_balance_reservations(
        leave_request_id
    );

CREATE INDEX idx_leave_balance_reservations_status
    ON leave_balance_reservations(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_balance_reservations_period
    ON leave_balance_reservations(
        tenant_id,
        reservation_start_date,
        reservation_end_date
    );

CREATE INDEX idx_leave_balance_reservations_expiration
    ON leave_balance_reservations(
        tenant_id,
        expires_at
    );

CREATE INDEX idx_leave_balance_reservations_active
    ON leave_balance_reservations(
        tenant_id,
        is_active
    );

COMMIT;