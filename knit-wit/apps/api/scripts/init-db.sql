-- Database initialization script for Knit-Wit
-- This script runs once when the PostgreSQL container is first created

-- Create extensions (if needed in future)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create initial schemas (placeholder for future migrations)
-- Note: In MVP, the backend is stateless and doesn't use the database
-- This script is a placeholder for future phases when we add user accounts,
-- pattern storage, and other persistent features

-- Future tables might include:
-- - users (user accounts, authentication)
-- - patterns (saved pattern configurations)
-- - exports (cached export files)
-- - analytics (usage metrics)

-- For now, just ensure the database is properly initialized
SELECT 'Knit-Wit database initialized successfully' AS status;
