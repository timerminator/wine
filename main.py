from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import pprint
from itertools import groupby
import collections

year_of_birth = 1920
this_year = datetime.datetime.now().year
years = this_year - year_of_birth

drinks = pandas.read_excel('wine3.xlsx', na_values=['N/A', 'NA'], keep_default_na=False).to_dict(orient='record')
drinks = sorted(drinks, key=lambda x: x['Категория'])
drinks_groupby_category = collections.defaultdict(list)
for category, drinks_in_category in groupby(drinks, lambda x: x['Категория']):
    drinks_groupby_category[category] = list(drinks_in_category)
pprint.pprint(drinks_groupby_category)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(drinks=drinks_groupby_category)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
