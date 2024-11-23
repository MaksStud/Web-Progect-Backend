CREATE DATABASE webdevbackend;
CREATE USER webdevbackend WITH PASSWORD 'qwerty123';
GRANT ALL PRIVILEGES ON DATABASE webdevbackend TO webdevbackend;
ALTER USER webdevbackend CREATEDB;