CREATE TABLE grai.table2(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY ( id ),
    FOREIGN KEY (id) REFERENCES grai.table1(id)
);
