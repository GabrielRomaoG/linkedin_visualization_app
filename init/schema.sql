CREATE TABLE IF NOT EXISTS connections (
    user_name VARCHAR(255) PRIMARY KEY,
    Company VARCHAR(255),
    Position VARCHAR(255),
    Connected_On DATE
);

CREATE TABLE IF NOT EXISTS shares (
    share_id VARCHAR(21) PRIMARY KEY,
    shared_date DATE,
    num_of_comments INT,
    num_of_likes INT
)