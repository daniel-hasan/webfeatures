create database wiki_quality CHARACTER SET utf8mb4;
CREATE USER 'wiki_quality'@127.0.0.1 IDENTIFIED BY 'all_mondega';
GRANT ALL ON *.* TO 'wiki_quality'@127.0.0.1;
