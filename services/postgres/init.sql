CREATE TABLE recommendation (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    anime_id INTEGER NOT NULL,
    value REAL NOT NULL,
    timestamp BIGINT NOT NULL
);

CREATE TABLE model (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    status TEXT NOT NULL,
    timestamp BIGINT NOT NULL
);
