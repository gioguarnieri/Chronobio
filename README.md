## Instalando o Python

### Windows

Acho o melhor jeito de instalar o python a partir do [spyder](https://www.spyder-ide.org/) que você instala junto com o [anaconda](https://www.anaconda.com/products/individual), a instalação é bem fácil e direta. 

### MAC

Para MAC existem mais jeitos, pode instalar o [python pelo terminal](https://python.org.br/instalacao-mac/) ou usar o próprio [spyder](https://www.spyder-ide.org/) que você instala junto com o [anaconda](https://www.anaconda.com/products/individual), a instalação é bem fácil e direta. 

## Dependências 

Para rodar o script vamos precisar que algumas dependências sejam instaladas, de preferência na mesma versão que usei, versões diferentes podem causar problemas. A instalação dos pacotes depende de como instalou o Python em sua máquina.

As dependências são:

PyQt5==5.14.1

scipy==1.4.1

numpy==1.18.1

[Pelo Anaconda](https://docs.anaconda.com/anaconda/user-guide/tasks/install-packages/). Exemplo: conda install scipy=1.4.1 (note que aqui é só um igual)

[Pelo terminal](https://docs.python.org/3/installing/index.html). Exemplo: python -m pip install scipy==1.4.1

# Rotinas

## Rotinas de interface

Não sou muito bom nessa parte, as rotinas de interface ficaram bem simples e com alguns bugs, mas servem o propósito. Elas são:

  - getInteger(): Pega o valor da coluna que deve ser analisada;
  - getDouble(): Pega dois valores de Threshold caso seja necessário;
  - ifThresh(): Verifica se o usuário quer aplicar um threshold ou não;
  - ifSmooth(): Pergunta se o usuário quer aplicar uma suavização dos dados
  - getWeight(): Pega o peso que deve ser feito para a suavização;
  - ifDetrend(): Pergunta se o usuário quer destendenciar os dados;
  - showGraph(): Mostra o gráfico, não funciona sempre, sei lá por que.


## Funções de tratamento

Funções que tratam os dados, fazem limpeza, suavizam, etc.

  - suaviza(dados, pesos): Recebe o conjunto de dados e pesos e faz uma suavização que calcula um novo data set pegando 3 dados e substituindo o central pela média ponderada dos que estão em volta;
  - writeFile(dados): Escreve os dados em um arquivo;
  - plotData(dados, threshold, legendas do gráfico): plota um gráfico;
  - mkHisto(dados, legendas do gráfico): plota um histograma;
  - detrend(dados): destendecia os dados ao fazer uma regressão linear nos dados e diminuir o valor da regressão em todos os dados;
  - hrlyMean(dados): faz a média horária dos dados, começando, por exemplo, das 10:30:00 e indo até 11:30:00.
  
# Funcionamento do script

O script vai retornar pro usuário um arquivo de dados pronto pra entrar numa outra rotina (colocar o nome aqui) já feita anteriormente pra análise desses dados. A ideia é simplesmente preparar os arquivos de dados para fazer uma entrada no script seguinte e gerar uma certa visualização pro usuário.
