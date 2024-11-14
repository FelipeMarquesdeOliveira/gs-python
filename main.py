import json
import webbrowser
import matplotlib.pyplot as plt

def carregar_dados(arquivo='dados.json'):
    """
    Carrega dados de um arquivo JSON.
    """
    try:
        with open(arquivo, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def obter_tarifa(consumo_mensal):
    """
    Retorna a tarifa com base no consumo mensal em kWh.
    """
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
    """
    Salva os dados no arquivo JSON.
    """
    try:
        with open(arquivo, 'w') as f:
            json.dump(dados, f, indent=4)
    except Exception as e:
        print("Erro ao salvar dados:", e)

def gerar_grafico(dados):
    """
    Gera um gráfico comparativo entre custos com e sem energia solar.
    """
    custo_instalacao = dados.get("custo_instalacao", 0)
    economia_mensal = dados.get("economia_mensal", 0)
    consumo_mensal = dados.get("consumo_mensal", 0)
    anos = 10
    
    custo_comum = []
    custo_solar = []
    
    acumulado_comum = 0
    acumulado_solar = custo_instalacao
    
    for ano in range(anos):
        acumulado_comum += consumo_mensal * 12
        acumulado_solar = max(0, acumulado_solar - economia_mensal * 12)
        
        custo_comum.append(acumulado_comum)
        custo_solar.append(acumulado_solar)
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(anos), custo_comum, label="Custo sem energia solar", color="red", linestyle="--")
    plt.plot(range(anos), custo_solar, label="Custo com energia solar", color="green")
    
    plt.title("Comparação de Custos com e sem Energia Solar ao Longo dos Anos")
    plt.xlabel("Anos")
    plt.ylabel("Custo Acumulado (R$)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    plt.show()

def calcular_custo_instalacao(dados):
    """
    Calcula o custo de instalação com base no consumo mensal.
    """
    try:
        consumo_mensal = float(input("Insira o consumo médio mensal (em kWh): "))
        capacidade_necessaria_kw = round((consumo_mensal / 150) + 0.5)
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
    """
    Calcula a economia mensal com energia solar.
    """
    try:
        media_consumo = float(input("Insira o consumo médio mensal (em kWh): "))
        tarifa = float(input("Insira a tarifa de energia de sua região (EX: R$1 por kwh) "))
        economia_total = media_consumo * tarifa

        dados['economia_mensal'] = economia_total
        salvar_dados_automaticamente(dados)

        return economia_total
    except ValueError:
        print("Valor inválido. Por favor, insira números válidos.")
        return None

def calcular_tempo_retorno(dados):
    """
    Calcula o tempo de retorno do investimento em energia solar.
    """
    try:
        if 'custo_instalacao' in dados and 'economia_mensal' in dados and dados['economia_mensal'] > 0:
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
    """
    Exibe o menu e gerencia a navegação do sistema de cotação.
    """
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
            gerar_grafico(dados)

        elif escolha == "5":
            print("Abrindo link para contato no Instagram...")
            webbrowser.open("https://www.instagram.com/greenwave2207/")

        elif escolha == "6":
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida. Tente novamente.")

menu()
