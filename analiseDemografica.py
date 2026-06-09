import pandas as pd
import urllib.request
import io

# Carregar dataset do censo 1994
url = "https://raw.githubusercontent.com/freeCodeCamp/boilerplate-demographic-data-analyzer/main/adult.data.csv"
response = urllib.request.urlopen(url)
df = pd.read_csv(io.StringIO(response.read().decode('utf-8')))

print("=" * 55)
print("   ANÁLISE DEMOGRÁFICA — CENSO DE 1994")
print("=" * 55)

# 1. Contagem por raça
print("\n1. Pessoas por raça:")
race_count = df['race'].value_counts()
print(race_count.to_string())

# 2. Média de idade dos homens
avg_age_men = df[df['sex'] == 'Male']['age'].mean().round(1)
print(f"\n2. Média de idade dos homens: {avg_age_men} anos")

# 3. % com diploma Bachelors
bachelors_pct = round((df['education'] == 'Bachelors').mean() * 100, 1)
print(f"\n3. % com diploma de Bacharel: {bachelors_pct}%")

# 4. % educação superior com >50K
higher_ed = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
higher_ed_rich = round((df[higher_ed]['salary'] == '>50K').mean() * 100, 1)
print(f"\n4. % educação superior que ganha >50K: {higher_ed_rich}%")

# 5. % sem educação superior com >50K
lower_ed_rich = round((df[~higher_ed]['salary'] == '>50K').mean() * 100, 1)
print(f"\n5. % sem educação superior que ganha >50K: {lower_ed_rich}%")

# 6. Mínimo de horas por semana
min_hours = df['hours-per-week'].min()
print(f"\n6. Mínimo de horas trabalhadas por semana: {min_hours}h")

# 7. % mínimo de horas e >50K
min_workers = df[df['hours-per-week'] == min_hours]
min_workers_rich_pct = round((min_workers['salary'] == '>50K').mean() * 100, 1)
print(f"\n7. % que trabalham {min_hours}h/semana e ganham >50K: {min_workers_rich_pct}%")

# 8. País com maior % >50K
country_pct = (
    df[df['salary'] == '>50K']['native-country'].value_counts()
    / df['native-country'].value_counts() * 100
).dropna()
top_country = country_pct.idxmax()
top_pct = round(country_pct.max(), 1)
print(f"\n8. País com maior % de >50K: {top_country} ({top_pct}%)")

# 9. Ocupação mais popular na Índia (>50K)
india_rich = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
top_occ_india = india_rich['occupation'].value_counts().idxmax()
print(f"\n9. Ocupação mais popular na Índia (>50K): {top_occ_india}")

print("\n" + "=" * 55)