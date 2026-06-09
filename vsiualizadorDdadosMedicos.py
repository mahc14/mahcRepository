import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 - Importar os dados
df = pd.read_csv('medical_examination.csv')

# 2 - Adicionar coluna 'overweight'
df['overweight'] = (df['weight'] / (df['height'] / 100) ** 2).apply(lambda x: 1 if x > 25 else 0)

# 3 - Normalizar cholesterol e gluc: 0 = bom, 1 = ruim
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)


# 4 - Desenhar o Gráfico Categórico
def draw_cat_plot():
    # 5 - Criar DataFrame com pd.melt
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # 6 - Agrupar e reformatar os dados, renomear coluna para contagem
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).size()
    df_cat.rename(columns={'size': 'total'}, inplace=True)

    # 7 - Criar catplot com seaborn
    g = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar'
    )

    # 8 - Obter figura e armazenar em fig
    fig = g.fig

    # 9 - Não modificar as linhas abaixo
    fig.savefig('catplot.png')
    return fig


# 10 - Desenhar o Mapa de Calor
def draw_heat_map():
    # 11 - Limpar os dados
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12 - Calcular a matriz de correlação
    corr = df_heat.corr()

    # 13 - Gerar máscara para o triângulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14 - Configurar a figura do matplotlib
    fig, ax = plt.subplots(figsize=(12, 10))

    # 15 - Plotar a matriz de correlação com sns.heatmap()
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        center=0,
        vmin=-0.16,
        vmax=0.32,
        square=True,
        linewidths=0.5,
        ax=ax,
        cbar_kws={'shrink': 0.5}
    )

    # 16 - Não modificar as linhas abaixo
    fig.savefig('heatmap.png')
    return fig