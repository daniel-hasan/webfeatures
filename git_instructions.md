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

## Início de uma nova Sprint
- Para cada Sprint, a partir do branch master, crie um novo branch chamado `feat-usuario-NUM` sendo que `NUM` é o número da sprint.
Veja o exemplo em que o usuário é `daniel-hasan` e estamos na Sprint `5`:
```bash
git checkout master
git branch feat-daniel-hasan-5
```
- Entre no branch no seu repositório local para poder começar a fazer as alterações desejadas:
```bash
git checkout feat-daniel-hasan-5
```

## Enviando e obtendo alterações em seu branch

- **Enviando alterações:** Para enviar as alterações para o repositório remoto (ainda em seu branch) utilize:
```bash
git add -A
git commit -m "Alterações blah feita hoje"
git push origin feat-daniel-hasan-5
```

- Recomendável fazer isso constantemente. Pois isto irá fazer backup de suas alterações. Isto também é útil quando trabalhamos em mais de um computador e queremos passar as alterações de um computador para outro.
- Além disso, assim que você enviar suas alterações pelo repositório remoto, serão realizados testes para verificar se o seu código não criou nenhum tipo de erro em seu branch. Para verificar  tais testes, acesse o nosso repositório no bitbucket, vá em `pipelines` e acesse o seu branch.

- **Obtendo alterações:** Algumas vezes, alterações em seu branch não existem em seu repositório local. Pois, você
pode ter alterado em outro computador ou alguém, que estava ajudando nesta funcionalidade,
atualizou o repositório remoto. Assim, você deverá executar o comando `pull` para obter tais alterações:

```bash
  git pull origin feat-daniel-hasan-5
```

## Obtendo atualização do Branch Master em seu Branch
- Obtenha frequentemente as atualizações do branch `master`. Assim,
menos erros ocorrerão quando for fazer o merge **para o** branch `master`. Para isso, vá em seu branch e solicite um branch **do** master **para o** seu branch:
```bash
git checkout feat-daniel-hasan-5
git merge master
```
  - Caso haja conflito, corrija-os. Veja a seção que fala sobre [solução de conflitos](#markdown-header-solucao-de-conflitos)


## Finalizando funcionalidade - Enviando-as ao branch Master

- Antes de começar, [obtenha as atualizações do branch master](#markdown-header-obtendo-atualizacao-do-branch-master-em-seu-branch)
- Ainda em seu branch, caso tenha alterações no repositório local que não estão no repositório remoto, [envie tais alterações](#markdown-header-enviando-e-obtendo-alteracoes-em-seu-branch):
    - Você pode executar `git status` para ver se há alguma alteração no seu repositório local que ainda não foi enviada ao respositório remoto

- Acesse usando [repositório wikiquality no bitbucket](https://bitbucket.org/daniel-hasan/wiki-quality) por meio de seu login e senha.
- Acesse o menu `Pipelines` clique em seu branch e veja se
o repositório foi construído com sucesso
  - Caso haja erros na construção do repositório, veja o erro o que ocorreu, corrija-o e envie as alterações

- Após corrigir todos os erros, no menu, acesse `Pull Request` e clique em `create pull request`.

  - Faça um `Pull Request` do seu branch para o master. O administrador receberá um email para aprovar as alterações
  feitas e fazer o merge no master.

  - Caso, ao solicitar o Pull Request, haja algum arquivo com conflito (haverá um "c" no nome do arquivo), não será possível fazer o merge. Assim, você deve solicionar os conflitos para isso, [obtenha as atualizações do branch master - veja a seção anterior](#markdown-header-obtendo-atualizacao-do-branch-master-em-seu-branch) e, logo após, solucione os conflitos.

## Solução de conflitos

Existem algumas ferramentas visuais para solução de conflitos. Aqui, explicarei a instalação da `Meld`. Primeiramente, instale a ferramenta:
```bash
sudo apt-get install meld
```

Voce pode deixar ele como default ao dar merge: 
```bash
git config --global merge.tool meld
```
Logo após de verificar um conflito (por exemplo, fazendo um merge do master para seu branch) abra a interface do meld. 
Para execurar o meld, digite "meld" e  clique em "Version control view" e selecione a pasta raiz de nosso repositório. 
Logo após, clique nos arquivos com status "conflict" para fazer as alterações necessárias

De um lado estará o repositorio local e , do outro, o repositório remoto (veja o titulo acima do código) e, no meio, o arquivo a ser editado (com o conflito). Assim, você poderá fazer merge das edições locais (suas) e edições remotas (de outras pessoas) para o código que está no meio.
Salve as alterações.