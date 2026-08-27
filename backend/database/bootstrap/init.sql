-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- Database Bootstrap
-- =============================================================================

\echo ''
\echo '=============================================='
\echo 'Quantum Workforce OS Database Bootstrap'
\echo '=============================================='
\echo ''

-- ---------------------------------------------------------------------------
-- Extensions
-- ---------------------------------------------------------------------------

\echo 'Loading Extensions...'

\i ../schema/000_extensions.sql

-- ---------------------------------------------------------------------------
-- Enums
-- ---------------------------------------------------------------------------

\echo 'Loading Enums...'

\i ../schema/001_enums.sql

-- ---------------------------------------------------------------------------
-- Domains
-- ---------------------------------------------------------------------------

\echo 'Loading Domains...'

\i ../schema/001a_domains.sql

-- ---------------------------------------------------------------------------
-- Functions
-- ---------------------------------------------------------------------------

\echo 'Loading Functions...'

\i ../functions/update_updated_at.sql

-- ---------------------------------------------------------------------------
-- Identity Schema
-- ---------------------------------------------------------------------------

\echo 'Creating Identity Schema...'

\i ../schema/002_users.sql
\i ../schema/003_user_profiles.sql
\i ../schema/004_roles.sql
\i ../schema/005_permissions.sql
\i ../schema/006_role_permissions.sql
\i ../schema/007_user_roles.sql
\i seed_rbac.sql
\i ../schema/008_sessions.sql
\i ../schema/009_session_tokens.sql
\i ../schema/010_login_history.sql
\i ../schema/011_password_resets.sql
\i ../schema/012_email_verifications.sql
\i ../schema/013_invitations.sql
\i ../schema/014_security_policies.sql

-- ---------------------------------------------------------------------------
-- HR Core
-- ---------------------------------------------------------------------------

\echo 'Creating HR Core Schema...'

\i ../schema/015_employee_number_sequences.sql
\i ../schema/016_employees.sql
\i ../schema/017_employee_profiles.sql
\i ../schema/018_employee_reporting_relationships.sql
\i ../schema/019_employee_positions.sql
\i ../schema/020_employee_immigration.sql
\i ../schema/021_employee_documents.sql
\i ../schema/022_document_definitions.sql
\i ../schema/023_document_definition_fields.sql
\i ../schema/024_document_extraction_results.sql
\i ../schema/025_document_definition_seed.sql

-- ---------------------------------------------------------------------------
-- Attendance & Payroll
-- ---------------------------------------------------------------------------

\echo 'Creating Attendance & Payroll Schema...'

\i ../schema/026_attendance_policies.sql
\i ../schema/027_employee_work_arrangements.sql
\i ../schema/028_employee_attendance_policies.sql
\i ../schema/029_employee_work_agreements.sql
\i ../schema/030_pay_calendars.sql
\i ../schema/031_pay_periods.sql
\i ../schema/032_attendance_records.sql
\i ../schema/033_attendance_events.sql
\i ../schema/034_work_schedules.sql
\i ../schema/035_work_schedule_days.sql
\i ../schema/036_employee_work_schedules.sql
-- ---------------------------------------------------------------------------
-- Triggers
-- ---------------------------------------------------------------------------

\echo 'Creating Triggers...'

\i ../triggers/audit_triggers.sql

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

\echo 'Creating Indexes...'

\i ../schema/999_indexes.sql

\echo ''
\echo '=============================================='
\echo 'Quantum Workforce OS Database Created'
\echo '=============================================='
\echo ''