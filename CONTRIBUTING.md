


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
pip3 install django
pip3 install mysqlclient
```
  - caso tenha problemas instalando o mysql pelo pip, instale por meio do apt-get: `sudo apt-get install python3-mysqldb`
mysqlclient or MySQL-python
1. crie um super usuário
```bash
python3 manage.py createsuperuser;
```

1. Clone o repositório na pasta desejada


## Criação de novas funcionalidades

1. Crie um novo branch chamado `feat-usuario-NUM` sendo que `NUM` é o número da funcionalidade (use o número da tarefa REDMINE) e usuário é o nome do usuário no git. Note que a abreviatura `feat` vem de
feature, ou seja, uma funcionalidade no software.
Veja o exemplo em que o usuário é `daniel-hasan` e o código da funcionalidade é `123`:
```bash
git branch func-daniel-hasan-123
```
1. Obtenha este branch no seu repositório local:
```bash
git checkout func-daniel-hasan-123
```
1. Trabalhe neste branch dando quantos commits/push necessários.
1. Atualize frequentemente seu branch com o branch `master`. Assim,
menos erros ocorrerão quando for fazer o merge com o branch `master`. Para isso,
execute em seu branch:
```bash
git rebase master
```
  - Corrija os conflitos que podem ocorrer e faça os testes unitários para verificar se o seu código ainda funciona.

1. Quando finalizada esta funcionalidade, volte para o branch `master`:
```bash
git checkout master
```
1. Obtenha a ultima versão do master:
```bash
git pull
```
1. Insira as modificações do branch criado no branch `master`:
```bash
  git merge func-daniel-hasan-123 --no-ff -m "escreva aqui o que foi modificado"
```
  - Caso tenha algum conflito, resolva-os
1. **Teste a funcionalidade no branch master** e faça todos os testes unitários existentes na aplicação. Faça (na pasta `wiki_quality-web`)
```bash
  python3 manage.py test wqual
```
  - Corrija possíveis erros que irão ocorrer. Apenas envie estas modificações após corrigir todos os erros.

1. Caso esteja tudo ok, remova o branch
```bash
git branch -d func-daniel-hasan-123
```
1. Por fim, envie essas modificações para o repositório remoto
```bash
  git push origin master
```
