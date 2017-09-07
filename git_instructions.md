# Utilização do GIT

## Criação de nova funcionalidade
- Para cada funcionalidade, crie um novo branch chamado `feat-usuario-NUM` sendo que `NUM` é o número da funcionalidade (use o número da tarefa REDMINE) e usuário é o nome do usuário no git. Note que a abreviatura `feat` vem de
feature, ou seja, uma funcionalidade no software.
Veja o exemplo em que o usuário é `daniel-hasan` e o código da funcionalidade é `123`:
```bash
git branch feat-daniel-hasan-123
```
- Entre no branch no seu repositório local para poder começar a fazer as alterações desejadas:
```bash
git checkout feat-daniel-hasan-123
```

## Fazendo/obtendo alterações em seu branch

- **Fazendo alterações:** Para enviar as alterações para o repositório remoto (ainda em seu branch) utilize:
```bash
git add -A
git commit -m "Alterações blah feita hoje"
git push origin feat-daniel-hasan-123
```
  - Recomendável fazer isso constantemente. Pois isto irá fazer backup de suas alterações.
  Isto também é útil quando trabalhamos em mais de um computador e queremos passar as alterações de
  um computador para outro.

- **Obtendo alterações:** Algumas vezes, alterações em seu branch não existem em seu repositório local. Pois, você
pode ter alterado em outro computador ou alguém, que estava ajudando nesta funcionalidade,
atualizou o repositório remoto. Assim, você deverá executar o comando `pull` para obter tais alterações:

```bash
  git pull origin feat-daniel-hasan-123
```

## Obtendo atualização do Branch Master
- Obtenha frequentemente as atualizações do branch `master`. Assim,
menos erros ocorrerão quando for fazer o merge com o branch `master`. Para isso,
execute em seu branch:
```bash
git rebase master
```
  - Corrija os conflitos que podem ocorrer e faça os testes unitários para verificar se o seu código ainda funciona.


## Finalizando funcionalidade - Enviando-as ao branch Master

- Antes de começar, obtenha as atualizações do branch master [veja na seção anterior](#obtendo-atualização-do-branch-master)
- Envie suas alterações ao branch master (caso tenha dado `rebase`, isso pode ter gerado também alterações que devem ser enviadas ao respositório remoto):
  - Ainda em seu branch, envie suas últimas alterações, caso não tenha feito:

  ```bash
  git add -A
  git commit -m "Alterações blah feita hoje"
  git push origin feat-daniel-hasan-123
  ```
  - Acesse usando seu login e senha  [repositório wikiquality no bitbucket](https://bitbucket.org/daniel-hasan/wiki-quality).
  No menu acesse `Pull Request` e clique em `create pull request`.

  - Faça um `Pull Request` do seu branch para o master. O administrador receberá um email para aprovar as alterações
  feitas e fazer o merge no master.
    - Ao solicitar um pull request, pode ser 



<!--
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
-->
