-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 035_work_schedule_days.sql
-- Version     : 1.0
-- Description : Weekly day rules for reusable work schedules
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- WORK SCHEDULE DAYS
-- =============================================================================

CREATE TABLE work_schedule_days (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Work Schedule
    ---------------------------------------------------------------------------

    work_schedule_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Day of Week
    --
    -- ISO-style numbering:
    --
    --     1 = Monday
    --     2 = Tuesday
    --     3 = Wednesday
    --     4 = Thursday
    --     5 = Friday
    --     6 = Saturday
    --     7 = Sunday
    --
    ---------------------------------------------------------------------------

    day_of_week SMALLINT NOT NULL,

    ---------------------------------------------------------------------------
    -- Day Type
    --
    --     workday
    --     rest_day
    --
    ---------------------------------------------------------------------------

    day_type identifier_code
        NOT NULL
        DEFAULT 'workday',

    ---------------------------------------------------------------------------
    -- Working Times
    ---------------------------------------------------------------------------

    start_time TIME,

    end_time TIME,

    ---------------------------------------------------------------------------
    -- Break
    ---------------------------------------------------------------------------

    break_minutes INTEGER
        NOT NULL
        DEFAULT 0,

    ---------------------------------------------------------------------------
    -- Overnight Shift
    --
    -- TRUE when the shift crosses midnight.
    --
    ---------------------------------------------------------------------------

    is_overnight BOOLEAN
        NOT NULL
        DEFAULT FALSE,

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

    CONSTRAINT fk_work_schedule_days_schedule
        FOREIGN KEY (work_schedule_id)
        REFERENCES work_schedules(id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_work_schedule_days_schedule_day
        UNIQUE (
            tenant_id,
            work_schedule_id,
            day_of_week
        ),

    CONSTRAINT chk_work_schedule_days_day
        CHECK (
            day_of_week BETWEEN 1 AND 7
        ),

    CONSTRAINT chk_work_schedule_days_type
        CHECK (
            day_type IN (
                'workday',
                'rest_day'
            )
        ),

    CONSTRAINT chk_work_schedule_days_break
        CHECK (
            break_minutes >= 0
        ),

    CONSTRAINT chk_work_schedule_days_times
        CHECK (
            (
                day_type = 'rest_day'
                AND start_time IS NULL
                AND end_time IS NULL
                AND break_minutes = 0
            )
            OR
            (
                day_type = 'workday'
                AND start_time IS NOT NULL
                AND end_time IS NOT NULL
            )
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_work_schedule_days_schedule
    ON work_schedule_days(work_schedule_id);

CREATE INDEX idx_work_schedule_days_day
    ON work_schedule_days(day_of_week);

CREATE INDEX idx_work_schedule_days_type
    ON work_schedule_days(day_type);

COMMIT;