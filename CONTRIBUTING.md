


Instale o mysql 

No seu mysql, configure a base de dados e o usuário

create database wiki_quality CHARACTER SET utf8mb4;


CREATE USER 'wiki_quality'@'localhost' IDENTIFIED BY 'all_mondega';
GRANT ALL ON wiki_quality.* TO 'wiki_quality'@'localhost';


python3 manage.py createsuperuser;
