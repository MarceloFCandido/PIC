# PIC01 (Projeto de Iniciação Científica 01)

Principais códigos criados durante o projeto de iniciação científica
(no CEFET-MG) que abordou a comparação de dois métodos de modelamento da
propagação de ondas em meios não-homogêneos: os métodos de **diferenças finitas**
e o de **traçamento de raios**.

## Código em manutenção
A restauração do código foi concluída, graças a Deus, e, até que se prove
contrário, ele se apresenta funcional. Contudo, há coisas ainda a se melhorar
no repositório em geral e que serão resolvidas quando eu tiver mais
disponibilidade, como:
  - mais exemplos para os códigos (principalmente para o MDF);
  - scripts de execução e Makefiles;
  - refatorar o relatório, que ainda está com o código desatualizado com relação ao repositório;
  - terminar esse `README`

## Como rodar os códigos
### Configurando o seu computador
Esse tutorial considera que o código em questão será executado em um sistema
operacional Linux derivado do Debian. Recomendado fortemente executar apenas
nesse tipo de ambiente.

Para configurar o seu computador com todos os programas e bibliotecas
pré-requisito basta tornar executável o _bash script_ `env-config.sh` com
```
$ chmod +x env-config.sh
```
executar o _script_ da seguinte forma
```
$ ./env-config.sh
```
Ele requisitará sua senha de administrador para a instalação dos pacotes e, no
fim de sua execução, limpará a tela.

### Código MDF
O tutorial de execução de código a seguir considera que o usuário está na pasta
`./src/MDF/src/` do repostório.

Primeiramente, os arquivos de configuração do meio pelo qual a onda se
propagará devem ser criados. Para tal, o usuário pode executar
`$ python userInterface.py` e colocar as entradas manualmente à medida que o
programa as requisita. O usuário também pode criar os arquivos de configuração
com a ajuda de um arquivo de texto auxiliar (como os exemplos encontrados em
`../data/inputs/`) e executar `userInterface.py` da seguinte forma
```
$ python userInterface.py < arquivoAuxiliar
```
Com isso, não será necessário colocar as entradas durante a execução da
interface.

Em seguida, o usuário deve escolher se quer executar o código com
fronteiras abertas (`openBoundaries.py`) ou com fronteiras reflexivas
(`reflect.py`). Para o primeiro basta executar
```
$ python openBoundaries.py
```
e para o segundo, de semelhante forma,
```
$ python reflect.py
```
A execução pode demorar dependendo do número de pontos que o usuário determinar
para a malha.

Por fim, para visualizar os dados gerados, o usuário pode criar _snapshots_
utilizando `snapshoter.py` dessa forma
```
$ python snapshoter.py
```
Com isso, basta seguir as requisições do programa e esperar sua execução
terminar, o que pode demorar, dependendo do número de images requisitadas
pelo usuário e o número de pontos com que a malha foi definida. As imagens
geradas podem ser encontradas em `../data/images/open/` ou
`../data/images/reflect/`, dependendo da simulação escolhida durante a
execução de `snapshoter.py`. Fronteiras abertas para o primeiro caminho,
fronteiras reflexivas para o segundo.

### Código TR
**A fazer**.
