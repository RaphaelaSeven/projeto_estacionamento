# 🅿️ Sistema de Gestão de Estacionamento (CLI)

Sistema de controle de estacionamento desenvolvido em **Python**, executado via linha de comando (CLI). O projeto conta com persistência de dados em formato JSON, validação de placas (padrão nacional antigo e Mercosul), gerenciamento de vagas exclusivas (PCD) e um sistema integrado de logs e simulação de colisões.

---

## 🚀 Funcionalidades

* **Controle de Entrada e Saída:** Gerenciamento em tempo real de até 15 vagas.
* **Validação de Placas:** Utilização de Expressões Regulares (`Regex`) para garantir o formato correto de placas brasileiras (antigas e padrão Mercosul).
* **Prevenção de Duplicidade:** O sistema impede que o mesmo veículo seja cadastrado duas vezes simultaneamente.
* **Vaga Exclusiva PCD:** Validação interativa para vagas reservadas.
* **Persistência de Dados (`Dados.json`):** As informações de ocupação são salvas automaticamente, garantindo que os dados não sejam perdidos ao fechar o programa.
* **Simulação de Colisão:** Algoritmo probabilístico baseado na ocupação de vagas vizinhas, registrando avisos quando aplicável.
* **Sistema de Logs (`estacionamento.log`):** Registro de eventos e alertas críticos em segundo plano.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* Módulos nativos utilizados:
  * `json` (Manipulação e salvamento de dados)
  * `os` (Verificação de arquivos no sistema operacional)
  * `logging` (Geração de logs do sistema)
  * `random` (Lógica probabilística para simulação de colisão)
  * `re` (Validação de padrões com Expressões Regulares)

---

## 📦 Como Executar o Projeto

1. Certifique-se de ter o **Python 3** instalado em sua máquina.
2. Clone este repositório ou faça o download do arquivo `estacionana.py`:
   ```bash
   git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)


