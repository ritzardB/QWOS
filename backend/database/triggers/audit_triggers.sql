-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 001c_triggers.sql
-- Version     : 1.1
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
-- This script is intentionally idempotent so it can be safely re-run during
-- development, database rebuilds, and bootstrap operations.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- USERS
-- =============================================================================

DROP TRIGGER IF EXISTS trg_users_updated_at ON users;

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE
ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- USER PROFILES
-- =============================================================================

DROP TRIGGER IF EXISTS trg_user_profiles_updated_at ON user_profiles;

CREATE TRIGGER trg_user_profiles_updated_at
BEFORE UPDATE
ON user_profiles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- ROLES
-- =============================================================================

DROP TRIGGER IF EXISTS trg_roles_updated_at ON roles;

CREATE TRIGGER trg_roles_updated_at
BEFORE UPDATE
ON roles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- EMPLOYEE NUMBER SEQUENCES
-- =============================================================================

DROP TRIGGER IF EXISTS trg_employee_number_sequences_updated_at
ON employee_number_sequences;

CREATE TRIGGER trg_employee_number_sequences_updated_at
BEFORE UPDATE
ON employee_number_sequences
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- EMPLOYEES
-- =============================================================================

DROP TRIGGER IF EXISTS trg_employees_updated_at ON employees;

CREATE TRIGGER trg_employees_updated_at
BEFORE UPDATE
ON employees
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- EMPLOYEE PROFILES
-- =============================================================================

DROP TRIGGER IF EXISTS trg_employee_profiles_updated_at
ON employee_profiles;

CREATE TRIGGER trg_employee_profiles_updated_at
BEFORE UPDATE
ON employee_profiles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- EMPLOYEE RELATIONSHIPS
-- =============================================================================

DROP TRIGGER IF EXISTS trg_employee_reporting_relationships_updated_at
ON employee_reporting_relationships;

CREATE TRIGGER trg_employee_reporting_relationships_updated_at
BEFORE UPDATE
ON employee_reporting_relationships
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- EMPLOYEE IMMIGRATION
-- =============================================================================

DROP TRIGGER IF EXISTS trg_employee_immigration_updated_at
ON employee_immigration;

CREATE TRIGGER trg_employee_immigration_updated_at
BEFORE UPDATE
ON employee_immigration
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- EMPLOYEE DOCUMENTS
-- =============================================================================

DROP TRIGGER IF EXISTS trg_employee_documents_updated_at
ON employee_documents;

CREATE TRIGGER trg_employee_documents_updated_at
BEFORE UPDATE
ON employee_documents
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

COMMIT;