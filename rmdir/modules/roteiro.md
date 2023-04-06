# Roteiro de criação para o programa

## Objetivo
O programa irá receber entradas de um arquivo de configuração, depois com base nesses dados irá excluir todos os diretórios dentro de uma pasta compartilhada na rede e irá criar novos diretórios com base numa lista contendo os nomes de todos os usuários de um domínio. Um arquivo de log deverá ser gerado contendo toda a execução do programa.

## Passos

1. Comece lendo o arquivo de configuração para obter as informações necessárias, como o caminho da pasta compartilhada e o nome do domínio.

2. Use o módulo `os` do Python para listar todos os diretórios dentro da pasta compartilhada. Em seguida, use um loop para excluir cada diretório.

3. Use o módulo `win32com.client` do Python para acessar o Active Directory e obter a lista de todos os usuários do domínio.

4. Para cada usuário, use o módulo `os` para criar um novo diretório dentro da pasta compartilhada com o nome do usuário.

5. Use o módulo `logging` do Python para registrar todas as ações do programa em um arquivo de log. Certifique-se de incluir informações importantes, como quais diretórios foram excluídos e quais novos diretórios foram criados.

6. Teste o programa para garantir que ele funcione corretamente e que os diretórios sejam criados corretamente.

7. Faça qualquer ajuste necessário para melhorar o desempenho ou a funcionalidade do programa.

8. Documente bem o código para que outros usuários possam entender e manter o programa no futuro.

9. Empacote o programa em um arquivo executável ou script e distribua-o para os usuários finais.
