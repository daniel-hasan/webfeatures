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



#apache 
sudo apt-get install apache2 libapache2-mod-wsgi-py3
colocar em sudo vim /etc/apache2/envvars :
	export LANG='en_US.UTF-8'
	export LC_ALL='en_US.UTF-8'


#Instalação do wsgi
http://pythonclub.com.br/configurando-ambiente-django-com-apache-e-mod-wsgi.html




#copy the wsgi to tthe right location and set the wqual_SECRET_KEY ewqual_db_PASSWORD correctly
cp git/wiki-quality/wiki-quality-web/wiki_quality_web/wsgi.py wsgi/wqual.py



#criando o ambientevirtual
virtualenv ~/wqual-env -p /usr/bin/python3
#ativando o ambiente virtual
source wqual-env/bin/activate
#desativando ambiente virtual
deactivate


#copiar o arquivo ".conf" para a producao
sudo cp deploy/django_wqual.conf /etc/apache2/sites-available/.

#alterar o arquivo init para apontar para as configurações de produção
vim wiki-quality-web/wiki_quality_web/settings/__init__.py 
sudo service apache2 reload
wget http://webfeatures.com.br
tail /var/log/apache2/error.log
