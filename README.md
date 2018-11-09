- [Como contribuir?](CONTRIBUTING.md)
- [Instruções GIT](git_instructions.md)
- [Passo a passo SVM](libsvm.md)

Por meio da internet, um novo tipo de repositório do conhecimento humano está sendo criado. Nele, o usuário não é apenas consumidor, mas também produtor de conteúdo. Tal liberdade, porém, traz consigo uma importante questão: como o usuário pode determinar a qualidade da informação que acessa? Comunidades colaborativas já possuem técnicas manuais para tratar o problema de qualidade dos documentos levando em conta o julgamento humano. Entretanto, tais técnicas manuais enfrentam problemas de escalabilidade devido ao tamanho dessas coleções e a velocidade com que ela se expande. Dessa forma, **o presente projeto visa implementar uma plataforma Web para extração de indicadores de qualidade textuais em documentos colaborativos**.

Nossa hipótese é que tais indicadores irão auxiliar na  tarefa de avaliação de qualidade de conteúdo colaborativo, uma vez que tais indicadores poderiam oferecer subsídios para definir quais documentos deveriam ser revisados, o que revisar, detectar processos de revisão inadequados, tais como vandalismos, ou recomendar diretamente o material aos usuários baseado nos seus indícios de qualidade e confiabilidade. Logo após, será realizado também uma caracterização para entender como essa plataforma e seus indicadores podem auxiliar em um determinado domínio, como na Wikipédia. Pretende-se que essa plataforma esteja disponível on-line, com o objetivo de auxiliar a comunidade externa e pesquisadores que poderão extrair indicadores de qualidade para textos de documentos colaborativos para seu uso em pesquisas.


O tema do trabalho será livre e deverá possuir, obrigatoriamente os seguintes elementos: 


- Um CRUD (Funcionalidades de adicionar/remover/atualizar e recuperar) usando [Generic Views]() para [listar](https://docs.djangoproject.com/pt-br/2.1/topics/class-based-views/generic-display/#making-friendly-template-contexts) e [inserir/remover/atualizar](https://docs.djangoproject.com/pt-br/2.1/ref/class-based-views/generic-editing/) os elementos
- Alguma operação (consulta, inserção, atualização ou remoção) usando Ajax
- Autenticação e a tela dos CRUDs só podem ser usadas se autenticado
- Uso de [cache](https://docs.djangoproject.com/en/2.1/topics/cache/) para [alguma view](https://docs.djangoproject.com/en/2.1/topics/cache/#the-per-view-cache) e para [algum template](https://docs.djangoproject.com/en/2.1/topics/cache/#template-fragment-caching)
- Uma das telas devem ser testadas usando [um teste unitário Django apropriado](https://docs.djangoproject.com/pt-br/2.1/topics/testing/overview/). O teste deverá efetuar operação de consulta, inserção, remoção e atualização dos elementos [simulando a requisição](https://docs.djangoproject.com/pt-br/2.1/topics/testing/tools/).

Você deverá [criar um ambiente virtual e gerar o arquivo requirements.txt](https://docs.python.org/3/tutorial/venv.html) com todas as dependencias do projeto. Use o Bitbucket para criar um repositório, e [use pipeline](https://confluence.atlassian.com/bitbucket/build-test-and-deploy-with-pipelines-792496469.html) testando por meio do teste unitário criado. Assim, sempre que alguém de commit na aplicação, os testes serão executados e vocês serão informados se, depois de algum commit, sua aplicação parou de funcionar <3. 

Crie um repositório público no bitbucket. Entregue o link deste repositório. Crie um readme.md com (a) os integrantes do grupo (máximo 3); (b) instruções para implantação do sistema para o prof poder executá-lo.