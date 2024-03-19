CREATE SCHEMA IF NOT EXISTS grai;
DROP TABLE IF EXISTS grai.customers;

CREATE TABLE grai.customers(
    id INT NOT NULL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    created_at timestamp NOT NULL
);
