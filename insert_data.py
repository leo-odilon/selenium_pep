import sys
import pandas as pd
import requests
import json
import pandasql as psql


def read_parquet(file_path):
    return pd.read_parquet(file_path)


def query_data(df, query):
    return psql.sqldf(query, locals())


def dataframe_to_json(df):
    return df.to_json(orient='records')


def send_post_request(api_url, json_data, headers):
    response = requests.post(api_url, data=json.dumps(json_data), headers=headers)
    return response


def main(parquet_file_path, query, api_url, auth_token, chunk_size=None):
    # Ler o arquivo Parquet
    df = read_parquet(parquet_file_path)

    # Realizar a consulta
    result_df = query_data(df, query)

    # Converter o DataFrame resultante em JSON
    json_data = json.loads(dataframe_to_json(result_df))

    # Estrutura do JSON final
    json_payload = {"verificationList": json_data}
    # print(json_payload)
    headers = {
        "Authorization": f"Bearer 00Dcb00000016WX!AQEAQOl6ZWNZ8AX.6P3z6ki5Yue4R5vXK6jEkV5DNvtqwpYRRNn1zXknew.lKkUi_oAlm4Vo7Hve8dQuVoKlcOzpVBMi7hZL",
        "Content-Type": "application/json"
    }

    # Enviar o JSON em partes (chunks) ou completo
    if chunk_size:
        total_chunks = (len(json_data) + chunk_size - 1) // chunk_size
        for i in range(total_chunks):
            start = i * chunk_size
            end = start + chunk_size
            chunk = json_data[start:end]
            chunk_payload = {"verificationList": chunk}
            response = send_post_request(api_url, chunk_payload, headers)
            print(f"Enviando chunk {i + 1}/{total_chunks}: Status {response.status_code}")
            if response.status_code != 200:
                print(f"Erro: {response.text}")
                break
    else:
        response = send_post_request(api_url, json_payload, headers)
        print(f"Enviando JSON completo: Status {response.status_code}")
        if response.status_code != 200:
            print(f"Erro: {response.text}")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python script.py <caminho_parquet> <query> <api_url> <auth_token> [chunk_size]")
        sys.exit(1)

    parquet_file_path = sys.argv[1]
    query = sys.argv[2]
    api_url = sys.argv[3]
    auth_token = sys.argv[4]
    chunk_size = int(sys.argv[5]) if len(sys.argv) > 5 else None

    main(parquet_file_path, query, api_url, auth_token, chunk_size)
