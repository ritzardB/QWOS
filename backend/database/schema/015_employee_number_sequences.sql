-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 015_employee_number_sequences.sql
-- Version     : 1.0
-- Description : Tenant-specific employee number generation configuration
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores the employee-number generation configuration for each tenant.
--
-- Example:
--
--     Prefix          : QW
--     Separator       : -
--     Padding Length  : 5
--     Next Number     : 1
--
-- Produces:
--
--     QW-00001
--     QW-00002
--     QW-00003
--
-- =============================================================================

BEGIN;

CREATE TABLE employee_number_sequences (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Numbering Configuration
    ---------------------------------------------------------------------------

    prefix VARCHAR(20)
        NOT NULL,

    separator VARCHAR(10)
        NOT NULL
        DEFAULT '-',

    padding_length INTEGER
        NOT NULL
        DEFAULT 5
        CHECK (
            padding_length BETWEEN 1 AND 20
        ),

    next_number BIGINT
        NOT NULL
        DEFAULT 1
        CHECK (
            next_number >= 1
        ),

    ---------------------------------------------------------------------------
    -- Status
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

    CONSTRAINT uq_employee_number_sequences_tenant
        UNIQUE (tenant_id)

);

COMMIT;
