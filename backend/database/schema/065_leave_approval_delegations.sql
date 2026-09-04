-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 065_leave_approval_delegations.sql
-- Version     : 1.0
-- Description : Leave approval delegation assignments
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines temporary or effective-dated delegation of leave approval authority
-- from one employee to another.
--
-- The normal approver remains unchanged. The delegation determines who may
-- act on the approver's behalf during the configured delegation period.
--
-- This table defines delegation rules.
--
-- Actual approval decisions remain stored in:
--
--     042_leave_request_approvals
--
-- Workflow definitions remain stored in:
--
--     063_leave_approval_workflows
--
-- Workflow steps remain stored in:
--
--     064_leave_approval_workflow_steps
--
-- =============================================================================
--
-- Example:
--
-- Manager A
--     │
--     │ delegates
--     ▼
-- Manager B
--
-- Effective:
--     2027-01-01 → 2027-01-15
--
-- Manager B may approve leave requests on behalf of Manager A during
-- the configured delegation period.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE APPROVAL DELEGATIONS
-- =============================================================================

CREATE TABLE leave_approval_delegations (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Original Approver
    ---------------------------------------------------------------------------

    delegator_employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Delegate
    ---------------------------------------------------------------------------

    delegate_employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Optional Workflow Restriction
    --
    -- NULL = applies to all leave approval workflows available to the
    -- delegator.
    ---------------------------------------------------------------------------

    leave_approval_workflow_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Optional Workflow Step Restriction
    --
    -- NULL = applies to all steps within the selected workflow.
    ---------------------------------------------------------------------------

    leave_approval_workflow_step_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Delegation Identification
    ---------------------------------------------------------------------------

    delegation_number VARCHAR(50) NOT NULL,

    delegation_reason TEXT,

    ---------------------------------------------------------------------------
    -- Effective Period
    ---------------------------------------------------------------------------

    effective_from DATE NOT NULL,

    effective_until DATE,

    ---------------------------------------------------------------------------
    -- Delegation Status
    --
    -- pending
    -- approved
    -- active
    -- expired
    -- cancelled
    -- rejected
    ---------------------------------------------------------------------------

    status identifier_code NOT NULL DEFAULT 'pending',

    ---------------------------------------------------------------------------
    -- Approval
    ---------------------------------------------------------------------------

    approved_by CHAR(26),

    approved_at TIMESTAMPTZ,

    approval_comments TEXT,

    ---------------------------------------------------------------------------
    -- Cancellation
    ---------------------------------------------------------------------------

    cancelled_by CHAR(26),

    cancelled_at TIMESTAMPTZ,

    cancellation_reason TEXT,

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

    CONSTRAINT fk_leave_approval_delegations_delegator
        FOREIGN KEY (delegator_employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_delegations_delegate
        FOREIGN KEY (delegate_employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_delegations_workflow
        FOREIGN KEY (leave_approval_workflow_id)
        REFERENCES leave_approval_workflows(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_delegations_workflow_step
        FOREIGN KEY (leave_approval_workflow_step_id)
        REFERENCES leave_approval_workflow_steps(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_delegations_approved_by
        FOREIGN KEY (approved_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_delegations_cancelled_by
        FOREIGN KEY (cancelled_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Delegation Number
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_delegations_number
        CHECK (
            LENGTH(TRIM(delegation_number)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Delegator and Delegate
    --
    -- An employee cannot delegate approval authority to themselves.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_delegations_different_employee
        CHECK (
            delegator_employee_id <> delegate_employee_id
        ),

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_delegations_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        ),

    ---------------------------------------------------------------------------
    -- Workflow Step Dependency
    --
    -- A workflow step cannot be specified without its parent workflow.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_delegations_workflow_step
        CHECK (
            leave_approval_workflow_step_id IS NULL
            OR leave_approval_workflow_id IS NOT NULL
        ),

    ---------------------------------------------------------------------------
    -- Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_delegations_status
        CHECK (
            status IN (
                'pending',
                'approved',
                'active',
                'expired',
                'cancelled',
                'rejected'
            )
        ),

    ---------------------------------------------------------------------------
    -- Approval Consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_delegations_approval
        CHECK (
            (
                status IN ('pending', 'rejected', 'cancelled')
                AND approved_by IS NULL
                AND approved_at IS NULL
            )
            OR
            (
                status IN ('approved', 'active', 'expired')
                AND approved_by IS NOT NULL
                AND approved_at IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Cancellation Consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_delegations_cancellation
        CHECK (
            (
                status <> 'cancelled'
                AND cancelled_by IS NULL
                AND cancelled_at IS NULL
                AND cancellation_reason IS NULL
            )
            OR
            (
                status = 'cancelled'
                AND cancelled_by IS NOT NULL
                AND cancelled_at IS NOT NULL
                AND cancellation_reason IS NOT NULL
                AND LENGTH(TRIM(cancellation_reason)) > 0
            )
        ),

    ---------------------------------------------------------------------------
    -- Approval Timestamp
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_delegations_approval_time
        CHECK (
            approved_at IS NULL
            OR approved_at >= created_at
        ),

    ---------------------------------------------------------------------------
    -- Cancellation Timestamp
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_delegations_cancellation_time
        CHECK (
            cancelled_at IS NULL
            OR cancelled_at >= created_at
        )

);

-- =============================================================================
-- UNIQUE CONSTRAINT
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_approval_delegations_number
    ON leave_approval_delegations(
        tenant_id,
        delegation_number
    );

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_approval_delegations_delegator
    ON leave_approval_delegations(
        tenant_id,
        delegator_employee_id
    );

CREATE INDEX idx_leave_approval_delegations_delegate
    ON leave_approval_delegations(
        tenant_id,
        delegate_employee_id
    );

CREATE INDEX idx_leave_approval_delegations_workflow
    ON leave_approval_delegations(
        tenant_id,
        leave_approval_workflow_id
    );

CREATE INDEX idx_leave_approval_delegations_workflow_step
    ON leave_approval_delegations(
        tenant_id,
        leave_approval_workflow_step_id
    );

CREATE INDEX idx_leave_approval_delegations_status
    ON leave_approval_delegations(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_approval_delegations_effective
    ON leave_approval_delegations(
        tenant_id,
        effective_from,
        effective_until
    );

CREATE INDEX idx_leave_approval_delegations_active
    ON leave_approval_delegations(
        tenant_id,
        is_active
    );

-- =============================================================================
-- ACTIVE DELEGATIONS
-- =============================================================================

CREATE INDEX idx_leave_approval_delegations_current
    ON leave_approval_delegations(
        tenant_id,
        delegator_employee_id,
        effective_from,
        effective_until
    )
    WHERE status = 'active'
      AND is_active = TRUE;

COMMIT;