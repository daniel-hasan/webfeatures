##**Padrão de codificação**

###Templates

Nos templates, adotaremos o método de herança de templates. 

Informações mais consistentes sobre o método podem ser encontradas [aqui](https://docs.djangoproject.com/en/1.7/topics/templates/).

Observações importantes:

* Quantidade de níveis de herança que serão utilizados;

* Quantidade de templates necessários.

Segue sugestão para a modelagem dos arquivos:

####_Arquivo bootstrap.html_

```python
	{% extends 'bootstrap3/bootstrap3.html' %}

	{% load bootstrap3 %}

	0{% block bootstrap3_title %}{% block title %}{% endblock %}{% endblock %}
```

####_Arquivo base.html_

```python
	<!--
			estende a base que contem o menu
	-->
	{% extends 'bootstrap.html' %}

	<!--
			inicia bloco de conteudo bootstrap
	-->
	{% block bootstrap3_content %}
	{% endblock %}

	<div class="container">
		{% block main %}
		{% endblock %}
	</div>
```

####_Outros arquivos_

```python
	<!--
		pode estender quantas bases forem necessárias
	-->
	{% extends 'base.html' %}
	{% block title %}
		Title
	{% endblock %}

	{% block main %}
	{% endblock %}
```
