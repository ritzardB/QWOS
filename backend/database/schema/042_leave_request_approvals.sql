-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 042_leave_request_approvals.sql
-- Version     : 1.0
-- Description : Leave request approval workflow and audit history
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores approval actions performed against employee leave requests.
--
-- Leave Request
--     = WHAT the employee is requesting
--
-- Leave Request Approval
--     = WHO reviewed the request and WHAT decision was made
--
-- Multiple approval records may exist for a single leave request, allowing
-- QWOS to support sequential or multi-level approval workflows.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE REQUEST APPROVALS
-- =============================================================================

CREATE TABLE leave_request_approvals (

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
    -- Approval Sequence
    --
    -- Defines the order in which approval steps are evaluated.
    --
    -- Example:
    --     1 = Line Manager
    --     2 = HR
    --     3 = Final Approver
    ---------------------------------------------------------------------------

    approval_sequence INTEGER NOT NULL DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Approver
    --
    -- Employee/user responsible for this approval step.
    ---------------------------------------------------------------------------

    approver_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Decision
    --
    -- pending  = awaiting action
    -- approved = approval granted
    -- rejected = approval denied
    -- skipped  = step intentionally bypassed
    -- cancelled = approval step cancelled
    ---------------------------------------------------------------------------

    decision identifier_code NOT NULL DEFAULT 'pending',

    ---------------------------------------------------------------------------
    -- Decision Timestamp
    ---------------------------------------------------------------------------

    decided_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Comments
    ---------------------------------------------------------------------------

    comments TEXT,

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

    CONSTRAINT fk_leave_request_approvals_request
        FOREIGN KEY (leave_request_id)
        REFERENCES leave_requests(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_request_approvals_approver
        FOREIGN KEY (approver_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_leave_request_approvals_sequence
        CHECK (
            approval_sequence > 0
        ),

    CONSTRAINT chk_leave_request_approvals_decision
        CHECK (
            decision IN (
                'pending',
                'approved',
                'rejected',
                'skipped',
                'cancelled'
            )
        ),

    CONSTRAINT chk_leave_request_approvals_decided_at
        CHECK (
            (
                decision = 'pending'
                AND decided_at IS NULL
            )
            OR
            (
                decision <> 'pending'
                AND decided_at IS NOT NULL
            )
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_request_approvals_request
    ON leave_request_approvals(leave_request_id);

CREATE INDEX idx_leave_request_approvals_approver
    ON leave_request_approvals(approver_id);

CREATE INDEX idx_leave_request_approvals_decision
    ON leave_request_approvals(decision);

CREATE INDEX idx_leave_request_approvals_sequence
    ON leave_request_approvals(
        leave_request_id,
        approval_sequence
    );

CREATE INDEX idx_leave_request_approvals_pending
    ON leave_request_approvals(
        tenant_id,
        approver_id,
        decision
    );

COMMIT;