-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 061_leave_request_withdrawals.sql
-- Version     : 1.0
-- Description : Leave request withdrawal records
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records an employee-initiated withdrawal of a leave request as a separate
-- auditable business event.
--
-- Withdrawal is different from cancellation:
--
--   Withdrawal
--       Employee retracts their own leave request.
--
--   Cancellation
--       Leave request is cancelled through an authorized cancellation
--       workflow, including approved leave where applicable.
--
-- The original leave request is never deleted or overwritten.
--
-- =============================================================================
--
-- Relationship:
--
-- 041 leave_requests
--       │
--       └── 061 leave_request_withdrawals
--
-- A withdrawal may cause:
--
--       058 leave_balance_reservations
--                 │
--                 └── 059 leave_balance_reservation_days
--                              │
--                              └── reservation released
--
-- This table does NOT directly modify:
--
--       043 leave_balance_transactions
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE REQUEST WITHDRAWALS
-- =============================================================================

CREATE TABLE leave_request_withdrawals (

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
    -- Withdrawal Information
    ---------------------------------------------------------------------------

    withdrawal_number VARCHAR(50) NOT NULL,

    withdrawal_reason TEXT NOT NULL,

    ---------------------------------------------------------------------------
    -- Actor
    --
    -- Normally the employee who owns the leave request.
    ---------------------------------------------------------------------------

    withdrawn_by CHAR(26) NOT NULL,

    withdrawn_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    ---------------------------------------------------------------------------
    -- Previous Request Status
    ---------------------------------------------------------------------------

    previous_status identifier_code NOT NULL,

    ---------------------------------------------------------------------------
    -- Withdrawal Status
    --
    -- pending
    -- approved
    -- rejected
    -- processed
    -- cancelled
    ---------------------------------------------------------------------------

    status identifier_code NOT NULL DEFAULT 'pending',

    ---------------------------------------------------------------------------
    -- Approval
    ---------------------------------------------------------------------------

    approved_by CHAR(26),

    approved_at TIMESTAMPTZ,

    approval_comments TEXT,

    ---------------------------------------------------------------------------
    -- Processing
    ---------------------------------------------------------------------------

    processed_at TIMESTAMPTZ,

    processed_by CHAR(26),

    ---------------------------------------------------------------------------
    -- Optional Notes
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

    CONSTRAINT fk_leave_request_withdrawals_request
        FOREIGN KEY (leave_request_id)
        REFERENCES leave_requests(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_withdrawals_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_withdrawals_withdrawn_by
        FOREIGN KEY (withdrawn_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_withdrawals_approved_by
        FOREIGN KEY (approved_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_withdrawals_processed_by
        FOREIGN KEY (processed_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Withdrawal Number
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_withdrawals_number
        CHECK (
            LENGTH(TRIM(withdrawal_number)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Withdrawal Reason
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_withdrawals_reason
        CHECK (
            LENGTH(TRIM(withdrawal_reason)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Previous Request Status
    --
    -- Withdrawal should normally occur while the request is still pending.
    -- An approved request may also be withdrawn if the business workflow
    -- permits withdrawal before the leave period begins.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_withdrawals_previous_status
        CHECK (
            previous_status IN (
                'pending',
                'approved'
            )
        ),

    ---------------------------------------------------------------------------
    -- Withdrawal Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_withdrawals_status
        CHECK (
            status IN (
                'pending',
                'approved',
                'rejected',
                'processed',
                'cancelled'
            )
        ),

    ---------------------------------------------------------------------------
    -- Approval Consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_withdrawals_approval
        CHECK (
            (
                status IN ('pending', 'rejected', 'cancelled')
                AND approved_by IS NULL
                AND approved_at IS NULL
            )
            OR
            (
                status IN ('approved', 'processed')
                AND approved_by IS NOT NULL
                AND approved_at IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Processing Consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_withdrawals_processing
        CHECK (
            (
                status <> 'processed'
                AND processed_at IS NULL
                AND processed_by IS NULL
            )
            OR
            (
                status = 'processed'
                AND processed_at IS NOT NULL
                AND processed_by IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Approval Timestamp
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_withdrawals_approval_time
        CHECK (
            approved_at IS NULL
            OR approved_at >= withdrawn_at
        ),

    ---------------------------------------------------------------------------
    -- Processing Timestamp
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_withdrawals_processing_time
        CHECK (
            processed_at IS NULL
            OR (
                processed_at >= withdrawn_at
                AND (
                    approved_at IS NULL
                    OR processed_at >= approved_at
                )
            )
        ),

    ---------------------------------------------------------------------------
    -- One withdrawal record per leave request
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_request_withdrawals_request
        UNIQUE (
            tenant_id,
            leave_request_id
        ),

    ---------------------------------------------------------------------------
    -- Unique Withdrawal Number
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_request_withdrawals_number
        UNIQUE (
            tenant_id,
            withdrawal_number
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_request_withdrawals_request
    ON leave_request_withdrawals(
        leave_request_id
    );

CREATE INDEX idx_leave_request_withdrawals_employee
    ON leave_request_withdrawals(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_request_withdrawals_withdrawn_by
    ON leave_request_withdrawals(
        withdrawn_by
    );

CREATE INDEX idx_leave_request_withdrawals_status
    ON leave_request_withdrawals(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_request_withdrawals_withdrawn_at
    ON leave_request_withdrawals(
        tenant_id,
        withdrawn_at
    );

CREATE INDEX idx_leave_request_withdrawals_pending
    ON leave_request_withdrawals(
        tenant_id,
        status,
        withdrawn_at
    )
    WHERE status = 'pending';

CREATE INDEX idx_leave_request_withdrawals_active
    ON leave_request_withdrawals(
        tenant_id,
        is_active
    );

COMMIT;