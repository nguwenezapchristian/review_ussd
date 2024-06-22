CREATE DATABASE IF NOT EXISTS feedback;
CREATE USER IF NOT EXISTS 'rugema4'@'localhost' IDENTIFIED BY 'Mitari20';
GRANT ALL PRIVILEGES ON feedback.* TO 'rugema4'@'localhost';