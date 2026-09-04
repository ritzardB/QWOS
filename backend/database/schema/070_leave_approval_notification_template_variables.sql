-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 070_leave_approval_notification_template_variables.sql
-- Version     : 1.0
-- Description : Controlled variables available to leave notification templates
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines the approved variables that may be used by leave approval
-- notification templates.
--
-- This table acts as a controlled variable registry.
--
-- 069_leave_approval_notification_templates
--     = Notification message templates
--
-- 070_leave_approval_notification_template_variables
--     = Approved template variables
--
-- 067_leave_approval_notifications
--     = Rendered notification snapshot / delivery record
--
-- Variables are intentionally stored as metadata rather than arbitrary
-- employee/database field references.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE APPROVAL NOTIFICATION TEMPLATE VARIABLES
-- =============================================================================

CREATE TABLE leave_approval_notification_template_variables (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    --
    -- NULL is intentionally not used here. Variables are tenant-scoped so
    -- tenants can later introduce controlled custom variables without
    -- affecting another tenant.
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Variable Identification
    ---------------------------------------------------------------------------

    variable_code VARCHAR(100) NOT NULL,

    variable_name VARCHAR(150) NOT NULL,

    description TEXT NOT NULL,

    ---------------------------------------------------------------------------
    -- Data Type
    --
    -- string
    -- integer
    -- decimal
    -- boolean
    -- date
    -- datetime
    -- time
    -- url
    ---------------------------------------------------------------------------

    data_type identifier_code NOT NULL DEFAULT 'string',

    ---------------------------------------------------------------------------
    -- Variable Scope
    --
    -- employee
    -- leave_request
    -- approval
    -- workflow
    -- delegation
    -- escalation
    -- tenant
    -- system
    ---------------------------------------------------------------------------

    variable_scope identifier_code NOT NULL,

    ---------------------------------------------------------------------------
    -- Notification Type
    --
    -- NULL means the variable is available to all supported leave
    -- notification types.
    --
    -- Otherwise the variable is restricted to the specified event.
    ---------------------------------------------------------------------------

    notification_type identifier_code,

    ---------------------------------------------------------------------------
    -- Formatting
    --
    -- Optional display format used by the notification rendering service.
    --
    -- Examples:
    -- date: YYYY-MM-DD
    -- datetime: YYYY-MM-DD HH:mm
    -- decimal: 0.00
    ---------------------------------------------------------------------------

    format_pattern VARCHAR(100),

    ---------------------------------------------------------------------------
    -- Security / Availability
    ---------------------------------------------------------------------------

    is_required BOOLEAN NOT NULL DEFAULT FALSE,

    is_system_variable BOOLEAN NOT NULL DEFAULT TRUE,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    ---------------------------------------------------------------------------
    -- Effective Period
    ---------------------------------------------------------------------------

    effective_from DATE NOT NULL DEFAULT CURRENT_DATE,

    effective_until DATE,

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
    -- Variable Code
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_template_variables_code
        CHECK (
            BTRIM(variable_code) <> ''
        ),

    CONSTRAINT chk_leave_approval_notification_template_variables_name
        CHECK (
            BTRIM(variable_name) <> ''
        ),

    CONSTRAINT chk_leave_approval_notification_template_variables_description
        CHECK (
            BTRIM(description) <> ''
        ),

    ---------------------------------------------------------------------------
    -- Data Type
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_template_variables_data_type
        CHECK (
            data_type IN (
                'string',
                'integer',
                'decimal',
                'boolean',
                'date',
                'datetime',
                'time',
                'url'
            )
        ),

    ---------------------------------------------------------------------------
    -- Variable Scope
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_template_variables_scope
        CHECK (
            variable_scope IN (
                'employee',
                'leave_request',
                'approval',
                'workflow',
                'delegation',
                'escalation',
                'tenant',
                'system'
            )
        ),

    ---------------------------------------------------------------------------
    -- Notification Type
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_template_variables_type
        CHECK (
            notification_type IS NULL
            OR notification_type IN (
                'approval_required',
                'approval_approved',
                'approval_rejected',
                'approval_escalated',
                'approval_delegated',
                'leave_submitted',
                'leave_withdrawn',
                'leave_cancelled'
            )
        ),

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_template_variables_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        )

);

-- =============================================================================
-- UNIQUE VARIABLE CODE
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_approval_notification_template_variables_code
    ON leave_approval_notification_template_variables(
        tenant_id,
        variable_code
    );

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_approval_notification_template_variables_scope
    ON leave_approval_notification_template_variables(
        tenant_id,
        variable_scope
    );

CREATE INDEX idx_leave_approval_notification_template_variables_type
    ON leave_approval_notification_template_variables(
        tenant_id,
        notification_type
    );

CREATE INDEX idx_leave_approval_notification_template_variables_data_type
    ON leave_approval_notification_template_variables(
        tenant_id,
        data_type
    );

CREATE INDEX idx_leave_approval_notification_template_variables_active
    ON leave_approval_notification_template_variables(
        tenant_id,
        is_active
    );

CREATE INDEX idx_leave_approval_notification_template_variables_effective
    ON leave_approval_notification_template_variables(
        tenant_id,
        effective_from,
        effective_until
    );

COMMIT;