# Student's Hell

Jogo Arcade 2D desenvolvido em **Python + Pygame** como projeto da disciplina de Computação Gráfica.

O projeto foi desenvolvido com foco na implementação própria dos principais algoritmos de Computação Gráfica apresentados durante a disciplina, incluindo rasterização, preenchimento de regiões, transformações geométricas, janela e viewport, clipping e mapeamento de texturas.

---

## Sobre o jogo

**Student's Hell** é um jogo arcade 2D no qual o jogador controla um personagem/nave dentro de uma arena, enfrentando inimigos e utilizando projéteis para sobreviver e completar o desafio.

O jogo utiliza gráficos construídos a partir de primitivas geométricas e algoritmos de rasterização implementados no próprio projeto.

Além da área principal de jogo, o projeto possui uma **viewport com zoom acompanhando o jogador**, permitindo visualizar uma região ampliada da arena.

---

## Principais características

* Jogo Arcade 2D;
* Controle do jogador por teclado;
* Sistema de inimigos;
* Sistema de projéteis;
* Projéteis com diferentes comportamentos;
* Colisões entre entidades;
* Animações durante a execução;
* Menu e interação com o usuário;
* Background utilizando mapeamento de textura;
* Sprites/texturas aplicados sobre polígonos;
* Viewport com zoom acompanhando o jogador;
* Clipping para limitar os elementos à região da viewport.

---

# Tecnologias utilizadas

* **Python**
* **Pygame**
* Algoritmos próprios de Computação Gráfica

O Pygame é utilizado principalmente para:

* criação da janela;
* leitura de teclado;
* carregamento de imagens;
* acesso à superfície gráfica;
* utilização do `set_at()` para escrita de pixels;
* controle do loop principal do jogo.

Os algoritmos gráficos utilizados no projeto foram implementados no código da aplicação.

---

# Funcionalidades de Computação Gráfica

O projeto contempla os principais requisitos solicitados na atividade.

## 1. Set Pixel

Foi implementada uma função própria para escrita de pixels, responsável por verificar os limites da superfície e aplicar o pixel na posição desejada.

---

## 2. Primitivas de Rasterização

Foram implementados algoritmos próprios para rasterização das principais primitivas:

* **Reta**
* **Circunferência**

Essas primitivas são utilizadas na construção dos elementos gráficos do projeto e na tela de abertura.

---

## 3. Preenchimento de regiões

Foram utilizados algoritmos de preenchimento de regiões, incluindo:

* **Flood Fill / Boundary Fill**
* **Scanline Fill**

O Scanline é utilizado principalmente no preenchimento de polígonos.

---

## 4. Polígonos

Os elementos do jogo são construídos utilizando polígonos.

Os polígonos podem ser preenchidos através de:

* preenchimento sólido;
* mapeamento de texturas.

---

## 5. Mapeamento de Textura

O projeto implementa **mapeamento de textura sobre polígonos**.

As coordenadas UV são utilizadas para determinar quais pixels da imagem devem ser aplicados aos pixels correspondentes do polígono.

O sistema também é utilizado no background do jogo.

A textura do cenário é mapeada de acordo com a região do mundo visualizada pela câmera, permitindo que o background acompanhe o movimento e o zoom do jogador.

---

## 6. Transformações Geométricas

Foram implementadas as três principais transformações geométricas:

### Translação

Utilizada para movimentar objetos dentro do mundo do jogo.

### Escala

Utilizada para modificar o tamanho dos objetos e também no sistema de zoom da viewport.

### Rotação

Utilizada para alterar a orientação dos objetos, incluindo elementos móveis do jogo.

As transformações são realizadas utilizando matrizes de transformação.

---

## 7. Janela e Viewport

O projeto possui um sistema de **janela de mundo e viewport**.

A janela define qual região do mundo será visualizada, enquanto a viewport define onde essa região será apresentada na tela.

A câmera acompanha a posição do jogador:

```text
                 MUNDO DO JOGO
┌─────────────────────────────────────────┐
│                                         │
│        ┌───────────────┐                │
│        │               │                │
│        │    JOGADOR    │                │
│        │               │                │
│        └───────────────┘                │
│             JANELA                      │
│                                         │
└─────────────────────────────────────────┘
                    │
                    │ transformação
                    ▼
             ┌─────────────┐
             │   VIEWPORT  │
             │             │
             │   JOGADOR   │
             │             │
             └─────────────┘
```

O sistema inclui:

* translação da janela;
* zoom através de escala;
* transformação de coordenadas do mundo para a viewport;
* limitação da janela aos limites da arena.

---

## 8. Clipping

O clipping é utilizado para impedir que elementos desenhados ultrapassem os limites definidos para a viewport.

---

## 9. Input

O jogo possui interação através do teclado.
A Movimentação é feita com "WASD"
Para ficar mais lento sua-se Shift
Para mudar de minimapa para zoom usa-se a tecla V
E para atirar usa-se a seta para cima

---

## 10. Menu e interação gráfica

O projeto possui um menu interativo para navegação entre as diferentes partes do jogo.

A interação é realizada através dos dispositivos de entrada disponíveis ao jogador.

---

# 🗂️ Estrutura do projeto

A organização do código está dividida em módulos de acordo com suas responsabilidades.

```text
/
├── game.py
├── engine.py
├── graphic_functions.py
├── input.py
├── player.py
├── enemy.py
├── bullet.py
└── README.md
```

### Principais módulos

**`game.py`**

Responsável pelo loop principal do jogo, gerenciamento da cena, atualização dos objetos e desenho das diferentes áreas da tela.

**`graphic_functions.py`**

Contém as funções relacionadas à Computação Gráfica, incluindo rasterização, preenchimento, transformações, clipping, viewport e mapeamento de textura.

**`engine.py`**

Contém funções e estruturas relacionadas ao funcionamento do jogo, como transformações, movimentação, colisões e outras operações auxiliares.

**`player.py`**

Implementa o jogador, incluindo sua movimentação, representação gráfica e interação com o ambiente.

**`enemy.py`**

Implementa os inimigos e seus comportamentos.

**`bullet.py`**

Implementa os projéteis e seu comportamento durante o jogo.

---

# ⚙️ Como executar

## Pré-requisitos

É necessário possuir:

* **Python 3.x**
* **Pip**
* **Pygame**

## Executando o jogo

Execute o arquivo principal:

```bash
cd Python
python main.py
```

ou:

```bash
cd Python
python3 main.py
```

---

# Controles

| Tecla     | Ação                |
| --------- | ------------------- |
| `W` | Mover para cima     |
| `A` | Mover para esquerda |
| `S` | Mover para baixo    |
| `D` | Mover para direita  |
| `Tecla para cima` | Atirar              |
| `V` | Alternar Minimapa |
