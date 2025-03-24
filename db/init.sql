CREATE TABLE articles (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    text TEXT
);

INSERT INTO articles (id, title, text) VALUES
(1, 'Cybersecurity', 'The first article about new threats on information sec'),
(2, 'SQL-injection', 'General methods of protection against sql-injections'),
(3, 'CTF', 'How to prepare for CTF competitions');

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50)
);

INSERT INTO users (username, password) VALUES
('admin', 'CTF{Uni0n_S3l3ct_1s_P0wer}');