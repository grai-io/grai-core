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
    REFERENCES db.orders(id)
);

CREATE VIEW db.customer_orders_view AS
SELECT
    c.id AS customer_id,
    c.first_name,
    c.last_name,
    o.id AS order_id,
    o.status AS order_status,
    o.order_date,
    p.id AS payment_id,
    p.payment_method,
    p.amount AS payment_amount
FROM
    db.customers c
JOIN
    db.orders o ON c.id = o.user_id
JOIN
    db.payments p ON o.id = p.order_id
WITH NO SCHEMA BINDING;
