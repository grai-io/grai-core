CREATE SCHEMA grai;
GO
CREATE TABLE grai.table1(
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL,
);
GO
CREATE TABLE grai.table2(
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (id) REFERENCES grai.table1(id)
);
GO
