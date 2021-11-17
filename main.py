# Importando as dependências necessárias.
import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient
import pymongo

def get_database():
    from pymongo import MongoClient
    import pymongo

    # Prover a url de conexão do atlas para usar com o pymongo
    CONNECTION_STRING = "mongodb+srv://[usuario]:[senha]@[dominio]/[database]?retryWrites=true&w=majority"

    # Criar a conexão usando o MongoClient. Pode ser feita importando o MongoClient ou usando pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Criar o banco de dados ou usar o seguinte banco.
    return client['scrapper_database']

dbname = get_database()
scrapper_collection = dbname["scrapper_collection"]

# Definindo nossa url alvo.
url = "https://www.dicio.com.br/vida/"

# Baixando a página
page = requests.get(url)

# Formatando a página com BeautifulSoup4
beautiful_page = BeautifulSoup(page.text, 'html.parser')

# Capturando o elemento que possue a definição da palavra.
definition = beautiful_page.find(attrs={'itemprop': 'description'})

str_definition = []

# Iterando sobre todos os elementos do tipo span encontrados.
for definition_i in definition.find_all('span'):
    try:
        element_class = definition_i['class'][0]
    except:
        element_class = ""
    
    # Evitando os elementos que possuem a classe tag, para evitar repetições.
    if element_class != 'tag':
        str_definition.append(definition_i.get_text().strip())

# Nem sempre vamos ter disponível exemplos para todas as frases. Logo vamos usar um bloco try catch.
try:
    # Buscar o elemento H3 com a classe 'tit-exemplo', onde os exemplos estarão na sua div pai. por isso o uso do .parent
    example = beautiful_page.find(attrs={'class': 'tit-exemplo'}).parent.find_all(attrs={'class': 'frase'})
    
    str_example = []

    # Iterar sobre os exemplos.
    for example_i in example:
        str_example.append(example_i.get_text().strip())
except:
    example = "",
    str_example = [],

## Valor com o link da fonte das informações.
source = url

# Criando um objeto com todas as informações.
resolve = {
    "word": "amor",
    "definition": str_definition,
    "source": source,
    "example": str_example,
    "html": {
        "definition": str(definition),
        "example": str(example),
    }
}

# Escrevendo em um objeto tipo json guardando o nosso objeto.
f = open("significado_de_amor.json", "a")

f.write(str(resolve).replace('"', "`").replace("'", '"').replace("`", "'"))

f.write(',\n')

f.close()

# Salvar o objeto em banco de dados.
scrapper_collection.insert_one(resolve)