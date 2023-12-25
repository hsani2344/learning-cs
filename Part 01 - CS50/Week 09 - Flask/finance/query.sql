CREATE TABLE stocks (
    id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    symbol VARCHAR UNIQUE NOT NULL,
    name VARCHAR
);

CREATE TABLE users_stocks (
    id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    user_id SERIAL NOT NULL,
    stock_id SERIAL NOT NULL,
    shares INT UNSIGNED NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (stock_id) REFERENCES stocks(id)
);

CREATE TABLE history (
    id SERIAL PRIMARY KEY UNIQUE NOT NULL,
    user_id SERIAL NOT NULL,
    type VARCHAR NOT NULL,
    stock_id SERIAL NOT NULL,
    shares INT UNSIGNED NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (stocks_id) REFERENCES stocks(id)
);
