-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table (Consider syncing with auth.users in production)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    plan_type VARCHAR(20) DEFAULT 'free' CHECK (plan_type IN ('free', 'premium', 'enterprise')),
    api_key VARCHAR(255) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_api_key ON users(api_key);

-- Processing Tasks table
CREATE TABLE IF NOT EXISTS processing_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    video_url TEXT NOT NULL,
    target_language VARCHAR(10) DEFAULT 'zh-CN',
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'downloading', 'transcribing', 'summarizing', 'completed', 'failed')),
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_processing_tasks_user_id ON processing_tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_processing_tasks_status ON processing_tasks(status);
CREATE INDEX IF NOT EXISTS idx_processing_tasks_created_at ON processing_tasks(created_at DESC);

-- Video Metadata table
CREATE TABLE IF NOT EXISTS video_metadata (
    task_id UUID PRIMARY KEY REFERENCES processing_tasks(id),
    title TEXT NOT NULL,
    channel_name VARCHAR(255),
    duration_seconds INTEGER,
    upload_date DATE,
    view_count BIGINT,
    thumbnail_url TEXT,
    raw_metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Summary Results table
CREATE TABLE IF NOT EXISTS summary_results (
    task_id UUID PRIMARY KEY REFERENCES processing_tasks(id),
    language VARCHAR(10) NOT NULL,
    full_summary TEXT NOT NULL,
    terminology JSONB,
    processing_time_seconds FLOAT,
    accuracy_score FLOAT CHECK (accuracy_score >= 0 AND accuracy_score <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_summary_results_language ON summary_results(language);

-- Chapter Summaries table
CREATE TABLE IF NOT EXISTS chapter_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES processing_tasks(id),
    chapter_title VARCHAR(255) NOT NULL,
    start_time_seconds INTEGER,
    end_time_seconds INTEGER,
    summary_text TEXT NOT NULL,
    key_points JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chapter_summaries_task_id ON chapter_summaries(task_id);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE processing_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE video_metadata ENABLE ROW LEVEL SECURITY;
ALTER TABLE summary_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE chapter_summaries ENABLE ROW LEVEL SECURITY;

-- Grant permissions to anon and authenticated roles (Adjust as needed for production)
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO anon, authenticated, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON processing_tasks TO anon, authenticated, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON video_metadata TO anon, authenticated, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON summary_results TO anon, authenticated, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON chapter_summaries TO anon, authenticated, service_role;

-- Basic Policies (Allow all for dev, tighten for prod)
CREATE POLICY "Enable all access for all users" ON users FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all access for all users" ON processing_tasks FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all access for all users" ON video_metadata FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all access for all users" ON summary_results FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all access for all users" ON chapter_summaries FOR ALL USING (true) WITH CHECK (true);
