


1. Instale o mysql
```bash
  sudo apt-get install mysql-server
```

1. No seu mysql, configure a base de dados e o usuário

```
create database wiki_quality CHARACTER SET utf8mb4;
CREATE USER 'wiki_quality'@'localhost' IDENTIFIED BY 'all_mondega';
GRANT ALL ON wiki_quality.* TO 'wiki_quality'@'localhost';
```
Note que o usuario será wiki_quality e, a senha será all_mondega.

1. Instale o django, python 3.5 e o instalador do python:
```
sudo apt-get install python3 python3-pip
```
1. Instale o django e o mysqlDB

```
pip3 install django
pip3 install mysqldbda
```

1. crie um super usuário
```bash
python3 manage.py createsuperuser;
```

## Criação de novas funcionalidades

1. Crie um novo branch chamado `func-usuario-NUM` sendo que `NUM` é o número da funcionalidade (use o número da tarefa REDMINE) e usuario é o nome do usuário no git.
Veja o exemplo em que o usuário é `daniel-hasan` e o código da funcionalidade é `123`:
```bash
git branch func-daniel-hasan-123
```
1. Obtenha este branch no seu repositório local:
```bash
git branch func-daniel-hasan-123
```
1. Trabalhe neste branch dando quantos commits/push necessários.
1. Quando finalizada esta funcionalidade, volte para o branch `master`:
```bash
git checkout master
```
1. Insira as modificações do branch criado no branch `master`:
```bash
  git merge func-daniel-hasan-123
```
1. Caso tenha algum conflito, resolva-os
1. **Teste a funcionalidade no branch master** e faça todos os testes unitários existentes na aplicação.
1. Caso esteja tudo ok, envie essas modificações para o repositório remoto
```bash
  git push origin master
```
