# Scripts de criação do banco

Para executar é necessário possuir docker instalado na máquina

Pode ser necessário executar com acesso `root`

O arquivo deve ser chamado com source:

    $ source ./run.sh

ou:

    $ . ./run.sh

Ao executar pedirá para definir as variaveis de ambiente necessárias para definir usuario, senha, etc, caso não exista no arquivo `./set_env`.

Se esse arquivo já exisitir essa etapa será pulada.

A instancia gerada pode ser acessada com o comando:

    $ psql -h <endereço_da_instancia> -U <usuario> <nome_do_banco_de_dados>

Que também pedirá a senha salva no arquivo `./set_env`

# Tipos de Commits e Branches

**test**: indica qualquer tipo de criação ou alteração de códigos de teste. Exemplo: Criação de testes unitários.

**feat**: indica o desenvolvimento de uma nova feature ao projeto. Exemplo: Acréscimo de um serviço, funcionalidade, endpoint, etc.

**refactor**: usado quando houver uma refatoração de código que não tenha qualquer tipo de impacto na lógica/regras de negócio do sistema. 
Exemplo: Mudanças de código após um code review

**style**: empregado quando há mudanças de formatação e estilo do código que não alteram o sistema de nenhuma forma.
Exemplo: Mudar o style-guide, mudar de convenção lint, arrumar indentações, remover espaços em brancos, remover comentários, etc..

**fix**: utilizado quando há correção de erros que estão gerando bugs no sistema.
Exemplo: Aplicar tratativa para uma função que não está tendo o comportamento esperado e retornando erro.

**chore**: indica mudanças no projeto que não afetem o sistema ou arquivos de testes. São mudanças de desenvolvimento.
Exemplo: Mudar regras do eslint, adicionar prettier, adicionar mais extensões de arquivos ao .gitignore

**docs**: usado quando há mudanças na documentação do projeto.
Exemplo: adicionar informações na documentação da API, mudar o README, etc.

**build**: utilizada para indicar mudanças que afetam o processo de build do projeto ou dependências externas.
Exemplo: Gulp, adicionar/remover dependências do npm, etc.

**perf**: indica uma alteração que melhorou a performance do sistema.
Exemplo: alterar ForEach por while, melhorar a query ao banco, etc.

**ci**: utilizada para mudanças nos arquivos de configuração de CI.
Exemplo: Circle, Travis, BrowserStack, etc.

**revert**: indica a reverão de um commit anterior.

# Padrões dos Nomes de Commits e Branches

**Commits:** `"tipo: fazer algo; fazer outras coisas; ..."`

Exemplo: `feat: adicionar botão; estilizar input`

**Branches:** `"tipo/descricao-da-tarefa"`

Exemplo: `fix/consertar-bug-de-cadastro-de-usuarios` (A Descrição normalmente é o nome do card)
