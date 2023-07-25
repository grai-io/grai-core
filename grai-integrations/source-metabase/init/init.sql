CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
);

INSERT INTO users (name, email, password) VALUES
  ('John Doe', 'johndoe@example.com', 'password'),
  ('Jane Doe', 'janedoe@example.com', 'password');
