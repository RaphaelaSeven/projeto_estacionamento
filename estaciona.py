# ==============================================================================
# IMPORTAÇÃO DE BIBLIOTECAS (Módulos embutidos do Python)
# ==============================================================================
import logging  # Biblioteca para criar "arquivos de log" (registros do sistema no fundo)
import json     # Biblioteca para ler e gravar dados no formato JSON (JavaScript Object Notation)
import os       # Biblioteca para interagir com o Sistema Operacional (ex: verificar se um arquivo existe)
import random   # Biblioteca para gerar números aleatórios (usada na lógica de colisão)
import re       # Biblioteca para Expressões Regulares (Regex), usada para validar o formato da placa

# ==============================================================================
# CONFIGURAÇÕES GLOBAIS (Constantes)
# ==============================================================================
# Por convenção em Python, variáveis que não devem mudar de valor são escritas em MAIÚSCULAS.
VAGAS_TOTAIS = 15
VAGAS_PCD = ["1"]  # Lista contendo as chaves (strings) das vagas reservadas para PCD.
ARQUIVO_BD = 'Dados.json' # Nome do arquivo que servirá como nosso "Banco de Dados"

# Configuração do sistema de "Logging" (Diário de bordo do sistema)
# Isso cria um arquivo txt (estacionamento.log) que guarda eventos silenciosos.
logging.basicConfig(
    filename='estacionamento.log', # Onde salvar
    encoding='utf-8',              # Aceitar acentos
    level=logging.INFO,            # Nível mínimo de gravidade para registrar (INFO, WARNING, ERROR)
    format='%(asctime)s - %(levelname)s - %(message)s', # Formato: Data/Hora - Nível - Mensagem
)

# ==============================================================================
# FUNÇÕES AUXILIARES (Pequenos blocos de código que resolvem problemas específicos)
# ==============================================================================

def carregar_banco():
    """Carrega o arquivo JSON com tratamento de erro."""
    
    # ESTRUTURA DE DECISÃO: Verifica se o arquivo de dados já existe na pasta
    if os.path.exists(ARQUIVO_BD):
        # TRATAMENTO DE EXCEÇÃO (try/except):
        # O programa "tenta" executar o bloco 'try'. Se algo der errado (ex: arquivo corrompido),
        # em vez do programa "crachar" (fechar na cara do usuário), ele pula pro 'except'.
        try:
            # A instrução 'with open()' abre o arquivo de forma segura. 
            # O 'r' significa READ (Leitura). Ao sair do bloco 'with', o arquivo fecha sozinho.
            with open(ARQUIVO_BD, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo) # Converte o texto do JSON para um Dicionário Python
        except (json.JSONDecodeError, OSError):
            # Se o JSON estiver quebrado ou houver erro no sistema de arquivos, avisa o usuário.
            print("Erro ao carregar o banco. Criando novo arquivo...")
    
    # Se o arquivo não existir ou deu erro lá em cima, criamos os dados do zero.
    # COMPREENSÃO DE DICIONÁRIO: Uma forma rápida de criar um dicionário num loop só.
    # Cria chaves de "1" a "15" com o valor 'None' (Vazio) para todas elas.
    dados = {str(i): None for i in range(1, VAGAS_TOTAIS + 1)}
    salvar_banco(dados) # Chama a função abaixo para já criar o arquivo físico
    return dados


def salvar_banco(dados):
    """Salva o estado atual no JSON."""
    # O 'w' significa WRITE (Escrita). Ele apaga o arquivo antigo e escreve por cima.
    with open(ARQUIVO_BD, 'w', encoding='utf-8') as arquivo:
        # Pega o Dicionário Python ('dados') e converte de volta para texto JSON no 'arquivo'.
        # indent=4 deixa o arquivo formatado bonitinho para leitura humana.
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def contar_ocupadas(estacionamento):
    """Conta quantas vagas estão ocupadas."""
    # EXPRESSÃO GERADORA: Faz um laço (for) por todos os valores do dicionário.
    # Se o valor não for nulo (is not None), ele soma 1. Retorna o total da soma.
    return sum(1 for vaga in estacionamento.values() if vaga is not None)


def validar_placa(placa):
    """Valida placa brasileira (antiga e Mercosul)."""
    # EXPRESSÃO REGULAR (Regex): Uma fórmula textual para validar padrões.
    # ^[A-Z]{3} = Começa com exatas 3 letras.
    # [0-9] = Seguido por 1 número.
    # [A-Z0-9] = Seguido por 1 letra ou número (cobre o padrão Mercosul e o Antigo).
    # [0-9]{2}$ = Termina com exatos 2 números.
    padrao = r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$'
    # Retorna True se a placa bater com a fórmula, ou False se não bater.
    return re.match(padrao, placa) is not None


def placa_ja_existe(estacionamento, placa):
    """Verifica se a placa já está no estacionamento."""
    # Verifica se o texto da placa está dentro da lista de valores do dicionário.
    return placa in estacionamento.values()


# ==============================================================================
# EXIBIÇÃO
# ==============================================================================

def exibir_painel(estacionamento):
    ocupadas = contar_ocupadas(estacionamento)
    livres = VAGAS_TOTAIS - ocupadas

    print("\n" + "="*50)
    print("           MAPA DO ESTACIONAMENTO")
    print("="*50)

    # LAÇO FOR (Repetição com contador): Vai do número 1 até o limite (15).
    # O + 1 é necessário porque o range em Python para um número ANTES do limite final.
    for i in range(1, VAGAS_TOTAIS + 1):
        chave = str(i) # Converte o número (ex: 1) para texto (ex: "1") para buscar no dicionário
        placa = estacionamento.get(chave, None) # Pega o que tem dentro da vaga (pode ser a placa ou None)

        if placa is None: # Vaga Vazia
            if chave in VAGAS_PCD: # Verifica se a chave atual (ex:"1") está na lista de PCD
                status = "Livre (PCD)"
            else:
                status = "Livre"
        else: # Vaga Ocupada
            status = f"Ocupada: {placa}" # f-string para injetar a variável dentro do texto

        # {i:02d} formata o número inteiro para ter sempre dois dígitos (ex: 01, 02... 10)
        print(f"Vaga {i:02d}: [ {status} ]")

    print("-"*50)
    print(f"{ocupadas} ocupadas | {livres} livres")
    print("="*50)


