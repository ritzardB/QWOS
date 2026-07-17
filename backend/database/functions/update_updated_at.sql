-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 001b_functions.sql
-- Version     : 1.0
-- Description : Shared Database Functions
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Contains reusable PostgreSQL functions used throughout Quantum Workforce OS.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- Function: update_updated_at()
--
-- Automatically updates the updated_at column whenever a row changes.
-- =============================================================================

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS
$$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

COMMIT;