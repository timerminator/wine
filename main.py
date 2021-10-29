from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from itertools import groupby
import collections
import argparse


def main():
    parser = argparse.ArgumentParser(description='Запуск винного сайта')
    parser.add_argument('-f', '--filepath', help='Расположение каталога товаров', default='wine3.xlsx')
    args = parser.parse_args()

    births_year = 1920
    this_year = datetime.datetime.now().year
    years = this_year - births_year

    drinks = pandas.read_excel(args.filepath, na_values=['N/A', 'NA'], keep_default_na=False).to_dict(orient='record')
    drinks = sorted(drinks, key=lambda x: x['Категория'])
    grouped_by_category_drinks = collections.defaultdict(list)
    for category, drinks_in_category in groupby(drinks, lambda x: x['Категория']):
        grouped_by_category_drinks[category] = list(drinks_in_category)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    print(grouped_by_category_drinks)
    rendered_page = template.render(drinks=grouped_by_category_drinks)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
