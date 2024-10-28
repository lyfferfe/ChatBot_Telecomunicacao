from crewai import Task, Crew
from agentes import identificador, juridico, tecnico, supervisor
from tarefas import identificacao, solucao_tecnica, solucao_juridica, supervisar

problema = "Minha pia está entupida"

crew = Crew(
    agents=[identificador, tecnico, juridico, supervisor],
    tasks=[identificacao, solucao_tecnica, solucao_juridica, supervisar],
    verbose=2
)

resultado = crew.kickoff(inputs={"problema": problema})

print(resultado)
