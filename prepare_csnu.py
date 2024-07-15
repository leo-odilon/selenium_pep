import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
import os


# Função para encontrar o primeiro arquivo com uma determinada extensão em um diretório
def find_first_file_with_extension(directory, extension):
    for file in os.listdir(directory):
        if file.endswith(extension):
            return os.path.join(directory, file)
    return None

# Caminho do arquivo ZIP
download_directory = os.getenv('RUNNER_TEMP') + '/downloads_csnu'
parquet_directory = os.getenv('RUNNER_TEMP') + '/csnu-parquet'

xml_file_path = find_first_file_with_extension(download_directory, '.xml')
if xml_file_path is None:
    raise FileNotFoundError("Nenhum arquivo XML encontrado no diretório de downloads.")

# Função para extrair o valor de um elemento XML
def get_element_text(element, path):
    elem = element.find(path)
    return elem.text if elem is not None else ""

# Carregar e parsear o arquivo XML extraído
tree = ET.parse(f'{xml_file_path}')
root = tree.getroot()

# Lista para armazenar os dados extraídos
data_individuals = []
data_entities = []

# Extrair dados dos indivíduos
for individual in root.findall('.//INDIVIDUAL'):
    data = {
        "DATAID": get_element_text(individual, 'DATAID'),
        "FIRST_NAME": get_element_text(individual, 'FIRST_NAME'),
        "SECOND_NAME": get_element_text(individual, 'SECOND_NAME'),
        "THIRD_NAME": get_element_text(individual, 'THIRD_NAME'),
        "UN_LIST_TYPE": get_element_text(individual, 'UN_LIST_TYPE'),
        "REFERENCE_NUMBER": get_element_text(individual, 'REFERENCE_NUMBER'),
        "LISTED_ON": get_element_text(individual, 'LISTED_ON'),
        "NATIONALITY": get_element_text(individual, 'NATIONALITY/VALUE'),
        "LIST_TYPE": get_element_text(individual, 'LIST_TYPE/VALUE')
    }
    data_individuals.append(data)

# Extrair dados das entidades
for entity in root.findall('.//ENTITY'):
    data = {
        "DATAID": get_element_text(entity, 'DATAID'),
        "FIRST_NAME": get_element_text(entity, 'FIRST_NAME'),
        "SECOND_NAME": "",
        "THIRD_NAME": "",
        "UN_LIST_TYPE": get_element_text(entity, 'UN_LIST_TYPE'),
        "REFERENCE_NUMBER": get_element_text(entity, 'REFERENCE_NUMBER'),
        "LISTED_ON": get_element_text(entity, 'LISTED_ON'),
        "NATIONALITY": "",
        "LIST_TYPE": ""
    }
    data_entities.append(data)

# Converter listas de dados em DataFrames
df_individuals = pd.DataFrame(data_individuals)
df_entities = pd.DataFrame(data_entities)

# Concatenar os DataFrames
df_final = pd.concat([df_individuals, df_entities], ignore_index=True)

# Salvar em formato Parquet
df_final.to_parquet(f'{parquet_directory}/csnu.parquet', engine='pyarrow')

print("Dados extraídos e salvos no arquivo output.parquet")
