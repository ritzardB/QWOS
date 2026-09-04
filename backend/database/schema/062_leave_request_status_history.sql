-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 062_leave_request_status_history.sql
-- Version     : 1.0
-- Description : Leave request status transition history
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records every status transition made to a leave request.
--
-- The current status remains stored on:
--
--     041_leave_requests.status
--
-- This table provides the immutable audit trail showing:
--
--     previous status
--         ↓
--     new status
--         ↓
--     who changed it
--         ↓
--     when it changed
--         ↓
--     why / supporting comments
--
-- =============================================================================
--
-- Example lifecycle:
--
-- pending
--    ↓
-- approved
--    ↓
-- cancelled
--
-- or:
--
-- pending
--    ↓
-- withdrawn
--
-- or:
--
-- pending
--    ↓
-- rejected
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE REQUEST STATUS HISTORY
-- =============================================================================

CREATE TABLE leave_request_status_history (

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
    --
    -- Denormalized for efficient employee-level audit queries.
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Status Transition
    ---------------------------------------------------------------------------

    previous_status identifier_code,

    new_status identifier_code NOT NULL,

    ---------------------------------------------------------------------------
    -- Transition Sequence
    --
    -- Sequential number within the leave request lifecycle.
    ---------------------------------------------------------------------------

    transition_sequence INTEGER NOT NULL,

    ---------------------------------------------------------------------------
    -- Transition Information
    ---------------------------------------------------------------------------

    transition_reason TEXT,

    transition_comments TEXT,

    ---------------------------------------------------------------------------
    -- Actor
    ---------------------------------------------------------------------------

    changed_by CHAR(26) NOT NULL,

    changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    ---------------------------------------------------------------------------
    -- Optional Source Reference
    --
    -- Identifies the business event that caused the transition.
    --
    -- Examples:
    --   approval
    --   cancellation
    --   withdrawal
    --   system processing
    --
    -- Kept as identifier_code because different workflow tables may
    -- originate a status transition.
    ---------------------------------------------------------------------------

    change_source identifier_code NOT NULL DEFAULT 'system',

    ---------------------------------------------------------------------------
    -- Optional Source ID
    --
    -- Application-level reference to the originating business event.
    ---------------------------------------------------------------------------

    source_id CHAR(26),

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

    CONSTRAINT fk_leave_request_status_history_request
        FOREIGN KEY (leave_request_id)
        REFERENCES leave_requests(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_status_history_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_status_history_changed_by
        FOREIGN KEY (changed_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Sequence
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_status_history_sequence
        CHECK (
            transition_sequence > 0
        ),

    ---------------------------------------------------------------------------
    -- Previous Status
    --
    -- NULL is allowed for the initial status entry.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_status_history_previous_status
        CHECK (
            previous_status IS NULL
            OR previous_status IN (
                'pending',
                'approved',
                'rejected',
                'cancelled',
                'withdrawn'
            )
        ),

    ---------------------------------------------------------------------------
    -- New Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_status_history_new_status
        CHECK (
            new_status IN (
                'pending',
                'approved',
                'rejected',
                'cancelled',
                'withdrawn'
            )
        ),

    ---------------------------------------------------------------------------
    -- Prevent No-op Status Changes
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_status_history_transition
        CHECK (
            previous_status IS NULL
            OR previous_status <> new_status
        ),

    ---------------------------------------------------------------------------
    -- Change Source
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_request_status_history_source
        CHECK (
            change_source IN (
                'system',
                'employee',
                'manager',
                'hr',
                'approval',
                'cancellation',
                'withdrawal',
                'administrative'
            )
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_request_status_history_request
    ON leave_request_status_history(
        leave_request_id,
        transition_sequence
    );

CREATE INDEX idx_leave_request_status_history_employee
    ON leave_request_status_history(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_request_status_history_previous_status
    ON leave_request_status_history(
        tenant_id,
        previous_status
    );

CREATE INDEX idx_leave_request_status_history_new_status
    ON leave_request_status_history(
        tenant_id,
        new_status
    );

CREATE INDEX idx_leave_request_status_history_changed_by
    ON leave_request_status_history(
        changed_by
    );

CREATE INDEX idx_leave_request_status_history_changed_at
    ON leave_request_status_history(
        tenant_id,
        changed_at
    );

CREATE INDEX idx_leave_request_status_history_source
    ON leave_request_status_history(
        change_source,
        source_id
    );

CREATE INDEX idx_leave_request_status_history_active
    ON leave_request_status_history(
        tenant_id,
        is_active
    );

-- =============================================================================
-- UNIQUE CONSTRAINT
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_request_status_history_sequence
    ON leave_request_status_history(
        tenant_id,
        leave_request_id,
        transition_sequence
    );

COMMIT;