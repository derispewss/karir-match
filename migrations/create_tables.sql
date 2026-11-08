PRAGMA foreign_keys = ON;

-- Users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    full_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Preferences (1:1)
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id INTEGER PRIMARY KEY,
    preferences_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Job taxonomy
CREATE TABLE IF NOT EXISTS job_categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS skills (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE);

-- Jobs
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    employment_type TEXT,
    experience_level TEXT,
    source TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    is_simulated BOOLEAN NOT NULL DEFAULT 0,
    posted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES job_categories(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS job_skills (
    job_id TEXT NOT NULL,
    skill_id INTEGER NOT NULL,
    PRIMARY KEY (job_id, skill_id),
    FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY(skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- Saved jobs (bookmark – idempotent)
CREATE TABLE IF NOT EXISTS saved_jobs (
    user_id INTEGER NOT NULL,
    job_id TEXT NOT NULL,
    saved_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, job_id),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Search history
CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    query TEXT NOT NULL,
    performed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Interaction events
CREATE TABLE IF NOT EXISTS interaction_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK(event_type IN ('view','click','save','apply')),
    is_simulated BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Recommendation logs
CREATE TABLE IF NOT EXISTS recommendation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id TEXT NOT NULL,
    source TEXT NOT NULL,
    rank INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Evaluation artefacts
CREATE TABLE IF NOT EXISTS eval_queries (id INTEGER PRIMARY KEY AUTOINCREMENT, query_id TEXT UNIQUE NOT NULL, query_text TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS relevance_judgments (id INTEGER PRIMARY KEY AUTOINCREMENT, query_id TEXT NOT NULL, doc_id TEXT NOT NULL, grade INTEGER NOT NULL CHECK(grade BETWEEN 0 AND 2), UNIQUE(query_id, doc_id));
CREATE TABLE IF NOT EXISTS eval_runs (id INTEGER PRIMARY KEY AUTOINCREMENT, run_name TEXT NOT NULL, run_path TEXT NOT NULL, created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

-- Indeks sesuai docs/data/database-design.md Bagian 5
CREATE INDEX IF NOT EXISTS ix_jobs_location ON jobs(location);
CREATE INDEX IF NOT EXISTS ix_jobs_category_id ON jobs(category_id);
CREATE INDEX IF NOT EXISTS ix_jobs_employment_type ON jobs(employment_type);
CREATE INDEX IF NOT EXISTS ix_jobs_experience_level ON jobs(experience_level);
CREATE INDEX IF NOT EXISTS ix_jobs_active_posted ON jobs(is_active, posted_at);
CREATE INDEX IF NOT EXISTS ix_saved_jobs_user_saved ON saved_jobs(user_id, saved_at);
CREATE INDEX IF NOT EXISTS ix_search_history_user_performed ON search_history(user_id, performed_at);
CREATE INDEX IF NOT EXISTS ix_events_user_created ON interaction_events(user_id, created_at);
CREATE INDEX IF NOT EXISTS ix_events_job_type ON interaction_events(job_id, event_type);
CREATE INDEX IF NOT EXISTS ix_events_simulated ON interaction_events(is_simulated);
CREATE INDEX IF NOT EXISTS ix_rec_logs_user_created ON recommendation_logs(user_id, created_at);
