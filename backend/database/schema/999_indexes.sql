-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 999_indexes.sql
-- Version     : 1.0.0
-- Status      : Production
-- Owner       : Database Architecture Team
--
-- Description : Shared Database Indexes
--
-- Notes:
--   - Indexes already created inside individual schema files are excluded.
--   - Index definitions must reference columns that exist in the current
--     table definitions.
--
-- =============================================================================


-- =============================================================================
-- USER ROLES
-- =============================================================================

CREATE INDEX idx_user_roles_user
    ON user_roles(user_id);

CREATE INDEX idx_user_roles_role
    ON user_roles(role_id);

CREATE INDEX idx_user_roles_enabled
    ON user_roles(is_enabled);

CREATE INDEX idx_user_roles_primary
    ON user_roles(is_primary);


-- =============================================================================
-- LOGIN HISTORY
-- =============================================================================

-- idx_login_history_user is already created by 010_login_history.sql


-- =============================================================================
-- PASSWORD RESETS
-- =============================================================================

CREATE INDEX idx_password_resets_user
    ON password_resets(user_id);

CREATE INDEX idx_password_resets_status
    ON password_resets(password_reset_status);

CREATE INDEX idx_password_resets_expires
    ON password_resets(expires_at);

CREATE INDEX idx_password_resets_requested
    ON password_resets(requested_at);


-- =============================================================================
-- EMAIL VERIFICATIONS
-- =============================================================================

CREATE INDEX idx_email_verifications_user
    ON email_verifications(user_id);

CREATE INDEX idx_email_verifications_status
    ON email_verifications(status);

CREATE INDEX idx_email_verifications_email
    ON email_verifications(email);

CREATE INDEX idx_email_verifications_expires
    ON email_verifications(expires_at);