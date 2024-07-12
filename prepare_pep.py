import zipfile
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import os


# Função para encontrar o primeiro arquivo com uma determinada extensão em um diretório
def find_first_file_with_extension(directory, extension):
    for file in os.listdir(directory):
        if file.endswith(extension):
            return os.path.join(directory, file)
    return None


# Função para extrair e processar o arquivo CSV de dentro do ZIP
def process_zip_to_parquet(zip_file_path, new_column_names, parquet_file_path, encoding='latin1'):
    # Extrair o conteúdo do arquivo ZIP
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Diretório onde o ZIP foi extraído
        extraction_path = os.path.dirname(zip_file_path)

        # Listar todos os arquivos dentro do ZIP
        csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
        if not csv_files:
            raise FileNotFoundError("Nenhum arquivo CSV encontrado no ZIP.")

        # Selecionar o primeiro arquivo CSV encontrado
        csv_file_name = csv_files[0]

        # Extrair o arquivo CSV para o diretório de extração
        zip_ref.extract(csv_file_name, extraction_path)

        # Caminho completo do arquivo CSV extraído
        csv_file_path = os.path.join(extraction_path, csv_file_name)

        # Ler o CSV em um DataFrame, sem cabeçalho
        dtype_options = {
            4: str  # Especifica que a coluna no índice 4 (quinta coluna) deve ser tratada como string
        }
        df = pd.read_csv(csv_file_path, header=0, encoding=encoding, on_bad_lines='skip', delimiter=';', dtype=dtype_options)

        # Adicionar novos nomes de colunas
        df.columns = new_column_names
        #
        # # Converter o DataFrame para um Table do PyArrow
        table = pa.Table.from_pandas(df)
        #
        # # Salvar o DataFrame como um arquivo Parquet
        pq.write_table(table, parquet_file_path)


# Caminho do diretório onde o arquivo ZIP foi baixado
download_directory = os.getenv('RUNNER_TEMP') + '/downloads_pep'
parquet_directory = os.getenv('RUNNER_TEMP') + '/pep-parquet'

# Encontrar o primeiro arquivo ZIP no diretório
zip_file_path = find_first_file_with_extension(download_directory, '.zip')
if zip_file_path is None:
    raise FileNotFoundError("Nenhum arquivo ZIP encontrado no diretório de downloads.")

# Novos nomes para as colunas
new_column_names = ['CPF', 'Nome_PEP', 'Sigla_Funcao',
                    'Descricao_Funcao', 'Nivel_Funcao', 'Nome_Orgao', 'Data_Inicio_Exercicio', 'Data_Fim_Exercicio', 'Data_Fim_Carencia']  # Adicione todos os nomes de colunas necessários
# Caminho para salvar o arquivo Parquet
parquet_file_path = os.path.join(download_directory, 'pep.parquet')

# Chamar a função para processar o arquivo
process_zip_to_parquet(zip_file_path, new_column_names, parquet_file_path)