# Metadata Experiences

## Características

Este projeto é uma ferramenta de manipulação de metadados XML para arquivos de vídeo. Ele permite que você altere várias tags, incluindo `<poster>`, `<plot>`, `<language>`, `<episode>`, `<season>` e `<title>`.

## Compatibilidade

Este projeto foi idealizado para a plataforma Jellyfin. Embora possa funcionar com outras plataformas de mídia, não garantimos total compatibilidade ou suporte.

## Como usar

1. Clone o repositório para o seu computador local.
2. Navegue até o diretório do projeto no terminal.
3. Instale as dependências do projeto com o comando `pip install -r requirements.txt`.
4. Execute o script principal com o comando `python metadata.py`.

## Configuração do Ambiente Virtual

É recomendado criar um ambiente virtual para instalar as dependências do projeto. Isso pode evitar conflitos entre as dependências deste projeto e as de outros projetos no seu sistema.

### No Windows

1. Navegue até o diretório do projeto no terminal.
2. Crie o ambiente virtual com o comando `python -m venv venv`.
3. Ative o ambiente virtual com o comando `.\venv\Scripts\activate`.
4. Agora você pode instalar as dependências com o comando `pip install -r requirements.txt`.

### No Linux

1. Navegue até o diretório do projeto no terminal.
2. Crie o ambiente virtual com o comando `python3 -m venv venv`.
3. Ative o ambiente virtual com o comando `source venv/bin/activate`.
4. Agora você pode instalar as dependências com o comando `pip install -r requirements.txt`.

Ao executar o script, você será solicitado a inserir as informações necessárias para alterar as tags desejadas.

## Funções principais

- Alteração e adição de tags `<poster>` em arquivos XML.
- Alteração e adição de tags `<plot>` em arquivos XML.
- Alteração e adição de tags `<language>` em arquivos XML.
- Alteração e adição de tags `<episode>` em arquivos XML.
- Alteração e adição de tags `<season>` em arquivos XML.
- Alteração e adição de tags `<title>` em arquivos XML.

## Notas de atualização

### Versão 1.0.0

- Lançamento inicial do projeto.
- Suporte para manipulação das tags `<poster>`, `<plot>`, `<language>`, `<episode>`, `<season>` e `<title>`.

### Versão 1.1.0

- Adicionado suporte para repetir perguntas quando a entrada é inválida.
- Corrigido um bug onde a tag `<season>` não era adicionada corretamente.

### Versão 1.2.0

- Melhorias na interface do usuário.
- Corrigido um bug onde a tag `<plot>` não era alterada corretamente.

### Versão 1.3.0

- Adicionado suporte para mais tipos de arquivos de vídeo.
- Melhorias na performance do script.

## Contribuindo

Se você deseja contribuir para este projeto, por favor, faça um fork do repositório e submeta um pull request.

## Licença

Este projeto está licenciado sob a licença MIT.

## Copyright

Copyright 2024 Rutileno Gabriel.