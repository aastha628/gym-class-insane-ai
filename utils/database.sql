-- initialising postgreSQL
-- sudo -i -u postgres
--psql

-- creating database for messaging app
CREATE DATABASE gym_app;

-- connect to DATABASE - \c gym_app

--creating user and giving it access to all the tables in the DATABASE 
CREATE USER gym_user WITH ENCRYPTED PASSWORD 'some_secure_key';

GRANT ALL PRIVILEGES ON DATABASE gym_app TO gym_user;

ALTER DEFAULT PRIVILEGES
IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO gym_user;
ALTER DEFAULT PRIVILEGES
IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO gym_user;

CREATE TABLE managers(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE gym_class(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE ,
    instructor TEXT NOT NULL ,
    time TIME NOT NULL ,
    capacity INT NOT NULL,
    current_member_count INT NOT NULL
);

CREATE TABLE members(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    contact TEXT NOT NULL UNIQUE,
    membership_type INT NOT NULL ,
    gym_class INT REFERENCES gym_class(id) ON DELETE SET NULL
);




