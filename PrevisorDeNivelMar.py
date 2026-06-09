import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # 1. Importar os dados
    df = pd.read_csv('epa-sea-level.csv')

    # 2. Criar o diagrama de dispersão
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], label='Dados originais', alpha=0.6)

    # 3. Linha de melhor ajuste com TODOS os dados (1880–2050)
    slope1, intercept1, *_ = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    years_extended = range(df['Year'].min(), 2051)
    sea_level_pred1 = [slope1 * year + intercept1 for year in years_extended]
    ax.plot(years_extended, sea_level_pred1, color='red', label='Melhor ajuste (1880–2050)')

    # 4. Linha de melhor ajuste apenas com dados a partir do ano 2000
    df_2000 = df[df['Year'] >= 2000]
    slope2, intercept2, *_ = linregress(df_2000['Year'], df_2000['CSIRO Adjusted Sea Level'])
    years_2000 = range(2000, 2051)
    sea_level_pred2 = [slope2 * year + intercept2 for year in years_2000]
    ax.plot(years_2000, sea_level_pred2, color='green', label='Melhor ajuste (2000–2050)')

    # 5. Rótulos, título e legenda
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level (inches)')
    ax.set_title('Rise in Sea Level')
    ax.legend()

    # Salvar e retornar a imagem
    plt.tight_layout()
    plt.savefig('sea_level_plot.png')
    return plt.gca()