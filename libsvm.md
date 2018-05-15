# Passo a passo SVM

## Para cada fold:

(Trocar i por número do fold)

### Rodar scale para o treino:

```
  libsvm$ ./svm-scale -s param.scale tools/Folds/TreinoFolds/treino.foldi.txt>treinoScaled.foldi
```

### Rodar scale para o teste:

```
  libsvm$ ./svm-scale -r param.scale tools/Folds/TesteFolds/teste.foldi.txt>testeScaled.foldi
```

### Rodar o grid_regression.py para descobrir o parametro custo e gama:

```
  libsvm/tools$ python grid_regression.py ../treinoScaled.foldi
```

### Usar o parametro custo e gama para o treino:

```
  libsvm$ ./svm-train -s 3 -c valor_custo -g valor_gama treinoScaled.foldi treino.modeloi
  libsvm$ ./svm-predict testeScaled.foldi treino.modeloi teste.predicti
```
