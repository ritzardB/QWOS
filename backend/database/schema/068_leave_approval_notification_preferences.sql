-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 068_leave_approval_notification_preferences.sql
-- Version     : 1.0
-- Description : Leave approval notification preferences
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores employee preferences for receiving leave-related approval
-- notifications.
--
-- This table defines notification preferences.
--
-- 067_leave_approval_notifications
--     = Actual notification delivery records
--
-- 068_leave_approval_notification_preferences
--     = Employee notification preferences
--
-- The notification service remains responsible for evaluating these
-- preferences before creating/delivering notifications.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE APPROVAL NOTIFICATION PREFERENCES
-- =============================================================================

CREATE TABLE leave_approval_notification_preferences (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Notification Type
    --
    -- approval_required
    -- approval_approved
    -- approval_rejected
    -- approval_escalated
    -- approval_delegated
    -- leave_submitted
    -- leave_withdrawn
    -- leave_cancelled
    ---------------------------------------------------------------------------

    notification_type identifier_code NOT NULL,

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
    -- Enabled
    ---------------------------------------------------------------------------

    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,

    ---------------------------------------------------------------------------
    -- Optional Quiet Hours
    ---------------------------------------------------------------------------

    quiet_hours_enabled BOOLEAN NOT NULL DEFAULT FALSE,

    quiet_hours_start TIME,

    quiet_hours_end TIME,

    ---------------------------------------------------------------------------
    -- Digest Configuration
    --
    -- none
    -- daily
    -- weekly
    ---------------------------------------------------------------------------

    digest_frequency identifier_code NOT NULL DEFAULT 'none',

    digest_time TIME,

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
    -- Foreign Keys
    ---------------------------------------------------------------------------

    CONSTRAINT fk_leave_approval_notification_preferences_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Notification Type
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_preferences_type
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

    CONSTRAINT chk_leave_approval_notification_preferences_channel
        CHECK (
            delivery_channel IN (
                'email',
                'in_app',
                'push',
                'sms'
            )
        ),

    ---------------------------------------------------------------------------
    -- Quiet Hours
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_preferences_quiet_hours
        CHECK (
            (
                quiet_hours_enabled = FALSE
                AND quiet_hours_start IS NULL
                AND quiet_hours_end IS NULL
            )
            OR
            (
                quiet_hours_enabled = TRUE
                AND quiet_hours_start IS NOT NULL
                AND quiet_hours_end IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Digest Frequency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_preferences_digest
        CHECK (
            digest_frequency IN (
                'none',
                'daily',
                'weekly'
            )
        ),

    ---------------------------------------------------------------------------
    -- Digest Time
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_preferences_digest_time
        CHECK (
            (
                digest_frequency = 'none'
                AND digest_time IS NULL
            )
            OR
            (
                digest_frequency IN ('daily', 'weekly')
                AND digest_time IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_approval_notification_preferences_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        )

);

-- =============================================================================
-- UNIQUE CONSTRAINT
-- =============================================================================
--
-- One preference definition per employee, notification type, and channel.
--
-- Effective-dated historical versions can be introduced later through
-- application-level versioning or by extending this constraint if the
-- notification-preference model requires multiple historical records.
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_approval_notification_preferences
    ON leave_approval_notification_preferences(
        tenant_id,
        employee_id,
        notification_type,
        delivery_channel
    );

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_approval_notification_preferences_employee
    ON leave_approval_notification_preferences(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_approval_notification_preferences_type
    ON leave_approval_notification_preferences(
        tenant_id,
        notification_type
    );

CREATE INDEX idx_leave_approval_notification_preferences_channel
    ON leave_approval_notification_preferences(
        tenant_id,
        delivery_channel
    );

CREATE INDEX idx_leave_approval_notification_preferences_enabled
    ON leave_approval_notification_preferences(
        tenant_id,
        is_enabled
    );

CREATE INDEX idx_leave_approval_notification_preferences_effective
    ON leave_approval_notification_preferences(
        tenant_id,
        effective_from,
        effective_until
    );

CREATE INDEX idx_leave_approval_notification_preferences_active
    ON leave_approval_notification_preferences(
        tenant_id,
        is_active
    );

COMMIT;