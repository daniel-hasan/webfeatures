# Utilização do GIT

Comandos mais usados:

- `git status`: verifica o estado dos arquivos em seu repositório local
- `git add -A`: adiciona os arquivos em seu repositório local
- `git commit -m "mensagem"`: faz commit de seus arquivos para o repositório local
- `git push origin nome-da-branch`: envia os arquivos para o respositório remoto na branch chamada `nome-da-branch`
- `git pull origin nome-da-branch`: obtém os arquivos do repositório remoto
- `git branch`: exibe as branches existentes e mostra em qual branch você está atualmente trabalhando
- `git branch nome-da-branch`: cria uma nova branch
- `git checkout nome-da-branch`: vai para uma determinada branch

## Criação de nova funcionalidade
- Para cada funcionalidade, a partir do branch master, crie um novo branch chamado `feat-usuario-NUM` sendo que `NUM` é o número da funcionalidade (use o número da tarefa REDMINE) e usuário é o nome do usuário no git. Note que a abreviatura `feat` vem de
feature, ou seja, uma funcionalidade no software.
Veja o exemplo em que o usuário é `daniel-hasan` e o código da funcionalidade é `123`:
```bash
git checkout master
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
- Recomendável fazer isso constantemente. Pois isto irá fazer backup de suas alterações. Isto também é útil quando trabalhamos em mais de um computador e queremos passar as alterações de um computador para outro.
- Além disso, assim que você enviar suas alterações pelo repositório remoto, serão realizados testes para verificar se o seu código não criou nenhum tipo de erro em seu branch. Para verificar  tais testes, acesse o nosso repositório no bitbucket, vá em `pipelines` e acesse o seu branch.

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
- Ainda em seu branch, caso tenha alterações no repositório local que não estão no repositório remoto, envie tais alterações (caso tenha dado `rebase`, isso pode ter gerado também alterações que devem ser enviadas ao respositório remoto):
  ```bash
  git add -A
  git commit -m "Alterações blah feita hoje"
  git push origin feat-daniel-hasan-123
  ```
    - Você pode executar `git status` para ver se há alguma alteração no seu repositório local que ainda não foi enviada ao respositório remoto

- Acesse usando [repositório wikiquality no bitbucket](https://bitbucket.org/daniel-hasan/wiki-quality) por meio de seu login e senha.
- Acesse o menu `Pipelines` clique em seu branch e veja se
o repositório foi construído com sucesso
  - Caso haja erros na construção do repositório, veja o erro o que ocorreu, corrija-o e envie as alterações

- Após corrigir todos os erros, no menu, acesse `Pull Request` e clique em `create pull request`.

  - Faça um `Pull Request` do seu branch para o master. O administrador receberá um email para aprovar as alterações
  feitas e fazer o merge no master.
