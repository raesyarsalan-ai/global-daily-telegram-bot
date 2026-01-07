CREATE TABLE IF NOT EXISTS subscriptions (
    telegram_id BIGINT PRIMARY KEY,
    expires_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT,
    tx_id TEXT,
    amount NUMERIC,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
