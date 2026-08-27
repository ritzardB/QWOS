-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 036_employee_work_schedules.sql
-- Version     : 1.0
-- Description : Effective-dated employee work schedule assignments
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE WORK SCHEDULES
-- =============================================================================

CREATE TABLE employee_work_schedules (

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
    -- Work Schedule
    ---------------------------------------------------------------------------

    work_schedule_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    effective_from DATE NOT NULL,

    effective_until DATE,

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

    CONSTRAINT fk_employee_work_schedules_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_employee_work_schedules_schedule
        FOREIGN KEY (work_schedule_id)
        REFERENCES work_schedules(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_work_schedules_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        ),

    CONSTRAINT uq_employee_work_schedules_start
        UNIQUE (
            tenant_id,
            employee_id,
            effective_from
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employee_work_schedules_employee
    ON employee_work_schedules(employee_id);

CREATE INDEX idx_employee_work_schedules_schedule
    ON employee_work_schedules(work_schedule_id);

CREATE INDEX idx_employee_work_schedules_active
    ON employee_work_schedules(is_active);

CREATE INDEX idx_employee_work_schedules_effective
    ON employee_work_schedules(
        employee_id,
        effective_from,
        effective_until
    );

COMMIT;