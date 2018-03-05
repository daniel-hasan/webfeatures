sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git python3 
sudo apt-get install python-pip3
sudo apt-get install mysql-server
sudo apt-get install make
sudo mysql_secure_instalation
sudo apt-get install libmysqlclient-dev

#instalacao do mysql
==Codigo no mysql (ao começão)
CREATE USER 'wiki_quality'@'127.0.0.1' IDENTIFIED BY '_S@no=38$238ch';
GRANT ALL ON wiki_quality.* TO 'wiki_quality'@'127.0.0.1';
GRANT ALL ON test_wiki_quality.* TO 'wiki_quality'@'127.0.0.1';


==Codigo do mysql - apos instalação) 
REVOKE CREATE DROP on wikiquality.* to 'wiki_quality'@'127.0.0.1';

#Instalação do wsgi
http://pythonclub.com.br/configurando-ambiente-django-com-apache-e-mod-wsgi.html

ln -s ../sites-available/wsgi_test wsgi_test
#django enviroment variables wqual_SECRET_KEY ewqual_db_PASSWORD
vim /etc/enviroment
#criando o ambientevirtual
virtualenv ~/wqual-env -p /usr/bin/python3
#ativando o ambiente virtual
source wqual-env/bin/activate
#desativando ambiente virtual
deactivate

#termono da instalasao do wsgi
colocar em sudo vim /etc/apache2/envvars :
	export LANG='en_US.UTF-8'
	export LC_ALL='en_US.UTF-8'
#alterar o arquivo init para apontar para as configurações de produção
vim wiki-quality-web/wiki_quality_web/settings/__init__.py 

#copiar o arquivo ".conf" para a producao
sudo cp deploy/django_wqual.conf /etc/apache2/sites-available/.

"
