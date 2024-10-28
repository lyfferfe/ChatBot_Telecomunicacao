from crewai import Task, Crew
from agentes import identificador, juridico, tecnico, supervisor
from tarefas import identificacao, solucao_tecnica, solucao_juridica, supervisar

problema = "Me explique sobre a Resolução Nº 426, de 9 de dezembro de 2005"

crew = Crew(
    agents=[identificador, tecnico, juridico, supervisor],
    tasks=[identificacao, solucao_tecnica, solucao_juridica, supervisar],
    verbose=2
)

resultado = crew.kickoff(inputs={"problema": problema})

print(resultado)
