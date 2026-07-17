CREATE INDEX idx_user_roles_user
ON user_roles(user_id);

CREATE INDEX idx_user_roles_role
ON user_roles(role_id);

CREATE INDEX idx_user_roles_enabled
ON user_roles(is_enabled);

CREATE INDEX idx_user_roles_primary
ON user_roles(is_primary);

CREATE INDEX idx_refresh_tokens_session
ON refresh_tokens(session_id);

CREATE INDEX idx_refresh_tokens_user
ON refresh_tokens(user_id);

CREATE INDEX idx_refresh_tokens_active
ON refresh_tokens(is_active);

CREATE INDEX idx_refresh_tokens_expiry
ON refresh_tokens(expires_at);

CREATE INDEX idx_login_history_user
ON login_history(user_id);

CREATE INDEX idx_login_history_attempted_at
ON login_history(attempted_at);

CREATE INDEX idx_login_history_result
ON login_history(login_result);

CREATE INDEX idx_login_history_email
ON login_history(email_attempted);

CREATE INDEX idx_password_resets_user
ON password_resets(user_id);

CREATE INDEX idx_password_resets_status
ON password_resets(password_reset_status);

CREATE INDEX idx_password_resets_expires
ON password_resets(expires_at);

CREATE INDEX idx_password_resets_requested
ON password_resets(requested_at);

CREATE INDEX idx_email_verifications_user
ON email_verifications(user_id);

CREATE INDEX idx_email_verifications_status
ON email_verifications(status);

CREATE INDEX idx_email_verifications_email
ON email_verifications(email);

CREATE INDEX idx_email_verifications_expires
ON email_verifications(expires_at);