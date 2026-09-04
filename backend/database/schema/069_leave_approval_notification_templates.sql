-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 069_leave_approval_notification_templates.sql
-- Version     : 1.0
-- Description : Leave approval notification templates
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores reusable notification templates used by the leave approval
-- notification service.
--
-- 067_leave_approval_notifications
--     = Actual notification delivery records / snapshots
--
-- 068_leave_approval_notification_preferences
--     = Employee delivery preferences
--
-- 069_leave_approval_notification_templates
--     = Reusable notification message templates
--
-- Templates are configuration data. The notification service is responsible
-- for resolving a template, replacing supported variables, and creating the
-- final notification record in 067.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE APPROVAL NOTIFICATION TEMPLATES
-- =============================================================================

CREATE TABLE leave_approval_notification_templates (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Template Identification
    ---------------------------------------------------------------------------

    template_code VARCHAR(50) NOT NULL,

    template_name VARCHAR(150) NOT NULL,

    description TEXT,

    ---------------------------------------------------------------------------
    -- Notification Type
    --
    -- Must correspond to the notification types defined in 067.
    ---------------------------------------------------------------------------

    notification_type identifier_code NOT NULL,

    ---------------------------------------------------------------------------
    -- Delivery Channel
    --
    -- Templates may be channel-specific because email, SMS, push, and
    -- in-app notifications have different formatting requirements.
    ---------------------------------------------------------------------------

    delivery_channel identifier_code NOT NULL,

    ---------------------------------------------------------------------------
    -- Subject
    --
    -- Primarily used by email and other channels supporting a subject.
    ---------------------------------------------------------------------------

    subject_template VARCHAR(255),

    ---------------------------------------------------------------------------
    -- Message
    ---------------------------------------------------------------------------

    message_template TEXT NOT NULL,

    ---------------------------------------------------------------------------
    -- Optional Template Format
    --
    -- plain_text
    -- html
    -- markdown
    ---------------------------------------------------------------------------

    content_format identifier_code NOT NULL DEFAULT 'plain_text',

    ---------------------------------------------------------------------------
    -- System / Tenant Template
    --
    -- System templates may be supplied by QWOS.
    -- Tenant templates may be customized by the tenant.
    ---------------------------------------------------------------------------

    is_system_template BOOLEAN NOT NULL DEFAULT FALSE,

    ---------------------------------------------------------------------------
    -- Default Template
    --
    -- Only one active/default template should normally be selected by the
    -- application for a given notification type and delivery channel.
    ---------------------------------------------------------------------------

    is_default BOOLEAN NOT NULL DEFAULT FALSE,

    ---------------------------------------------------------------------------
    -- Effective Period
    ---------------------------------------------------------------------------

    effective_from DATE NOT NULL DEFAULT CURRENT_DATE,

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
    -- Constraints
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_templates_code
        CHECK (BTRIM(template_code) <> ''),

    CONSTRAINT chk_leave_approval_notification_templates_name
        CHECK (BTRIM(template_name) <> ''),

    CONSTRAINT chk_leave_approval_notification_templates_message
        CHECK (BTRIM(message_template) <> ''),

    ---------------------------------------------------------------------------
    -- Notification Type
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_templates_type
        CHECK (
            notification_type IN (
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
    -- Delivery Channel
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_templates_channel
        CHECK (
            delivery_channel IN (
                'email',
                'in_app',
                'push',
                'sms'
            )
        ),

    ---------------------------------------------------------------------------
    -- Content Format
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_templates_format
        CHECK (
            content_format IN (
                'plain_text',
                'html',
                'markdown'
            )
        ),

    ---------------------------------------------------------------------------
    -- Subject
    --
    -- A subject is required for email templates.
    -- Non-email channels may omit it.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_templates_subject
        CHECK (
            (
                delivery_channel = 'email'
                AND subject_template IS NOT NULL
                AND BTRIM(subject_template) <> ''
            )
            OR
            (
                delivery_channel <> 'email'
            )
        ),

    ---------------------------------------------------------------------------
    -- HTML Content
    --
    -- HTML is meaningful only for email templates.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_templates_html
        CHECK (
            content_format <> 'html'
            OR delivery_channel = 'email'
        ),

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_templates_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        )

);

-- =============================================================================
-- UNIQUE TEMPLATE CODE
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_approval_notification_templates_code
    ON leave_approval_notification_templates(
        tenant_id,
        template_code
    );

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_approval_notification_templates_type
    ON leave_approval_notification_templates(
        tenant_id,
        notification_type
    );

CREATE INDEX idx_leave_approval_notification_templates_channel
    ON leave_approval_notification_templates(
        tenant_id,
        delivery_channel
    );

CREATE INDEX idx_leave_approval_notification_templates_type_channel
    ON leave_approval_notification_templates(
        tenant_id,
        notification_type,
        delivery_channel
    );

CREATE INDEX idx_leave_approval_notification_templates_active
    ON leave_approval_notification_templates(
        tenant_id,
        is_active
    );

CREATE INDEX idx_leave_approval_notification_templates_effective
    ON leave_approval_notification_templates(
        tenant_id,
        effective_from,
        effective_until
    );

-- =============================================================================
-- DEFAULT TEMPLATE LOOKUP
-- =============================================================================

CREATE INDEX idx_leave_approval_notification_templates_default
    ON leave_approval_notification_templates(
        tenant_id,
        notification_type,
        delivery_channel
    )
    WHERE is_default = TRUE
      AND is_active = TRUE;

COMMIT;