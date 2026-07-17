-- ============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- Database Extensions
--
-- File: 000_extensions.sql
-- Version: 1.0
-- Author: Richard Balabarcon
-- ============================================================================
--
-- Purpose
-- -------
-- Installs PostgreSQL extensions required by Quantum Workforce OS.
--
-- Notes
-- -----
-- This file must execute before all other schema scripts.
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Cryptographic Functions
-- ----------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ----------------------------------------------------------------------------
-- Case-insensitive text comparisons
-- ----------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS citext;

-- ----------------------------------------------------------------------------
-- UUID support (reserved for interoperability)
-- ----------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

COMMIT;