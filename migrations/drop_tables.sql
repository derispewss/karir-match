-- Migrasi turun Fase 6 (SQLite).
-- Jalankan hanya pada database pengembangan; data akan hilang.

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS eval_runs;
DROP TABLE IF EXISTS relevance_judgments;
DROP TABLE IF EXISTS eval_queries;
DROP TABLE IF EXISTS recommendation_logs;
DROP TABLE IF EXISTS interaction_events;
DROP TABLE IF EXISTS search_history;
DROP TABLE IF EXISTS saved_jobs;
DROP TABLE IF EXISTS job_skills;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS job_categories;
DROP TABLE IF EXISTS user_preferences;
DROP TABLE IF EXISTS users;

PRAGMA foreign_keys = ON;
