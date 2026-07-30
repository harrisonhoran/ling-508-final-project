CREATE DATABASE IF NOT EXISTS transcript_parser_app;
USE transcript_parser_app;

CREATE TABLE podcast (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE transcript (
    id INT AUTO_INCREMENT PRIMARY KEY,
    podcast_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    raw_text LONGTEXT,
    clean_text LONGTEXT,
    mode VARCHAR(50) NOT NULL,
    FOREIGN KEY (podcast_id) REFERENCES podcast(id)
);

CREATE TABLE dialogue (
    id INT AUTO_INCREMENT PRIMARY_KEY,
    transcript_id INT NOT NULL,
    speaker VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    timestamp INT,
    'order' INT DEFAULT 1,
    FOREIGN KEY (transcript_id) REFERENCES transcript(id)
);