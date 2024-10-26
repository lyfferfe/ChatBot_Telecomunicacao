import os
from crewai_tools import tool, SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool, FileReadTool, PDFSearchTool
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from ia import get_openai_api_key, get_serper_api_key

openai_api_key = get_openai_api_key()
serper_api_key = get_serper_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SERPER_API_KEY"] = serper_api_key

gpt4o_mini_llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)

# Ferramenta para busca no google
search_tool = SerperDevTool()

# Ferramenta para raspagem de sites
scrape_tool = ScrapeWebsiteTool()

# Especificação de apenas um site para raspagem
docs_scrape_tool = ScrapeWebsiteTool(
    website_url=[
        "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/banda-larga",
        "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/telefonia-movel",
        "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/telefonia-fixa",
        "https://www.gov.br/anatel/pt-br/consumidor/conheca-seus-direitos/tv-por-assinatura"
    ]
)

# Ferramenta para RAG em arquivos PDF. Específica para fazer buscas e extrair partes relevantes em arquivos PDF. 
"""
pdf_search = PDFSearchTool(pdf=[
    "normas/335492.pdf",
    "normas/Anatel - Resolução nº 426, de 9 de dezembro de 2005.pdf",
    "normas/Anatel - Resolução nº 477, de 7 de agosto de 2007.pdf",
    "normas/Anatel - Resolução nº 488, de 3 de dezembro de 2007.pdf",
    "normas/Anatel - Resolução nº 581, de 26 de março de 2012.pdf",
    "normas/Anatel - Resolução nº 632, de 7 de março de 2014.pdf",
    "normas/oficio_12273325.pdf"])
"""
#Definição dos 3 agentes:
identificador = Agent(
    role="Identificador de Problemas",
    goal="Receber a dúvida do cliente e identificar de qual área é o seguinte problema: {problema}",
    backstory="Você está trabalhando na identificação da área do problema do cliente "
              "sobre o problema: {problema}."
              "Você coleta informações atualizadas através de sites e arquivos que ajudam a "
              "identificar a área do problema "
              "e indica qual é o agente especializado no problema "
              "As únicas duas áreas de problemas principais são Jurídico e Técnico "
              "Seu trabalho é a base para que o "
              "agente seguinte escreva possiveis soluções para o problema."
              "Retorne em string a área do problema: juridico ou tecnico. "
              "Se o problema não tiver relação com a área de telecomunicações, retorne 0",
    verbose=True,
    tools=[search_tool, scrape_tool, docs_scrape_tool],
    allow_delegation=False,
    llm=gpt4o_mini_llm
)

juridico = Agent(
    role="Solucionador de problemas da área Jurídica",
    goal="Definir uma solução, com base nas leis da Anatel, para o cliente a fim de resolver seu questionamento: {problema}",
    backstory="Você é um solucionador que recebe um problema de um cliente. "
              "Seu objetivo é dar soluções jurídicas para o problema do cliente."
              "Você também fornece insights objetivos e imparciais "
              "e os apoia com as informações "
              "baseadas nas leis da Anatel e regulamentações da Anatel. "
              "Após análise concluída você escreve um artigo aconselhando o cliente para a solução do seu problema.",
    verbose=True,
    allow_delegation=False,
    llm=gpt4o_mini_llm
)

tecnico = Agent(
    role="Solucionador de problemas da área Técnica",
    goal="Definir uma solução, com base em datasheets sobre o produto ou equipamento definidos pelo cliente para solução do problema: {problema}",
    backstory="Você é um solucionador que recebe um problema de um cliente. "
              "Seu objetivo é dar soluções técnicas para o problema do cliente."
              "Você também fornece insights objetivos e imparciais "
              "e os apoia com as informações "
              "fornecidas pelos datasheets. "
              "Após análise concluída você escreve um artigo aconselhando o cliente para a solução do seu problema.",
    verbose=True,
    allow_delegation=False,
    llm=gpt4o_mini_llm
)

supervisor = Agent(
    role="Supervisar os artigos produzidos pelos agenstes jurídicos e técnicos, corrigindo erros jurídicos, técnicos e gramaticais da lígua portuguesa.",
    goal="Analisar e corrigir possíveis erros cometidos pelo agente jurídico e pelo técnico para solucionar o seguinte problema: {problema}",
    backstory="Você é um solucionador que recebe uma solução para o {problema}."
              "Com essa solução, você deve verificar se ela é coerente com as leis da Anatel e com os datasheets utilizados para consulta."
              "Além disso, é necessário estudar a gramática portuguesa brasileira para verificar se há algum erro."
              "Por fim, retorne um arquivo em markdown com a correção.",
    verbose=True,
    allow_delegation=False,
    llm=gpt4o_mini_llm
)