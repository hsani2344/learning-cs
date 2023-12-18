-- CREATE TABLE "BTC-USD" (
--     id SERIAL PRIMARY KEY UNIQUE,
--     user_id SERIAL UNIQUE NOT NULL,
--     shares INT UNSIGNED NOT NULL DEFAULT 0,
--     FOREIGN KEY (user_id) REFERENCES users(id)
-- );

-- INSERT INTO "BTC-USD"(user_id, shares)
-- VALUES (1, 1);

SELECT * FROM "BTC-USD" WHERE user_id = 1;