# ==============================================================================
# COLISÃO
# ==============================================================================

def verificar_colisao(vaga, estacionamento):
    vaga = int(vaga) # Converte a string "vaga" digitada pelo usuário em número inteiro
    vizinhos = 0

    # Verifica o vizinho de trás (vaga - 1). 
    # 'in estacionamento' garante que a vaga existe (para não dar erro na vaga 0)
    if str(vaga - 1) in estacionamento and estacionamento[str(vaga - 1)]:
        vizinhos += 1

    # Verifica o vizinho da frente (vaga + 1).
    if str(vaga + 1) in estacionamento and estacionamento[str(vaga + 1)]:
        vizinhos += 1

    # OPERADOR TERNÁRIO: É um 'if/else' escrito numa linha só.
    chance = 0.15 if vizinhos == 1 else 0.50 if vizinhos == 2 else 0

    # random.random() gera um número decimal entre 0.0 e 1.0.
    # Se esse número for menor que a chance estipulada, a colisão ocorre.
    if random.random() < chance:
        print("⚠️ Colisão detectada!")
        # Registra o evento de colisão silenciosamente no arquivo de log criado lá no topo.
        logging.warning(f"Colisão na vaga {vaga}")


# ==============================================================================
# MAIN (FUNÇÃO PRINCIPAL DO PROGRAMA)
# ==============================================================================

def main():
    # Inicializa o dicionário puxando do arquivo JSON (ou criando um novo)
    estacionamento = carregar_banco()

    print("\n--- Sistema de Estacionamento ---")

    # LAÇO INFINITO: O programa roda eternamente até o usuário digitar '#' (break)
    while True:
        acao = input("\n(1) Entrada | (2) Saída | (3) Ver vagas | (#) Sair: ").strip()
        
        # Se a pessoa digitou um número (ex: "01"), transforma em inteiro para remover o zero,
        # e depois volta para texto ("1") para os if/elif funcionarem.
        # O .isdigit() garante que não vai dar erro se a pessoa digitar '#'
        if acao.isdigit():
            acao = str(int(acao))

        # ===================== ENTRADA =====================
        if acao == '1':
            # Evita o programa tentar processar se já está lotado
            if contar_ocupadas(estacionamento) >= VAGAS_TOTAIS:
                print("Estacionamento cheio.")
                continue # O 'continue' ignora tudo que está abaixo e VOLTA para o início do 'while'

            # .strip() remove espaços vazios acidentais e .upper() deixa tudo MAIÚSCULO
            placa = input("Placa: ").strip().upper()

            # Chamada da função de Regex. O 'not' inverte o resultado (se for False, entra aqui)
            if not validar_placa(placa):
                print("Placa inválida.")
                continue

            # Impedir duplicação de placas
            if placa_ja_existe(estacionamento, placa):
                print("Esse veículo já está no estacionamento.")
                continue

            vaga = input("Escolha a vaga: ")

            # Verifica se o que o usuário digitou realmente existe como chave no dicionário
            if vaga not in estacionamento:
                print("Vaga inválida.")
                continue

            # Se o conteúdo da chave não for 'None', é porque já tem carro
            if estacionamento[vaga] is not None:
                print("Vaga ocupada.")
                continue

            # Regra PCD
            if vaga in VAGAS_PCD:
                pcd = input("Veículo é PCD? (s/n): ").lower() # .lower() transforma em minúsculo
                if pcd != 's':
                    print("Essa vaga é exclusiva para PCD. Por favor, escolha outra vaga.")
                    continue # O continue ainda vai reiniciar a entrada, mas pelo menos a mensagem fica clara.

            # ATUALIZAÇÃO DO DICIONÁRIO: A chave (vaga) passa a guardar o valor (placa)
            estacionamento[vaga] = placa
            salvar_banco(estacionamento) # Salva a alteração imediatamente no JSON

            print("Veículo estacionado.")
            verificar_colisao(vaga, estacionamento) # Roda o algoritmo de probabilidade

        # ===================== SAÍDA =====================
        elif acao == '2':
            vaga = input("Informe a vaga: ").strip()

            if vaga not in estacionamento:
                print("Vaga inválida.")
                continue

            if estacionamento[vaga] is None:
                print("Vaga já está vazia.")
                continue

            print(f"Veículo {estacionamento[vaga]} saiu.")
            estacionamento[vaga] = None # Limpa a vaga, voltando-a para o estado nulo
            salvar_banco(estacionamento) # Atualiza o JSON com a vaga livre

        # ===================== VER VAGAS =====================
        elif acao == '3':
            exibir_painel(estacionamento)

        # ===================== SAIR =====================
        elif acao == '#':
            print("Encerrando...")
            break # O 'break' quebra a repetição do 'while True', permitindo o programa finalizar

        else:
            print("Opção inválida.")


# ==============================================================================
# EXECUÇÃO DO SCRIPT
# ==============================================================================
# O condicional abaixo é uma boa prática em Python.
# Ele garante que a função main() SÓ vai rodar se você executar ESTE arquivo diretamente.
# Se no futuro você importar este arquivo dentro de outro, a main() não vai rodar sozinha.
if __name__ == "__main__":
    main()
