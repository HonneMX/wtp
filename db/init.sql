CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
	temp_lo INTEGER NOT NULL,
	temp_hi INTEGER NOT NULL

);
INSERT INTO cities (id, name, country,temp_lo,temp_hi) VALUES
(1, 'Москва', 'Россия',-22,32),
(2, 'Санкт-Петербург', 'Россия',0,32),
(3, 'Киев', 'Украина',22,32),
(4, 'Минск', 'Беларусь',-10,55),
(5, 'Лондон', 'Великобритания',-1,32);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL

);
INSERT INTO users ( name, email, password, role_id)
VALUES ( 'John', 'john@example.com', 'password123', 1),
       ( 'Mary', 'mary@example.com', 'password456', 2),
       ( 'Bob', 'bob@example.com', 'password789', 1),
       ( 'Alice', 'alice@example.com', 'password321', 3),
       ( 'Tom', 'tom@example.com', 'password654', 2);
CREATE TABLE IF NOT EXISTS tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expire_at TIMESTAMP NOT NULL

);
INSERT INTO tokens (user_id, token, expire_at)
VALUES
    (1, 'token1', '2023-03-31 23:59:59'),
    (2, 'token2', '2023-04-01 12:00:00'),
    (3, 'token3', '2023-04-15 00:00:00'),
    (4, 'token4', '2023-05-01 00:00:00'),
    (5, 'token5', '2023-06-01 00:00:00');

CREATE TABLE IF NOT EXISTS packages (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    budget FLOAT NOT NULL,
    winner_id INTEGER NOT NULL

);
INSERT INTO packages (project_id, budget, winner_id)
VALUES ( 1, 1999, 1),
       ( 2, 200000, 2),
       ( 1, 150000, 3),
       ( 1, 15000, 4),
       ( 3, 270, 5);

CREATE TABLE IF NOT EXISTS winners (
    id SERIAL PRIMARY KEY,
    package_id INTEGER NOT NULL,
    win_budget FLOAT NOT NULL,
    register_date TIMESTAMP NOT NULL

);

INSERT INTO winners ( package_id, win_budget, register_date)
VALUES ( 1, 1999,  '2023-03-31 23:59:59'),
       ( 2, 200000, '2023-03-31 23:59:59'),
       ( 3, 150000,  '2023-03-31 23:59:59'),
       ( 4, 15000, '2023-03-31 23:59:59'),
       ( 5, 270,  '2023-03-31 23:59:59');



ALTER TABLE public.tokens ADD CONSTRAINT tokens_fk FOREIGN KEY (user_id) REFERENCES public.users(id);


