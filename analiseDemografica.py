import argparse
import io
import os
import sys
import urllib.request
from urllib.error import URLError

import pandas as pd

DEFAULT_SOURCE = (
    "https://raw.githubusercontent.com/freeCodeCamp/boilerplate-demographic-data-analyzer/main/adult.data.csv"
)
EXPECTED_COLUMNS = {
    'age',
    'workclass',
    'fnlwgt',
    'education',
    'education-num',
    'marital-status',
    'occupation',
    'relationship',
    'race',
    'sex',
    'capital-gain',
    'capital-loss',
    'hours-per-week',
    'native-country',
    'salary',
}


def load_dataset(source: str) -> pd.DataFrame:
    """Carrega o dataset do Censo 1994 de um URL ou caminho local."""
    if source.startswith(('http://', 'https://')):
        try:
            with urllib.request.urlopen(source, timeout=30) as response:
                content = response.read().decode('utf-8')
        except URLError as error:
            raise ValueError(f'Não foi possível carregar o arquivo remoto: {error}') from error
        df = pd.read_csv(io.StringIO(content))
    else:
        if not os.path.isfile(source):
            raise FileNotFoundError(f'O arquivo não existe: {source}')
        df = pd.read_csv(source)

    missing_columns = EXPECTED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(
            'O dataset não contém as colunas esperadas: ' + ', '.join(sorted(missing_columns))
        )

    return df


def compute_demographic_analysis(df: pd.DataFrame) -> dict:
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    min_hours = int(df['hours-per-week'].min())

    results = {
        'race_count': df['race'].value_counts().to_dict(),
        'avg_age_men': round(df[df['sex'] == 'Male']['age'].mean(), 1),
        'bachelors_pct': round((df['education'] == 'Bachelors').mean() * 100, 1),
        'higher_ed_rich_pct': round((df[higher_education]['salary'] == '>50K').mean() * 100, 1),
        'lower_ed_rich_pct': round((df[~higher_education]['salary'] == '>50K').mean() * 100, 1),
        'min_hours_per_week': min_hours,
        'min_workers_rich_pct': round(
            (df[df['hours-per-week'] == min_hours]['salary'] == '>50K').mean() * 100,
            1,
        ),
    }

    country_rich_pct = (
        df[df['salary'] == '>50K']['native-country'].value_counts()
        / df['native-country'].value_counts()
        * 100
    ).dropna()
    if not country_rich_pct.empty:
        results['top_country'] = country_rich_pct.idxmax()
        results['top_country_pct'] = round(country_rich_pct.max(), 1)
    else:
        results['top_country'] = None
        results['top_country_pct'] = 0.0

    india_rich = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    results['top_occupation_india'] = (
        india_rich['occupation'].value_counts().idxmax()
        if not india_rich.empty
        else None
    )
    return results


def format_results(results: dict) -> str:
    lines = [
        '=' * 55,
        '   ANÁLISE DEMOGRÁFICA — CENSO DE 1994',
        '=' * 55,
        '\n1. Pessoas por raça:',
    ]

    for race, count in results['race_count'].items():
        lines.append(f'   {race}: {count}')

    lines.extend([
        f"\n2. Média de idade dos homens: {results['avg_age_men']} anos",
        f"3. % com diploma de Bacharel: {results['bachelors_pct']}%",
        f"4. % com educação superior que ganha >50K: {results['higher_ed_rich_pct']}%",
        f"5. % sem educação superior que ganha >50K: {results['lower_ed_rich_pct']}%",
        f"6. Mínimo de horas trabalhadas por semana: {results['min_hours_per_week']}h",
        f"7. % que trabalham {results['min_hours_per_week']}h/semana e ganham >50K: {results['min_workers_rich_pct']}%",
    ])

    if results['top_country']:
        lines.append(
            f"8. País com maior % de >50K: {results['top_country']} ({results['top_country_pct']}%)"
        )
    else:
        lines.append('8. País com maior % de >50K: N/A')

    lines.append(
        f"9. Ocupação mais popular na Índia (>50K): {results['top_occupation_india'] or 'N/A'}"
    )
    lines.append('=' * 55)

    return '\n'.join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Executa análise demográfica do dataset do Censo de 1994.'
    )
    parser.add_argument(
        '--source',
        '-s',
        default=DEFAULT_SOURCE,
        help='URL ou caminho local para o arquivo CSV de dados.',
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        df = load_dataset(args.source)
    except (FileNotFoundError, ValueError, URLError, pd.errors.ParserError) as exc:
        print(f'Erro: {exc}', file=sys.stderr)
        return 1

    results = compute_demographic_analysis(df)
    print(format_results(results))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
