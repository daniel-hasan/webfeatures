


1. Instale o mysql
```bash
    sudo apt-get install mysql-server mysql-client
```

1. No seu mysql, configure a base de dados e o usuário

```
create database wiki_quality CHARACTER SET utf8mb4;
CREATE USER 'wiki_quality'@'127.0.0.1' IDENTIFIED BY 'all_mondega';
GRANT ALL ON *.* TO 'wiki_quality'@'127.0.0.1';
```
Note que o usuario será wiki_quality e, a senha (desenvolvimento) será all_mondega.

1. Instale o django, git, python 3.5 e o instalador do python:
```
sudo apt-get install python3 python3-pip git
```
1. Instale o django e o mysqldbda

```
pip3 install django==1.11.4
pip3 install mysqlclient
```
  - caso tenha problemas instalando o mysql pelo pip, instale por meio do apt-get: `sudo apt-get install python3-mysqldb`
mysqlclient or MySQL-python
1. Instale Demais dependencias
```
pip3 install django-bootstrap4
```
1. Clone o repositório na pasta desejada
```bash
git clone https://USUARIO@bitbucket.org/daniel-hasan/wiki-quality.git
```
  - Substitua `USUARIO` pelo seu nome de usuário no bitbucket
  
1. Na pasta  `wiki-quality-web`  do repositório:

  - atualize as tabelas:
```bash
   python3 manage.py migrate
```    
  - crie um super usuário:
```bash
python3 manage.py createsuperuser;
```





