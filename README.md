# EasyGest PDV

<p align="left">
  <img src="https://img.shields.io/badge/Python-3-blue?logo=python&logoColor=white" alt="Python 3">
  <img src="https://img.shields.io/badge/Interface-Tkinter-3776AB" alt="Tkinter">
  <img src="https://img.shields.io/badge/Database-MongoDB-47A248?logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/ORM-PyMongo-47A248" alt="PyMongo">
</p>

> Aplicação desktop para gestão comercial e operação de ponto de venda, desenvolvida em Python, com interface Tkinter e persistência em MongoDB.

## Sumário

- [Introdução](#introdução)
- [Objetivos e problema resolvido](#objetivos-e-problema-resolvido)
- [Principais funcionalidades](#principais-funcionalidades)
- [Fundamentação teórica: Programação Orientada a Objetos](#fundamentação-teórica-programação-orientada-a-objetos)
- [Tecnologias e desenvolvimento](#tecnologias-e-desenvolvimento)
- [Organização do código](#organização-do-código)
- [Banco de dados](#banco-de-dados)
- [Segurança](#segurança)
- [Regras de negócio](#regras-de-negócio)
- [Instalação e execução](#instalação-e-execução)
- [Empacotamento para Windows](#empacotamento-para-windows)
- [Testes](#testes)

## Introdução

O **EasyGest PDV** é um sistema de ponto de venda voltado ao controle diário das operações comerciais de pequenos estabelecimentos. O software integra cadastro de produtos, controle de estoque, registro de vendas, abertura e fechamento de caixa, sangrias, usuários e indicadores em uma única aplicação desktop.

A aplicação foi desenvolvida com uma interface gráfica intuitiva em Tkinter e utiliza MongoDB para armazenar entidades e históricos. Os dados são organizados em coleções consultadas por meio do PyMongo.

## Objetivos e problema resolvido

O objetivo do EasyGest PDV é reduzir erros e a dependência de processos manuais em tarefas comuns de venda e administração. O sistema busca centralizar informações e garantir que operações como baixa de estoque, cálculo do caixa e registro de pagamentos sejam realizadas de maneira padronizada.

Principais problemas e necessidades atendidas:

- cadastro e atualização descentralizada de produtos;
- falta de controle sobre entradas e saídas de estoque;
- dificuldade de registrar vendas por forma de pagamento;
- risco de divergências no saldo e fechamento do caixa;
- necessidade de separar as permissões de administradores e operadores;
- ausência de histórico para consultas posteriores;
- necessidade de uma solução desktop simples de instalar e utilizar no Windows.

## Principais funcionalidades

- autenticação de usuários ativos;
- perfis **ADMIN** e **OPERADOR**;
- cadastro, consulta, atualização e desativação de produtos;
- controle de entradas e saídas de estoque;
- alerta de estoque igual ou abaixo do mínimo;
- frente de caixa com carrinho de produtos;
- pagamentos em dinheiro, cartão e PIX;
- cálculo de troco e parcelamento;
- abertura e fechamento de caixa;
- sangrias com justificativa e confirmação por senha;
- histórico de vendas, caixas e sangrias;
- painel com indicadores comerciais e filtros por período.

## Fundamentação teórica: Programação Orientada a Objetos

A aplicação foi estruturada em classes que representam entidades do domínio comercial e comportamentos relacionados às operações do sistema.

### Classe e objeto

Uma **classe** é o modelo que define atributos e métodos, enquanto um **objeto** é uma instância dessa classe em execução. Por exemplo, a classe `Produto` define nome, descrição, preço, custo e situação, enquanto cada objeto criado representa um produto cadastrado no sistema.

Exemplos utilizados no projeto:

- `Usuario` representa uma conta;
- `Produto` representa um item comercializado;
- `Estoque` representa a quantidade disponível de um produto;
- `Venda` representa uma operação de venda;
- `Caixa` representa um turno de atendimento.

### Atributos

Os atributos armazenam o estado dos objetos. Em `Produto`, por exemplo, existem atributos como `nome`, `codigo_barras`, `preco_venda`, `custo` e `ativo`. Em `Usuario`, atributos como `usuario`, `perfil`, `ativo` e `senha_hash` guardam os dados necessários à autenticação e às permissões.

### Métodos

Os métodos representam ações executadas pelos objetos. A classe `Venda` possui métodos como `adicionar_item`, `calcular_total`, `finalizar` e `cancelar`. A classe `Estoque` utiliza `adicionar_quantidade`, `retirar_quantidade` e `verificar_estoque_baixo` para implementar regras de quantidade.

### Herança

A herança permite que uma classe reutilize características de outra classe. No módulo de pagamentos, `Pagamento` é uma classe abstrata base e `Dinheiro`, `Cartao` e `PIX` herdam dela:

```text
Pagamento
├── Dinheiro
├── Cartao
└── PIX
```

As classes derivadas reutilizam atributos e comportamentos comuns, como `valor_total` e `consultar_status`, por meio de `super()`.

### Abstração

A abstração simplifica o problema ao expor comportamentos essenciais e ocultar detalhes desnecessários. `Pagamento` é uma classe abstrata criada com `ABC` e `abstractmethod`; ela representa a ideia geral de um pagamento, mas exige que uma classe concreta implemente o método `processar`.

Assim, o sistema pode trabalhar com objetos de pagamento de forma geral, enquanto cada forma implementa a própria confirmação.

### Encapsulamento

O encapsulamento organiza dados e comportamentos dentro das classes e controla o acesso a alterações por meio de métodos. Em vez de modificar diretamente o estado da venda ou do estoque em qualquer parte do código, a aplicação utiliza métodos como `adicionar_item`, `finalizar`, `adicionar_quantidade` e `retirar_quantidade`.

Esses métodos também validam valores antes de alterar o estado do objeto. Por exemplo, não é permitido retirar uma quantidade maior que a disponível ou finalizar uma venda sem itens.

### Polimorfismo

O polimorfismo permite que objetos de classes diferentes respondam ao mesmo comportamento de maneiras próprias. Todas as formas de pagamento possuem o método `processar`, mas a implementação é específica de cada tipo:

- `Dinheiro.processar` aprova o pagamento após conferir o valor recebido;
- `Cartao.processar` simula a aprovação e registra as parcelas;
- `PIX.processar` simula a confirmação e utiliza um identificador de transação.

O método `to_document` também é sobrescrito pelas classes derivadas para incluir os dados particulares de cada forma de pagamento.

## Tecnologias e desenvolvimento

| Tecnologia | Finalidade no projeto |
|---|---|
| Python 3 | Linguagem principal e implementação das regras de negócio |
| Tkinter / `ttk` | Interface gráfica desktop, widgets, formulários e tabelas |
| MongoDB / MongoDB Atlas | Persistência orientada a documentos |
| PyMongo | Conexão, consultas e operações sobre coleções |
| python-dotenv | Carregamento da variável `MONGO_URI` |
| bcrypt | Geração e validação de hashes de senha |
| PyInstaller | Empacotamento da aplicação Windows |

Tkinter normalmente acompanha a instalação padrão do Python no Windows. Caso o módulo não esteja disponível, confirme se o componente Tcl/Tk foi instalado.

O projeto não utiliza um framework MVC formal, mas separa responsabilidades:

- `models/` concentra entidades e regras do domínio;
- `services/` reúne operações reutilizáveis;
- `telas/` implementa a interface gráfica;
- `conexao.py` cria e encerra a conexão;
- `main.py` inicia a aplicação;
- `assets/` contém recursos visuais.

## Organização do código

```text
EasyGest_PDV/
├── main.py                 # Inicialização da aplicação
├── conexao.py              # Conexão com MongoDB
├── models/                 # Classes de domínio
│   ├── usuario.py
│   ├── produto.py
│   ├── estoque.py
│   ├── venda.py
│   ├── item_venda.py
│   ├── caixa.py
│   └── pagamento.py        # Classe base abstrata
├── services/
│   └── usuario_service.py  # Cadastro e autenticação
├── telas/                  # Telas Tkinter
├── assets/
│   └── easygest.ico
├── EasyGestPDV.spec        # Configuração do PyInstaller
├── teste_usuario.py
└── teste_usuario_service.py
```

A interface utiliza janelas `Tk` e `Toplevel`. As telas se comunicam com os modelos, os serviços e as coleções do banco, enquanto `main.py` gerencia o ciclo de vida da janela principal.

## Banco de dados

O banco utilizado é o **`EasyGest_PDV`**. A conexão pode ser configurada para uma instância MongoDB local ou MongoDB Atlas por meio da variável `MONGO_URI`. A aplicação executa um comando `ping` antes de disponibilizar o sistema.

### Coleções principais

| Coleção | Dados principais | Observação |
|---|---|---|
| `usuarios` | `nome`, `usuario`, `senha_hash`, `perfil`, `ativo` | Contas locais do sistema |
| `produtos` | `nome`, `descricao`, `codigo_barras`, `preco_venda`, `custo`, `ativo` | Produtos desativados são mantidos |
| `estoques` | `produto_id`, `quantidade`, `quantidade_minima` | Referência ao produto |
| `caixas` | saldos, totais por pagamento, vendas, sangrias, status e datas | Operação de turno |
| `vendas` | `caixa_id`, `data`, `itens`, `valor_total`, `status` | Os itens são armazenados como documentos embutidos |
| `pagamentos` | `venda_id`, `tipo`, `valor`, `status` e dados da forma | Referência à venda |

Os relacionamentos são implementados principalmente por `ObjectId`. Os itens da venda e as sangrias podem ser embutidos no documento da operação para preservar o histórico.

Os formatos são definidos pelas classes e métodos `to_document`; o projeto não declara migrações ou validadores de esquema no MongoDB. Os valores monetários são manipulados pela aplicação como `float` e arredondados para duas casas decimais.

## Segurança

1. Configure a variável de ambiente `MONGO_URI` ou copie `.env.example` para `.env` e preencha a URI do seu ambiente.
2. Para MongoDB Atlas, utilize a string de conexão fornecida pelo cluster.
3. Não utilize credenciais reais em arquivos versionados.
4. Não compartilhe ou adicione o arquivo `.env` ao repositório.
5. Configure no MongoDB Atlas usuário específico, permissões mínimas, rede autorizada e conexão TLS.
6. O caractere especial em usuário ou senha da URI deve ser codificado conforme as regras de URI do MongoDB.

As principais medidas implementadas na aplicação são:

- senhas armazenadas como hash bcrypt;
- usuário precisa estar ativo para autenticar;
- perfis `ADMIN` e `OPERADOR`;
- gerenciamento de usuários limitado à interface administrativa;
- confirmação adicional por senha em sangrias e fechamentos;
- impedimento da desativação da própria conta;
- impedimento da desativação do último administrador ativo.

O controle da interface não substitui a segurança da infraestrutura. A política de usuários e rede deve ser configurada diretamente no MongoDB.

## Regras de negócio

### Produtos e estoque

- preço de venda deve ser maior que zero;
- custo não pode ser negativo;
- a exclusão pela interface é lógica: o produto é desativado;
- entradas e saídas requerem quantidade inteira positiva;
- uma saída não pode exceder o estoque disponível;
- estoque baixo ocorre quando `quantidade <= quantidade_minima`;
- produtos inativos não são oferecidos em vendas.

### Vendas e pagamentos

- uma venda precisa possuir pelo menos um item;
- cada item deve ter quantidade positiva;
- o estoque precisa ser suficiente;
- o total é a soma dos subtotais;
- **dinheiro** exige valor recebido suficiente e calcula o troco;
- **cartão** aceita de uma a doze parcelas;
- **PIX** utiliza um identificador de transação;
- cartões e PIX são simulados neste projeto e não fazem integração bancária real.

Ao finalizar uma venda, a aplicação utiliza uma transação MongoDB para vincular a venda ao caixa aberto, atualizar o estoque, registrar venda e pagamento e recalcular os totais. Todas as alterações devem ser confirmadas ou revertidas caso alguma etapa falhe.

### Caixa

- a abertura exige saldo inicial maior ou igual a zero;
- não pode haver mais de um caixa `ABERTO`;
- o saldo físico é calculado por:

  ```text
  saldo inicial + vendas em dinheiro - sangrias
  ```

- valores em cartão e PIX não integram o saldo físico em dinheiro;
- a sangria exige valor positivo, justificativa e saldo suficiente;
- o fechamento exige confirmação e nova autenticação;
- o fechamento registra o usuário responsável e fecha o caixa.

Os históricos permitem consultar caixas, vendas e sangrias realizadas.

## Instalação e execução

### Pré-requisitos

- Python 3 com suporte a Tkinter;
- MongoDB local ou MongoDB Atlas;
- URI de conexão configurada em `MONGO_URI`;
- sistema operacional Windows recomendado para a configuração atual.

### Configuração no Windows

Na pasta do projeto, abra o PowerShell e execute:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pymongo python-dotenv bcrypt
```

Copie o modelo de configuração e edite a URI com os dados do seu cluster:

```powershell
Copy-Item .env.example .env
```

O `.env.example` contém apenas valores fictícios. Não versione nem distribua o arquivo `.env` preenchido.

Em seguida, execute:

```powershell
python main.py
```

O sistema verifica a conexão antes de abrir a tela de login. O banco selecionado pelo código é `EasyGest_PDV`.

### Primeiro administrador

`main.py` não cria automaticamente o primeiro usuário. O arquivo `teste_usuario_service.py` oferece um fluxo interativo para cadastrar o primeiro administrador, autenticar e listar usuários.

```powershell
python teste_usuario_service.py
```

Execute esse script apenas em ambiente de desenvolvimento ou dados de teste, pois ele pode alterar o banco configurado.

## Empacotamento para Windows

O arquivo `EasyGestPDV.spec` contém a configuração do PyInstaller, incluindo o ícone e as dependências necessárias.

```powershell
python -m pip install pyinstaller
python -m PyInstaller EasyGestPDV.spec
```

O executável e os arquivos distribuíveis são gerados nas pastas de saída do PyInstaller. O arquivo `.env` não faz parte do arquivo `.spec`; configure `MONGO_URI` no ambiente de destino ou use um `.env` local não distribuído junto ao executável.

## Testes

Os arquivos `teste_usuario.py` e `teste_usuario_service.py` são scripts de apoio para o modelo e o serviço de usuário. O projeto não possui, atualmente, uma suíte automatizada abrangente nem um `requirements.txt` versionado.

As dependências podem ser registradas em um arquivo de requisitos futuro para facilitar a instalação reproduzível:

```text
pymongo
python-dotenv
bcrypt
pyinstaller
```
# EasyGestPDV
# EasyGestPDV
# EasyGestPDV
