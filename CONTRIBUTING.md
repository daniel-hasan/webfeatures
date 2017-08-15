Colocar como variavel de ambiente `WQUAL_TEMPLATE_DIR` o endereço dos templates na sua maquina

No ubuntu, você configura a variável de ambiente em `/etc/environment`
Exemplo: 
WQUAL_TEMPLATE_DIR=/home/aluno/git/wiki-quality/wiki-quality-web/templates

Instale o mysql 

No seu mysql, configure a base de dados e o usuário

create database wiki_quality;
CREATE USER 'wiki_quality'@'localhost' IDENTIFIED BY 'all_mondega';
GRANT ALL ON wiki_quality.* TO 'wiki_quality'@'localhost';
