import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =================================================================
# 1. CONFIGURAÇÃO E CARREGAMENTO
# =================================================================
# Certifique-se de que o arquivo CSV está na mesma pasta do script
NOME_ARQUIVO = 'Bank_Personal_Loan_Modelling.csv'
df = pd.read_csv(NOME_ARQUIVO)

# =================================================================
# 2. LIMPEZA E ENGENHARIA DE DADOS (DATA PREPARATION)
# =================================================================

# A coluna CCAvg (Gasto médio no cartão) vem como "1/60", precisamos converter para 1.6
df['CCAvg'] = df['CCAvg'].str.replace('/', '.').astype(float)

# Mapeamento da Escolaridade para nomes legíveis (Fundamental para o relatório)
educacao_map = {
    1: 'Graduação', 
    2: 'Pós-Graduação', 
    3: 'Especialização/PHD'
}
df['Escolaridade'] = df['Education'].map(educacao_map)

# Criação de Faixas de Renda (Bins) para segmentação estratégica
# Dividimos a renda em 3 grupos: Baixa, Médio e Alta
df['Faixa_Renda'] = pd.qcut(df['Income'], q=3, labels=['Renda Baixa', 'Renda Média', 'Renda Alta'])

# =================================================================
# 3. ANÁLISE DE CONVERSÃO (CROSS-SELL)
# =================================================================

# Criamos a matriz que mostra a taxa de aceitação do empréstimo (%)
# cruzando Escolaridade vs. Faixa de Renda
matriz_conversao = df.pivot_table(
    index='Escolaridade', 
    columns='Faixa_Renda', 
    values='Personal Loan', 
    aggfunc='mean'
) * 100

# =================================================================
# 4. VISUALIZAÇÃO DOS RESULTADOS (DASHBOARD)
# =================================================================

plt.figure(figsize=(12, 7))

# Criando o Heatmap (Mapa de Calor)
sns.heatmap(
    matriz_conversao, 
    annot=True,            # Coloca os números dentro dos quadrados
    cmap='YlGnBu',         # Escala de cores (Amarelo, Verde, Azul)
    fmt='.2f',             # Duas casas decimais
    cbar_kws={'label': 'Taxa de Conversão (%)'}
)

plt.title('Matriz de Propensão: Escolaridade vs. Nível de Renda', fontsize=15, pad=20)
plt.xlabel('Segmento de Renda Anual', fontsize=12)
plt.ylabel('Nível de Instrução', fontsize=12)

# Salva o gráfico para usar no LaTeX/Apresentação
plt.tight_layout()
plt.savefig('matriz_conversao_final.png')

# =================================================================
# 5. EXPORTAÇÃO E SUMÁRIO NO TERMINAL
# =================================================================

print("\n" + "="*40)
print("📊 RESULTADOS DA ANÁLISE DE CONVERSÃO (%)")
print("="*40)
print(matriz_conversao)
print("-" * 40)

# Mostra também o número de clientes em cada grupo para validar a amostra
print("\n👥 DISTRIBUIÇÃO DA BASE (Nº DE CLIENTES POR GRUPO):")
print(df.groupby(['Escolaridade', 'Faixa_Renda']).size().unstack())

# Exporta a base tratada caso precise abrir no Excel
df.to_csv('base_propensao_tratada.csv', index=False)
print("\n✅ Arquivos 'matriz_conversao_final.png' e 'base_propensao_tratada.csv' gerados!")