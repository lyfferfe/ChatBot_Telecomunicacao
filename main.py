import os
from crewai_tools import tool, SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool, FileReadTool, PDFSearchTool
from crewai_tools import tool
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from agentes import identificador, juridico, tecnico

agentes = {
    "juridico": juridico,
    "tecnico": tecnico
}

identificacao = Task(
    description=(
        "1. Identificar qual é a área do problema recebido "
            "e retornar juridico ou tecnico de acordo com o seguinte problema: {problema}.\n"
        "2. Retorne 0 caso o problema não tenha a ver com a área de Telecomunicações"
    ),
    expected_output="Uma string dizendo juridico ou tecnico ",
    agent=identificador,
)

equipe_identificacao = Crew(
    agents=[identificador],
    tasks=[identificacao],
    verbose=2
)

problema = "Meu Wifi não está funcionando"
area = equipe_identificacao.kickoff(inputs={"problema": problema})

if area != "0":
    solucionador = Task(
        description=(
            "1. De acordo com o problema "
            "crie um documento com soluções para o problema: {problema}.\n"
            "2. As seções/subtítulos devem ser nomeados "
                "de maneira envolvente.\n"
        ),
        expected_output="Um documento com soluções bem escrito, em português do Brasil, "
            "com cada seção contendo 3 ou 4 parágrafos.",
        agent=agentes[area],
    )

    solucao = Crew(
        agents=[agentes[area]],
        tasks=[solucionador],
        verbose=2
    )

    resultado_solucao = solucao.kickoff(inputs={"problema": problema})
else:
    resultado_solucao = "Problema não relacionado com a área de telecomunicações"

print(resultado_solucao)