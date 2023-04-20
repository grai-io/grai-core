CREATE SCHEMA IF NOT EXISTS db;

CREATE TABLE db.customers(
id INT NOT NULL PRIMARY KEY,
first_name VARCHAR(255) NOT NULL,
last_name VARCHAR(255) NOT NULL,
created_at timestamp NOT NULL
);


CREATE TABLE db.orders(
id INT NOT NULL PRIMARY KEY,
user_id INT NOT NULL,
status TEXT NOT NULL,
order_date TIMESTAMP NOT NULL,
CONSTRAINT fk_customers
   FOREIGN KEY(user_id)
   REFERENCES db.customers(id)
);


CREATE TABLE db.payments(
id INT NOT NULL PRIMARY KEY,
order_id INT NOT NULL,
payment_method TEXT NOT NULL,
amount INT NOT NULL,
CONSTRAINT fk_orders
    FOREIGN KEY(order_id)
    REFERENCES db.customers(id)
);
