-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 071_leave_approval_notification_delivery_logs.sql
-- Version     : 1.0
-- Description : Leave approval notification delivery attempt history
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records each delivery attempt made for a leave approval notification.
--
-- 067_leave_approval_notifications
--     = Notification record and final rendered message
--
-- 068_leave_approval_notification_preferences
--     = Employee delivery preferences
--
-- 069_leave_approval_notification_templates
--     = Reusable notification templates
--
-- 070_leave_approval_notification_template_variables
--     = Controlled template variable registry
--
-- 071_leave_approval_notification_delivery_logs
--     = Individual delivery attempts and provider responses
--
-- This table is an operational/audit log. It must not replace the notification
-- status stored in 067.
--
-- A single notification may have multiple delivery attempts.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE APPROVAL NOTIFICATION DELIVERY LOGS
-- =============================================================================

CREATE TABLE leave_approval_notification_delivery_logs (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Notification
    ---------------------------------------------------------------------------

    leave_approval_notification_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Recipient
    ---------------------------------------------------------------------------

    recipient_employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Delivery Channel
    --
    -- email
    -- in_app
    -- push
    -- sms
    ---------------------------------------------------------------------------

    delivery_channel identifier_code NOT NULL,

    ---------------------------------------------------------------------------
    -- Attempt
    ---------------------------------------------------------------------------

    attempt_number INTEGER NOT NULL DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Delivery Status
    --
    -- pending
    -- queued
    -- sent
    -- delivered
    -- failed
    -- cancelled
    ---------------------------------------------------------------------------

    status identifier_code NOT NULL DEFAULT 'pending',

    ---------------------------------------------------------------------------
    -- Provider
    --
    -- Examples:
    -- smtp
    -- sendgrid
    -- twilio
    -- firebase
    -- internal
    --
    -- Provider selection remains an application configuration concern.
    ---------------------------------------------------------------------------

    provider_code VARCHAR(100),

    ---------------------------------------------------------------------------
    -- Provider Reference
    --
    -- External message ID / delivery ID returned by the provider.
    ---------------------------------------------------------------------------

    provider_message_id VARCHAR(255),

    ---------------------------------------------------------------------------
    -- Attempt Timing
    ---------------------------------------------------------------------------

    attempted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    queued_at TIMESTAMPTZ,

    sent_at TIMESTAMPTZ,

    delivered_at TIMESTAMPTZ,

    failed_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Response Information
    ---------------------------------------------------------------------------

    provider_status_code VARCHAR(100),

    provider_response TEXT,

    failure_code VARCHAR(100),

    failure_reason TEXT,

    ---------------------------------------------------------------------------
    -- Retry
    ---------------------------------------------------------------------------

    retryable BOOLEAN NOT NULL DEFAULT FALSE,

    next_retry_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Request Metadata
    --
    -- Stores non-sensitive operational information useful for diagnostics.
    -- Do not store passwords, tokens, secrets, or full authentication data.
    ---------------------------------------------------------------------------

    request_reference VARCHAR(255),

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

    CONSTRAINT fk_leave_approval_notification_delivery_logs_notification
        FOREIGN KEY (leave_approval_notification_id)
        REFERENCES leave_approval_notifications(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_approval_notification_delivery_logs_employee
        FOREIGN KEY (recipient_employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Attempt Number
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_delivery_logs_attempt
        CHECK (
            attempt_number > 0
        ),

    ---------------------------------------------------------------------------
    -- Delivery Channel
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_delivery_logs_channel
        CHECK (
            delivery_channel IN (
                'email',
                'in_app',
                'push',
                'sms'
            )
        ),

    ---------------------------------------------------------------------------
    -- Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_delivery_logs_status
        CHECK (
            status IN (
                'pending',
                'queued',
                'sent',
                'delivered',
                'failed',
                'cancelled'
            )
        ),

    ---------------------------------------------------------------------------
    -- Provider
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_delivery_logs_provider
        CHECK (
            provider_code IS NULL
            OR BTRIM(provider_code) <> ''
        ),

    ---------------------------------------------------------------------------
    -- Provider Message ID
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_delivery_logs_provider_id
        CHECK (
            provider_message_id IS NULL
            OR BTRIM(provider_message_id) <> ''
        ),

    ---------------------------------------------------------------------------
    -- Failure Information
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_delivery_logs_failure
        CHECK (
            status <> 'failed'
            OR (
                failed_at IS NOT NULL
                AND (
                    failure_code IS NOT NULL
                    OR failure_reason IS NOT NULL
                )
            )
        ),

    ---------------------------------------------------------------------------
    -- Retry Information
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_delivery_logs_retry
        CHECK (
            retryable = TRUE
            OR next_retry_at IS NULL
        ),

    CONSTRAINT chk_leave_approval_notification_delivery_logs_retry_status
        CHECK (
            next_retry_at IS NULL
            OR status = 'failed'
        ),

    ---------------------------------------------------------------------------
    -- Delivery Timestamps
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_delivery_logs_timestamps
        CHECK (
            queued_at IS NULL
            OR queued_at >= attempted_at
        ),

    CONSTRAINT chk_leave_approval_notification_delivery_logs_sent_timestamp
        CHECK (
            sent_at IS NULL
            OR sent_at >= attempted_at
        ),

    CONSTRAINT chk_leave_approval_notification_delivery_logs_delivered_timestamp
        CHECK (
            delivered_at IS NULL
            OR (
                sent_at IS NOT NULL
                AND delivered_at >= sent_at
            )
        ),

    CONSTRAINT chk_leave_approval_notification_delivery_logs_failed_timestamp
        CHECK (
            failed_at IS NULL
            OR failed_at >= attempted_at
        ),

    ---------------------------------------------------------------------------
    -- Status / Timestamp Consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_delivery_logs_status_timestamp
        CHECK (
            (
                status <> 'queued'
                OR queued_at IS NOT NULL
            )
            AND
            (
                status NOT IN ('sent', 'delivered')
                OR sent_at IS NOT NULL
            )
            AND
            (
                status <> 'delivered'
                OR delivered_at IS NOT NULL
            )
            AND
            (
                status <> 'failed'
                OR failed_at IS NOT NULL
            )
        )

);

-- =============================================================================
-- UNIQUE ATTEMPT
-- =============================================================================
--
-- One delivery attempt number per notification and delivery channel.
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_approval_notification_delivery_logs_attempt
    ON leave_approval_notification_delivery_logs(
        tenant_id,
        leave_approval_notification_id,
        delivery_channel,
        attempt_number
    );

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_approval_notification_delivery_logs_notification
    ON leave_approval_notification_delivery_logs(
        tenant_id,
        leave_approval_notification_id
    );

CREATE INDEX idx_leave_approval_notification_delivery_logs_employee
    ON leave_approval_notification_delivery_logs(
        tenant_id,
        recipient_employee_id
    );

CREATE INDEX idx_leave_approval_notification_delivery_logs_channel
    ON leave_approval_notification_delivery_logs(
        tenant_id,
        delivery_channel
    );

CREATE INDEX idx_leave_approval_notification_delivery_logs_status
    ON leave_approval_notification_delivery_logs(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_approval_notification_delivery_logs_provider
    ON leave_approval_notification_delivery_logs(
        tenant_id,
        provider_code
    );

CREATE INDEX idx_leave_approval_notification_delivery_logs_attempted
    ON leave_approval_notification_delivery_logs(
        tenant_id,
        attempted_at
    );

CREATE INDEX idx_leave_approval_notification_delivery_logs_retry
    ON leave_approval_notification_delivery_logs(
        tenant_id,
        next_retry_at
    )
    WHERE retryable = TRUE
      AND status = 'failed';

CREATE INDEX idx_leave_approval_notification_delivery_logs_active
    ON leave_approval_notification_delivery_logs(
        tenant_id,
        is_active
    );

COMMIT;