DROP TABLE IF EXISTS grai.payments;

CREATE TABLE grai.payments(
    id int NOT NULL PRIMARY KEY,
    order_id int NOT NULL,
    payment_method text NOT NULL,
    amount int NOT NULL,
    CONSTRAINT fk_orders
       FOREIGN KEY(order_id)
        REFERENCES grai.customers(id));
