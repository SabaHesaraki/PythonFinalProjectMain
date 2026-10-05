DROP TABLE IF EXISTS records, environment_data, plants, plots, users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    full_name VARCHAR(100)
);

CREATE TABLE plots (
    id SERIAL PRIMARY KEY,
    plot_number VARCHAR(50),
    location VARCHAR(100)
);

CREATE TABLE plants (
    id SERIAL PRIMARY KEY,
    plant_name VARCHAR(100),
    plant_type VARCHAR(100)
);

CREATE TABLE environment_data (
    id SERIAL PRIMARY KEY,
    soil_type VARCHAR(50),
    ph_level NUMERIC(4,2),
    temperature NUMERIC(5,2),
    humidity NUMERIC(5,2)
);

CREATE TABLE records (
    id SERIAL PRIMARY KEY,
    record_date DATE DEFAULT CURRENT_DATE,
    user_id INT REFERENCES users(id),
    plot_id INT REFERENCES plots(id),
    plant_id INT REFERENCES plants(id),
    env_id INT REFERENCES environment_data(id),
    notes TEXT
);

DELETE FROM users WHERE username = 'admin';

INSERT INTO users (username, password, full_name)
VALUES ('admin', '123456', 'Administrator');


UPDATE users SET id = 1 WHERE username = 'admin';

SELECT setval('users_id_seq', 1, false);

