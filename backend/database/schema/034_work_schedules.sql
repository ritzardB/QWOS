-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 034_work_schedules.sql
-- Version     : 1.0
-- Description : Reusable work schedule definitions
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- WORK SCHEDULES
-- =============================================================================

CREATE TABLE work_schedules (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Schedule Identity
    ---------------------------------------------------------------------------

    schedule_code VARCHAR(50) NOT NULL,

    schedule_name VARCHAR(150) NOT NULL,

    ---------------------------------------------------------------------------
    -- Timezone
    --
    -- IANA timezone identifier used when interpreting schedule times.
    --
    -- Examples:
    --
    --     Asia/Dubai
    --     Asia/Manila
    --     Europe/London
    --
    ---------------------------------------------------------------------------

    timezone VARCHAR(100) NOT NULL
        DEFAULT 'UTC',

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    is_active BOOLEAN
        NOT NULL
        DEFAULT TRUE,

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

    CONSTRAINT uq_work_schedules_code
        UNIQUE (
            tenant_id,
            schedule_code
        ),

    CONSTRAINT chk_work_schedules_code
        CHECK (
            LENGTH(TRIM(schedule_code)) > 0
        ),

    CONSTRAINT chk_work_schedules_name
        CHECK (
            LENGTH(TRIM(schedule_name)) > 0
        ),

    CONSTRAINT chk_work_schedules_timezone
        CHECK (
            LENGTH(TRIM(timezone)) > 0
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_work_schedules_active
    ON work_schedules(is_active);

CREATE INDEX idx_work_schedules_tenant
    ON work_schedules(tenant_id);

CREATE INDEX idx_work_schedules_timezone
    ON work_schedules(timezone);

COMMIT;