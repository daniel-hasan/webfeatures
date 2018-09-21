


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

Comandos uteis do Django no projeto: 

- `python3 manage.py createsuperuser`: Cria o super usuário (útil para abrirmos a parte do admin). 

- `python3 manage.py runshell`: Abre o shell do python com o ambiente Django configurado, assim, podemos testar comandos python (e consultas ao banco, por exemplo)

- `python3 manage.py tests wqual.tests`: executa todos os testes presentes em `wqual.tests`

- `python3 manage.py makemigrations`: Cria novos scripts para executar criação/alteração de colunas/tabelas  no banco de dados.

- `python3 manage.py migrate`: aplica e reverte os scripts feitos por `makemigrations`.



# Configurando o ambiente no Eclipse

Após clonado o repositório e configurado o ambiente, para configurar o eclipse faça o seguinte:

- Instale o Pydev [veja este exemplo de instalação](http://www.vogella.com/tutorials/Python/article.html). Ao configurar o interpretador do python, confirme se a versão é superior a 3.0. 


Você deverá criar dois projetos: um projeto DJango e um projeto python. 

Para criar o **projeto python**: 

- Vá em `Arquivo`->`novo`->`PyDev Project`. As vezes, poderá estar em "outro"

- De um nome ao projeto e coloque a versão da gramática do interpretador como 3.0-3.5 e selecione o interpretador de seu Python (não esqueça que ele deve ser versão>3.0, de preferencia, 3.5)

- Selecione "Create links to existing sources" (as vezes, esse radio button "se esconde" é o terceiro após 'Create 'src' folder and add it to the PYTHONPATH). Clique em avançar

- Adicione a pasta `wiki-quality`. Quando damos o clone, a pasta de nosso repositório chamará `wiki-quality`, mas não é essa pasta que você deve referenciar e sim a pasta que está dentro do repositório que chama também `wiki-quality` (ou seja, `wiki-quality/wiki-quality`. Avance e clique em finalizar.

Para criar o **projeto Django** 

- Vá em `arquivo`->`novo`->`outros` e vá na pasta `PyDev` selecione "Django Project`
- De um nome ao projeto e coloque a versão da gramática do interpretador como 3.0-3.5 e selecione o interpretador de seu Python (não esqueça que ele deve ser versão>3.0, de preferencia, 3.5)
- Selecione "Create links to existing sources" (as vezes, esse radio button "se esconde" é o terceiro após 'Create 'src' folder and add it to the PYTHONPATH). Clique em avançar

- Adicione a pasta `wiki-quality-web` que está em nosso repositório. Clique em avançar

- Adicione como dependencia o projeto Python recém criado.

- Clique em avançar e, logo após, finalizar.

- Você irá verificar que, além da pasta que referenciamos `wiki-quality-web` o Eclipse criou outra pasta. Exclua ela.

- Clique com o botão direito no projeto Django, vá em propriedades->PyDev Django e defina as propriedades `Django manage.py` como `wiki-quality-web/manage.py` e, `django settings module` como `wiki_quality_web.settings.development`. Isso facilitará para executar alguns comandos do próprio settings. Mas, caso queira mexer no projeto (testar, abrir o ambiente, por exemplo) recomendo o terminal com os comandos úteis já apresentados antes desta seção. 




