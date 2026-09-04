-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 066_leave_approval_escalations.sql
-- Version     : 1.0
-- Description : Leave approval escalation records
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records escalation actions taken when a leave approval step is not completed
-- within its configured timeframe.
--
-- 064_leave_approval_workflow_steps
--     = Defines escalation configuration
--
-- 065_leave_approval_delegations
--     = Defines temporary alternate approvers
--
-- 066_leave_approval_escalations
--     = Records actual escalation events
--
-- 042_leave_request_approvals
--     = Records the resulting approval decision
--
-- 062_leave_request_status_history
--     = Records leave-request status transitions
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE APPROVAL ESCALATIONS
-- =============================================================================

CREATE TABLE leave_approval_escalations (

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
    -- Approval Record
    --
    -- Identifies the approval instance that required escalation.
    ---------------------------------------------------------------------------

    leave_request_approval_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Workflow
    ---------------------------------------------------------------------------

    leave_approval_workflow_id CHAR(26) NOT NULL,

    leave_approval_workflow_step_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Original Approver
    ---------------------------------------------------------------------------

    original_approver_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Escalated Approver
    ---------------------------------------------------------------------------

    escalated_to_employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Escalation Identification
    ---------------------------------------------------------------------------

    escalation_number VARCHAR(50) NOT NULL,

    escalation_level INTEGER NOT NULL DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Escalation Reason
    --
    -- timeout
    -- unavailable
    -- manual
    -- delegation_unavailable
    -- system
    ---------------------------------------------------------------------------

    escalation_reason identifier_code NOT NULL DEFAULT 'timeout',

    escalation_reason_details TEXT,

    ---------------------------------------------------------------------------
    -- Timing
    ---------------------------------------------------------------------------

    triggered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    due_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Escalation Status
    --
    -- pending
    -- sent
    -- acknowledged
    -- resolved
    -- cancelled
    -- failed
    ---------------------------------------------------------------------------

    status identifier_code NOT NULL DEFAULT 'pending',

    ---------------------------------------------------------------------------
    -- Resolution
    ---------------------------------------------------------------------------

    resolved_at TIMESTAMPTZ,

    resolved_by CHAR(26),

    resolution_comments TEXT,

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

    CONSTRAINT fk_leave_approval_escalations_request
        FOREIGN KEY (leave_request_id)
        REFERENCES leave_requests(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_escalations_approval
        FOREIGN KEY (leave_request_approval_id)
        REFERENCES leave_request_approvals(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_escalations_workflow
        FOREIGN KEY (leave_approval_workflow_id)
        REFERENCES leave_approval_workflows(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_escalations_workflow_step
        FOREIGN KEY (leave_approval_workflow_step_id)
        REFERENCES leave_approval_workflow_steps(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_escalations_original_approver
        FOREIGN KEY (original_approver_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_escalations_escalated_to
        FOREIGN KEY (escalated_to_employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_escalations_resolved_by
        FOREIGN KEY (resolved_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Escalation Number
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_escalations_number
        CHECK (
            LENGTH(TRIM(escalation_number)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Escalation Level
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_escalations_level
        CHECK (
            escalation_level > 0
        ),

    ---------------------------------------------------------------------------
    -- Different Approvers
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_escalations_different_approver
        CHECK (
            original_approver_id <> escalated_to_employee_id
        ),

    ---------------------------------------------------------------------------
    -- Escalation Reason
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_escalations_reason
        CHECK (
            escalation_reason IN (
                'timeout',
                'unavailable',
                'manual',
                'delegation_unavailable',
                'system'
            )
        ),

    ---------------------------------------------------------------------------
    -- Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_escalations_status
        CHECK (
            status IN (
                'pending',
                'sent',
                'acknowledged',
                'resolved',
                'cancelled',
                'failed'
            )
        ),

    ---------------------------------------------------------------------------
    -- Resolution Consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_escalations_resolution
        CHECK (
            (
                status IN (
                    'pending',
                    'sent',
                    'acknowledged',
                    'failed',
                    'cancelled'
                )
                AND resolved_at IS NULL
                AND resolved_by IS NULL
            )
            OR
            (
                status = 'resolved'
                AND resolved_at IS NOT NULL
                AND resolved_by IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Resolution Timestamp
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_escalations_resolution_time
        CHECK (
            resolved_at IS NULL
            OR resolved_at >= triggered_at
        ),

    ---------------------------------------------------------------------------
    -- Due Timestamp
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_escalations_due_time
        CHECK (
            due_at IS NULL
            OR due_at >= triggered_at
        )

);

-- =============================================================================
-- UNIQUE CONSTRAINTS
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_approval_escalations_number
    ON leave_approval_escalations(
        tenant_id,
        escalation_number
    );

CREATE UNIQUE INDEX uq_leave_approval_escalations_level
    ON leave_approval_escalations(
        tenant_id,
        leave_request_approval_id,
        escalation_level
    );

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_approval_escalations_request
    ON leave_approval_escalations(
        tenant_id,
        leave_request_id
    );

CREATE INDEX idx_leave_approval_escalations_approval
    ON leave_approval_escalations(
        leave_request_approval_id
    );

CREATE INDEX idx_leave_approval_escalations_workflow
    ON leave_approval_escalations(
        tenant_id,
        leave_approval_workflow_id
    );

CREATE INDEX idx_leave_approval_escalations_workflow_step
    ON leave_approval_escalations(
        tenant_id,
        leave_approval_workflow_step_id
    );

CREATE INDEX idx_leave_approval_escalations_original_approver
    ON leave_approval_escalations(
        tenant_id,
        original_approver_id
    );

CREATE INDEX idx_leave_approval_escalations_escalated_to
    ON leave_approval_escalations(
        tenant_id,
        escalated_to_employee_id
    );

CREATE INDEX idx_leave_approval_escalations_status
    ON leave_approval_escalations(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_approval_escalations_triggered
    ON leave_approval_escalations(
        tenant_id,
        triggered_at
    );

CREATE INDEX idx_leave_approval_escalations_pending
    ON leave_approval_escalations(
        tenant_id,
        status,
        triggered_at
    )
    WHERE status IN ('pending', 'sent', 'acknowledged');

CREATE INDEX idx_leave_approval_escalations_active
    ON leave_approval_escalations(
        tenant_id,
        is_active
    );

COMMIT;