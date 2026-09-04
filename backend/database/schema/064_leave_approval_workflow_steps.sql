-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 064_leave_approval_workflow_steps.sql
-- Version     : 1.0
-- Description : Leave approval workflow step definitions
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines the individual approval levels and approver rules belonging to a
-- leave approval workflow.
--
-- 063_leave_approval_workflows
--     = Workflow definition
--
-- 064_leave_approval_workflow_steps
--     = Approval levels / approver rules
--
-- 042_leave_request_approvals
--     = Actual approval decisions for a leave request
--
-- =============================================================================
--
-- Example:
--
-- Workflow: Standard Leave Approval
--
--   Step 1 → Direct Manager
--   Step 2 → Department Manager
--   Step 3 → HR
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE APPROVAL WORKFLOW STEPS
-- =============================================================================

CREATE TABLE leave_approval_workflow_steps (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Workflow
    ---------------------------------------------------------------------------

    leave_approval_workflow_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Step Identification
    ---------------------------------------------------------------------------

    step_number INTEGER NOT NULL,

    step_name VARCHAR(150) NOT NULL,

    description TEXT,

    ---------------------------------------------------------------------------
    -- Approver Type
    --
    -- manager
    -- department_manager
    -- hr
    -- specific_employee
    -- role
    -- system
    ---------------------------------------------------------------------------

    approver_type identifier_code NOT NULL DEFAULT 'manager',

    ---------------------------------------------------------------------------
    -- Optional Specific Approver
    --
    -- Used when approver_type = specific_employee.
    ---------------------------------------------------------------------------

    approver_employee_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Optional Role
    --
    -- Used when approver_type = role.
    --
    -- Role identifier is intentionally stored as CHAR(26) so the application
    -- can resolve the role through the identity/authorization domain.
    ---------------------------------------------------------------------------

    approver_role_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Approval Requirement
    --
    -- required = approval must be completed
    -- optional = step may be skipped according to workflow rules
    ---------------------------------------------------------------------------

    requirement_type identifier_code NOT NULL DEFAULT 'required',

    ---------------------------------------------------------------------------
    -- Minimum Approvals
    --
    -- Particularly useful for role/group-based approval steps.
    ---------------------------------------------------------------------------

    minimum_approvals INTEGER NOT NULL DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Escalation
    ---------------------------------------------------------------------------

    escalation_enabled BOOLEAN NOT NULL DEFAULT FALSE,

    escalation_after_hours INTEGER,

    ---------------------------------------------------------------------------
    -- Step Conditions
    --
    -- Optional application-defined condition identifier.
    -- The actual condition evaluation belongs to the application layer.
    ---------------------------------------------------------------------------

    condition_type identifier_code,

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

    CONSTRAINT fk_leave_approval_workflow_steps_workflow
        FOREIGN KEY (leave_approval_workflow_id)
        REFERENCES leave_approval_workflows(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_workflow_steps_employee
        FOREIGN KEY (approver_employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Step Number
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_number
        CHECK (
            step_number > 0
        ),

    ---------------------------------------------------------------------------
    -- Step Name
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_name
        CHECK (
            LENGTH(TRIM(step_name)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Approver Type
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_approver_type
        CHECK (
            approver_type IN (
                'manager',
                'department_manager',
                'hr',
                'specific_employee',
                'role',
                'system'
            )
        ),

    ---------------------------------------------------------------------------
    -- Specific Employee Requirement
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_employee
        CHECK (
            (
                approver_type = 'specific_employee'
                AND approver_employee_id IS NOT NULL
            )
            OR
            (
                approver_type <> 'specific_employee'
                AND approver_employee_id IS NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Role Requirement
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_role
        CHECK (
            (
                approver_type = 'role'
                AND approver_role_id IS NOT NULL
            )
            OR
            (
                approver_type <> 'role'
                AND approver_role_id IS NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- System Approver
    --
    -- System approval does not require an employee or role.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_system
        CHECK (
            approver_type <> 'system'
            OR (
                approver_employee_id IS NULL
                AND approver_role_id IS NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Requirement Type
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_requirement
        CHECK (
            requirement_type IN (
                'required',
                'optional'
            )
        ),

    ---------------------------------------------------------------------------
    -- Minimum Approvals
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_minimum
        CHECK (
            minimum_approvals > 0
        ),

    ---------------------------------------------------------------------------
    -- Escalation
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_escalation
        CHECK (
            (
                escalation_enabled = FALSE
                AND escalation_after_hours IS NULL
            )
            OR
            (
                escalation_enabled = TRUE
                AND escalation_after_hours > 0
            )
        ),

    ---------------------------------------------------------------------------
    -- Condition Type
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_condition
        CHECK (
            condition_type IS NULL
            OR LENGTH(TRIM(condition_type::TEXT)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_workflow_steps_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        )

);

-- =============================================================================
-- UNIQUE CONSTRAINTS
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_approval_workflow_steps_number
    ON leave_approval_workflow_steps(
        tenant_id,
        leave_approval_workflow_id,
        step_number
    );

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_approval_workflow_steps_workflow
    ON leave_approval_workflow_steps(
        tenant_id,
        leave_approval_workflow_id
    );

CREATE INDEX idx_leave_approval_workflow_steps_approver_employee
    ON leave_approval_workflow_steps(
        tenant_id,
        approver_employee_id
    );

CREATE INDEX idx_leave_approval_workflow_steps_approver_role
    ON leave_approval_workflow_steps(
        tenant_id,
        approver_role_id
    );

CREATE INDEX idx_leave_approval_workflow_steps_type
    ON leave_approval_workflow_steps(
        tenant_id,
        approver_type
    );

CREATE INDEX idx_leave_approval_workflow_steps_effective
    ON leave_approval_workflow_steps(
        tenant_id,
        effective_from,
        effective_until
    );

CREATE INDEX idx_leave_approval_workflow_steps_active
    ON leave_approval_workflow_steps(
        tenant_id,
        is_active
    );

COMMIT;