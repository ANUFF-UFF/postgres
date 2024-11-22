# Scripts de criação do banco

Para executar é necessário possuir docker instalado na máquina

Pode ser necessário executar com acesso `root`:

    $ sudo ./build.sh

Ao executar pedirá para definir a senha do usuário admin.

Essa senha também pode ser definida na chamada do comando. Ex.:

    $ sudo ./build.sh Minha_Senha123#

A instancia gerada terá um banco `anuff`, com usuário de acesso `admin`, podendo ser acessada com o comando:

    $ psql -h <endereço_da_instancia> -U admin anuff

Que pedirá a senha definida anteriormente

    Password for user admin:

