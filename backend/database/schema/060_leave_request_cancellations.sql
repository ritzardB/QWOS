-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 060_leave_request_cancellations.sql
-- Version     : 1.0
-- Description : Leave request cancellation records
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records the cancellation of a leave request as a separate auditable
-- business event.
--
-- This table does NOT delete or overwrite the original leave request.
-- The leave request remains the source record, while this table preserves
-- cancellation history, reason, actor, and timestamps.
--
-- Relationship:
--
-- 041 leave_requests
--       │
--       ▼
-- 060 leave_request_cancellations
--
-- Balance reservations are handled independently by:
--
-- 058 leave_balance_reservations
-- 059 leave_balance_reservation_days
--
-- Cancellation processing may release an active reservation, but the
-- cancellation record itself does not directly modify the balance.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE REQUEST CANCELLATIONS
-- =============================================================================

CREATE TABLE leave_request_cancellations (

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
    -- Cancellation Information
    ---------------------------------------------------------------------------

    cancellation_number VARCHAR(50) NOT NULL,

    cancellation_reason TEXT NOT NULL,

    ---------------------------------------------------------------------------
    -- Actor
    --
    -- The employee, manager, HR administrator, or other authorized user
    -- who initiated the cancellation.
    ---------------------------------------------------------------------------

    cancelled_by CHAR(26) NOT NULL,

    cancelled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    ---------------------------------------------------------------------------
    -- Previous Request Status
    --
    -- Preserves the status immediately before cancellation.
    ---------------------------------------------------------------------------

    previous_status identifier_code NOT NULL,

    ---------------------------------------------------------------------------
    -- Cancellation Status
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

    CONSTRAINT fk_leave_request_cancellations_request
        FOREIGN KEY (leave_request_id)
        REFERENCES leave_requests(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_cancellations_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_cancellations_cancelled_by
        FOREIGN KEY (cancelled_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_cancellations_approved_by
        FOREIGN KEY (approved_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_cancellations_processed_by
        FOREIGN KEY (processed_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Cancellation Number
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_cancellations_number
        CHECK (
            LENGTH(TRIM(cancellation_number)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Reason
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_cancellations_reason
        CHECK (
            LENGTH(TRIM(cancellation_reason)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Previous Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_cancellations_previous_status
        CHECK (
            previous_status IN (
                'pending',
                'approved'
            )
        ),

    ---------------------------------------------------------------------------
    -- Cancellation Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_cancellations_status
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

    CONSTRAINT chk_leave_request_cancellations_approval
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

    CONSTRAINT chk_leave_request_cancellations_processing
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

    CONSTRAINT chk_leave_request_cancellations_approval_time
        CHECK (
            approved_at IS NULL
            OR approved_at >= cancelled_at
        ),

    ---------------------------------------------------------------------------
    -- Processing Timestamp
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_cancellations_processing_time
        CHECK (
            processed_at IS NULL
            OR (
                processed_at >= cancelled_at
                AND (
                    approved_at IS NULL
                    OR processed_at >= approved_at
                )
            )
        ),

    ---------------------------------------------------------------------------
    -- One cancellation record per request
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_request_cancellations_request
        UNIQUE (
            tenant_id,
            leave_request_id
        ),

    ---------------------------------------------------------------------------
    -- Unique Cancellation Number
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_request_cancellations_number
        UNIQUE (
            tenant_id,
            cancellation_number
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_request_cancellations_request
    ON leave_request_cancellations(
        leave_request_id
    );

CREATE INDEX idx_leave_request_cancellations_employee
    ON leave_request_cancellations(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_request_cancellations_cancelled_by
    ON leave_request_cancellations(
        cancelled_by
    );

CREATE INDEX idx_leave_request_cancellations_status
    ON leave_request_cancellations(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_request_cancellations_cancelled_at
    ON leave_request_cancellations(
        tenant_id,
        cancelled_at
    );

CREATE INDEX idx_leave_request_cancellations_pending
    ON leave_request_cancellations(
        tenant_id,
        status,
        cancelled_at
    )
    WHERE status = 'pending';

CREATE INDEX idx_leave_request_cancellations_active
    ON leave_request_cancellations(
        tenant_id,
        is_active
    );

COMMIT;