-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 033_attendance_events.sql
-- Version     : 1.0
-- Description : Employee attendance event history
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- ATTENDANCE EVENTS
-- =============================================================================

CREATE TABLE attendance_events (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Attendance Record
    ---------------------------------------------------------------------------

    attendance_record_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Event Type
    --
    -- Supported values:
    --
    --     clock_in
    --     break_start
    --     break_end
    --     clock_out
    --
    ---------------------------------------------------------------------------

    event_type identifier_code
        NOT NULL,

    ---------------------------------------------------------------------------
    -- Event Timestamp
    ---------------------------------------------------------------------------

    event_at TIMESTAMPTZ NOT NULL,

    ---------------------------------------------------------------------------
    -- Event Source
    --
    -- Examples:
    --
    --     web
    --     mobile
    --     biometric
    --     admin
    --     import
    --     api
    --
    ---------------------------------------------------------------------------

    event_source identifier_code
        NOT NULL
        DEFAULT 'web',

    ---------------------------------------------------------------------------
    -- Notes
    ---------------------------------------------------------------------------

    notes TEXT,

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

    CONSTRAINT fk_attendance_events_record
        FOREIGN KEY (attendance_record_id)
        REFERENCES attendance_records(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_attendance_events_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_attendance_events_type
        CHECK (
            event_type IN (
                'clock_in',
                'break_start',
                'break_end',
                'clock_out'
            )
        ),

    CONSTRAINT chk_attendance_events_source
        CHECK (
            event_source IN (
                'web',
                'mobile',
                'biometric',
                'admin',
                'import',
                'api'
            )
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_attendance_events_record
    ON attendance_events(attendance_record_id);

CREATE INDEX idx_attendance_events_employee
    ON attendance_events(employee_id);

CREATE INDEX idx_attendance_events_timestamp
    ON attendance_events(event_at);

CREATE INDEX idx_attendance_events_type
    ON attendance_events(event_type);

CREATE INDEX idx_attendance_events_source
    ON attendance_events(event_source);

COMMIT;