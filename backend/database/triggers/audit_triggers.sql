-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 001c_triggers.sql
-- Version     : 1.0
-- Description : Shared Database Triggers
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Creates triggers that automatically maintain audit information.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- USERS
-- =============================================================================

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE
ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- USER PROFILES
-- =============================================================================

CREATE TRIGGER trg_user_profiles_updated_at
BEFORE UPDATE
ON user_profiles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- ROLES
-- =============================================================================

CREATE TRIGGER trg_roles_updated_at
BEFORE UPDATE
ON roles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

COMMIT;