-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 063_leave_approval_workflows.sql
-- Version     : 1.0
-- Description : Leave approval workflow definitions
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines the approval workflow configuration used by leave requests.
--
-- This table defines the workflow itself.
--
-- Individual approval decisions remain stored in:
--
--     042_leave_request_approvals
--
-- Workflow steps will be stored in:
--
--     064_leave_approval_workflow_steps
--
-- =============================================================================
--
-- Relationship:
--
-- 037 leave_types
--       │
--       ▼
-- 038 leave_policies
--       │
--       ▼
-- 063 leave_approval_workflows
--       │
--       ▼
-- 064 leave_approval_workflow_steps
--       │
--       ▼
-- 041 leave_requests
--       │
--       ▼
-- 042 leave_request_approvals
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE APPROVAL WORKFLOWS
-- =============================================================================

CREATE TABLE leave_approval_workflows (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Workflow Identification
    ---------------------------------------------------------------------------

    workflow_code VARCHAR(50) NOT NULL,

    workflow_name VARCHAR(150) NOT NULL,

    description TEXT,

    ---------------------------------------------------------------------------
    -- Optional Leave Policy Association
    --
    -- NULL allows a tenant-wide/default workflow.
    ---------------------------------------------------------------------------

    leave_policy_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Approval Mode
    --
    -- sequential = approvers act in defined order
    -- parallel   = approvers may act independently
    ---------------------------------------------------------------------------

    approval_mode identifier_code NOT NULL DEFAULT 'sequential',

    ---------------------------------------------------------------------------
    -- Minimum Approvals
    --
    -- Number of approvals required for successful completion.
    ---------------------------------------------------------------------------

    minimum_approvals INTEGER NOT NULL DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Maximum Approval Levels
    --
    -- Maximum number of workflow levels configured for the workflow.
    ---------------------------------------------------------------------------

    maximum_approval_levels INTEGER NOT NULL DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Auto Approval
    --
    -- Allows the application service to automatically approve requests
    -- satisfying the workflow's configured conditions.
    ---------------------------------------------------------------------------

    auto_approval_enabled BOOLEAN NOT NULL DEFAULT FALSE,

    ---------------------------------------------------------------------------
    -- Effective Dating
    ---------------------------------------------------------------------------

    effective_from DATE NOT NULL,

    effective_until DATE,

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

    CONSTRAINT fk_leave_approval_workflows_policy
        FOREIGN KEY (leave_policy_id)
        REFERENCES leave_policies(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Workflow Code
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflows_code
        CHECK (
            LENGTH(TRIM(workflow_code)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Workflow Name
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflows_name
        CHECK (
            LENGTH(TRIM(workflow_name)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Approval Mode
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflows_mode
        CHECK (
            approval_mode IN (
                'sequential',
                'parallel'
            )
        ),

    ---------------------------------------------------------------------------
    -- Minimum Approvals
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflows_minimum_approvals
        CHECK (
            minimum_approvals > 0
        ),

    ---------------------------------------------------------------------------
    -- Maximum Approval Levels
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflows_maximum_levels
        CHECK (
            maximum_approval_levels > 0
        ),

    ---------------------------------------------------------------------------
    -- Approval Limits
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflows_approval_limits
        CHECK (
            minimum_approvals <= maximum_approval_levels
        ),

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflows_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        )

);

-- =============================================================================
-- UNIQUE CONSTRAINTS
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_approval_workflows_code
    ON leave_approval_workflows(
        tenant_id,
        workflow_code
    );

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_approval_workflows_policy
    ON leave_approval_workflows(
        tenant_id,
        leave_policy_id
    );

CREATE INDEX idx_leave_approval_workflows_mode
    ON leave_approval_workflows(
        tenant_id,
        approval_mode
    );

CREATE INDEX idx_leave_approval_workflows_effective
    ON leave_approval_workflows(
        tenant_id,
        effective_from,
        effective_until
    );

CREATE INDEX idx_leave_approval_workflows_active
    ON leave_approval_workflows(
        tenant_id,
        is_active
    );

COMMIT;