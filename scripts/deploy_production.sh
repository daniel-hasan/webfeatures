sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git python3 
sudo apt-get install python-pip3
sudo apt-get install mysql-server
sudo apt-get install make
sudo mysql_secure_instalation
#instalacao do mysql
==Codigo no mysql (ao começão)
CREATE USER 'wiki_quality'@'127.0.0.1' IDENTIFIED BY '_S@no=38$238ch';
GRANT ALL ON wiki_quality.* TO 'wiki_quality'@'127.0.0.1';


==Codigo do mysql - apos instalação) 
REVOKE CREATE DROP on wikiquality.* to 'wiki_quality'@'127.0.0.1';

#Instalação do wsgi
http://pythonclub.com.br/configurando-ambiente-django-com-apache-e-mod-wsgi.htmlsudo 

ln -s ../sites-available/wsgi_test wsgi_test


