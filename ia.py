# Função para ler a chave de API do arquivo
def get_openai_api_key():
    with open('API_alunos_OpenAI.txt', 'r') as file:
        return file.read().strip()

# Função para ler a chave da API Serper
def get_serper_api_key():
    with open('API_Serper.txt', 'r') as file:
        return file.read().strip()