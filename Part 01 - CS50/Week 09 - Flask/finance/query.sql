-- CREATE TABLE "BTC-USD" (
--     id SERIAL PRIMARY KEY UNIQUE,
--     user_id SERIAL UNIQUE NOT NULL,
--     shares INT UNSIGNED NOT NULL DEFAULT 0,
--     FOREIGN KEY (user_id) REFERENCES users(id)
-- );

-- INSERT INTO "BTC-USD"(user_id, shares)
-- VALUES (1, 1);

-- SELECT * FROM "BTC-USD" WHERE user_id = 1;

-- UPDATE "users"
-- SET cash = 89.13
-- WHERE id = 1;

CREATE TABLE "stocks" (
    id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    user_id SERIAL NOT NULL,
    symbol CHAR(15) NOT NULL,
    shares INT UNSIGNED NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- INSERT INTO stocks(user_id, symbol)
-- VALUES (1, 'NKE');

-- UPDATE stocks SET shares = 2 WHERE user_id = 1 AND symbole = 'NKE';

-- SELECT * FROM stocks
--  WHERE id = 1 AND symbol = 'NKE';

-- SELECT * FROM stocks
 -- WHERE user_id = 1;

 -- UPDATE users SET cash = 300 WHERE id = 1;


