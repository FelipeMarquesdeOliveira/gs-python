import json
import webbrowser
import matplotlib.pyplot as plt


def carregar_dados(arquivo='dados.json'):
    try:
        with open(arquivo, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def obter_tarifa(consumo_mensal):
    if consumo_mensal <= 30:
        return 1.62
    elif consumo_mensal <= 50:
        return 3.24
    elif consumo_mensal <= 100:
        return 12.95
    elif consumo_mensal <= 200:
        return 25.89
    elif consumo_mensal <= 300:
        return 35.60
    else:
        return 45.31


def salvar_dados_automaticamente(dados, arquivo='dados.json'):
    try:
        with open(arquivo, 'w') as f:
            json.dump(dados, f, indent=4)
    except Exception as e:
        print("Erro ao salvar dados:", e)


def calcular_custo_instalacao(dados):
    print("\nPara calcular o custo de instalação, insira o consumo médio mensal de energia em kWh.")
    print("Esse valor geralmente está indicado na conta de luz como 'Consumo Total' ou 'Consumo em kWh'.\n")

    try:
        consumo_mensal = float(input("Insira o consumo médio mensal (em kWh): "))
        capacidade_necessaria_kw = (consumo_mensal / 150)
        capacidade_necessaria_kw = round(capacidade_necessaria_kw + 0.5)
        custo_por_kw = 5000
        custo_total = capacidade_necessaria_kw * custo_por_kw

        print(f"Custo total de instalação (estimado): R$ {custo_total:.2f}")

        dados['custo_instalacao'] = custo_total
        dados['consumo_mensal'] = consumo_mensal

        salvar_dados_automaticamente(dados)

        return custo_total
    except ValueError:
        print("Valor inválido. Por favor, insira um número válido.")
        return None


def calcular_economia_mensal(dados):
    print("\nPara calcular a economia mensal, você precisará do consumo médio mensal e da tarifa de energia.")
    print("Consumo Médio Mensal: Veja na sua conta de luz a seção 'Consumo Total' ou 'Consumo em kWh'.")
    print("Tarifa de Energia: Normalmente está indicada como 'Tarifa de Energia' e é o custo por kWh.\n")

    try:
        media_consumo = float(input("Insira o consumo médio mensal (em kWh): "))
        tarifa = float(input("Insira a tarifa de energia de sua região (EX: R$1 por kwh) "))
        economia_total = media_consumo * tarifa
        taxa = obter_tarifa(media_consumo)
        economia = economia_total - taxa

        print(f"\nEconomia Mensal Bruta Estimada: R${economia_total:.2f}")
        print(f"Taxa Base Subtraída: R${taxa:.2f}")
        print(f"Economia Final Mensal Estimada: R${economia:.2f}")

        dados['economia_mensal'] = economia

        salvar_dados_automaticamente(dados)

        return economia
    except ValueError:
        print("Valor inválido. Por favor, insira números válidos.")
        return None


def calcular_tempo_retorno(dados):
    print("\nPara calcular o tempo de retorno, precisamos do custo total de instalação e da economia mensal.")
    print("Isso nos ajuda a saber em quantos meses o investimento será recuperado com a economia na conta de luz.\n")

    try:
        if 'custo_instalacao' in dados and 'economia_mensal' in dados:
            retorno_meses = dados['custo_instalacao'] / dados['economia_mensal']
            anos = int(retorno_meses // 12)
            meses = int(retorno_meses % 12)

            print(f"Tempo de retorno estimado: {anos} anos e {meses} meses")
            return retorno_meses
        else:
            print("Calcule primeiro o custo de instalação e a economia mensal.")
            return None
    except ZeroDivisionError:
        print("Erro: economia mensal é zero.")
        return None


def menu():
    dados = carregar_dados()
    while True:
        print("\n---------------------------------------------")
        print("                 Green Wave                     ")
        print("         Soluções em Energia Solar              ")
        print("---------------------------------------------")
        print("--- Sistema de Cotação para Energia Solar ---")
        print("---------------------------------------------\n")
        print("1. Cotar Custo de Instalação")
        print("2. Cotar Economia Mensal")
        print("3. Calcular Tempo de Retorno")
        print("4. Gerar Gráfico Comparativo")
        print("5. Contate-nos")
        print("6. Sair\n")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            calcular_custo_instalacao(dados)

        elif escolha == "2":
            calcular_economia_mensal(dados)

        elif escolha == "3":
            calcular_tempo_retorno(dados)

        elif escolha == "4":
            print()

        elif escolha == "5":
            print("Abrindo link para contato no Instagram...")
            webbrowser.open("")

        elif escolha == "6":
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida. Tente novamente.")


menu()