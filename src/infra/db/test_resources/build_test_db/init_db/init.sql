CREATE TABLE IF NOT EXISTS connections (
    user_name VARCHAR(255) PRIMARY KEY,
    Company VARCHAR(255),
    Position VARCHAR(255),
    Connected_On DATE
);

INSERT INTO connections (user_name, Company, Position, Connected_On) VALUES
('john_doe', 'ABC Corp', 'Software Engineer', '2024-02-10'),
('jane_smith', 'XYZ Inc', 'Marketing Manager', '2024-02-11'),
('bob_jones', '123 Company', 'Sales Representative', '2024-02-12'),
('alice_williams', 'Acme Co', 'Product Manager', '2024-02-12'),
('sam_brown', 'Tech Solutions', 'IT Consultant', '2024-02-13');