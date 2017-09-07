##**Padrão de codificação**

###Models

* Para a nomenclatura das Features (Classes), cada filho deve deixar explícito no nome quem é seu pai e principalmente sua funcionalidade. Exemplo:

```python
	# Feature Pai: Word_Counter
	# Features Filhas: Word_Counter_Incorrects, Word_Counter_Corrects
```

* Para o nome das funções, adotar o padrão: `<tipo_de_retorno>_<lingua_utilizada_na_analise>_<funcionalidade>`. Exemplo:

```python
	# int_EN_Incorrect_Words, int_PT_Incorrect_Words
```

O padrão para a especificação dos Models, será:

```python
	class <nome_model> (<classes_de_heranca>):
	'''
		Classe <nome_model>: <funcao>
	'''
	{variaveis/atributos}

	#toString é obrigatório nas entidades. Usar o toString para a documentação
	def __str__(self):
		return <mensagem>
```
