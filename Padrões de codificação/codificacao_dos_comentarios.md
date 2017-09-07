##**Padrão de codificação**

###Comentários

O padrão a ser adotado para a escrita de comentários será:

####_Headers_

Arquivos `<*.py>`

```python
	Versão: <*.0> - [final]
	Data de modificação: <dia>/<mes>/<ano>
	Autor(<primeira versão>): <nome><sobrenome>
          AutorM(<ultima versão>): <nome><sobrenome>

	Arquivo: <nome_arq>
          Objetivo: {objetivos}
```

Arquivos `<*.html>`

```python
 <!--
	Versão: <*.0> - [final]
	Data de modificação: <dia>/<mes>/<ano>
	Autor(<primeira versão>): <nome><sobrenome>
          AutorM(<ultima versão>): <nome><sobrenome>

	Arquivo: <nome_arq>
          Objetivo: {objetivos}
 -->
```

####_Blocos de código_

Observações:

* Evitar escrever comentários à frente dos comandos, exemplo:

```python
	Conta_lista_de_contas = Conta.objects.all() #Recupera a lista de contas do banco de dados
```

* Dar preferência para a escrita de comentários acima do conjunto de comandos desejados, exemplo:

```python
	# Recupera a lista de contas do banco de dados
	Conta_lista_de_contas = Conta.objects.all()
```

* Quando se usar uma função de uma biblioteca Python pouco comum, colocar um comentário especificando sua funcionalidade.

####_Métodos, funções, views, ..._

Adotaremos o seguinte padrão para a especificação de comentários para este tipo de bloco.

São exemplos desse tipo de comentário:

```python
	<comentário sobre a funcionalidade>
	@autor <nome_autor>
	@data_criacao <dia>/<mes>/<ano>
	@{params} : <nome_param> #<especificacao_param>
	[@return][<mensagem_retorno>]
```

Os comentários devem ser colocado logo após o protótipo, respeitando a possibilidade de chamada da documentação pelo próprio interpretador do Python.

Comentários complementares para organização:

```python
	#Importacoes

	#Area de criacao de ******
```




