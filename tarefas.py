from crewai import Task
from agentes import identificador, tecnico, juridico, supervisor

identificacao = Task(
    description=(
        "1. Identificar qual é a área do problema recebido "
            "e passar para o agente responsável pela área o  seguinte problema: {problema}.\n"
    ),
    expected_output="Passar o problema para o agente responsável pela área ",
    agent=identificador,
)

solucao_tecnica = Task(
    description=(
        "1. De acordo com o problema "
        "crie um documento com soluções para o problema: {problema}.\n"
		"2. As seções/subtítulos devem ser nomeados "
            "de maneira envolvente.\n"
    "3. Caso o problema não seja de sua área não faça nada"
    ),
    expected_output="Caso o problema seja de sua área, envie esse documento para o Supervisor de artigos",
    agent=tecnico,
)

solucao_juridica = Task(
    description=(
        "1. De acordo com o problema "
        "crie um documento com soluções para o problema: {problema}.\n"
		"2. As seções/subtítulos devem ser nomeados "
            "de maneira envolvente.\n"
    "3. Caso o problema não seja de sua área não faça nada"
    ),
    expected_output="Caso o problema seja de sua área, envie esse documento para o Supervisor de artigos",
    agent=juridico,
)

supervisar = Task(
        description=(
        "1. Corrigir possíveis erros gramaticais do documento sobre o problema: {problema}\n"
        "2. Corrigir também erros jurídicos e técnicos \n"
        "3. Caso o problema não seja da área de Telecomunicações apague o texto anterior do documento e escreva que o problema está fora do escopo no documento"
        "4. Preze por fazer resumos em um único parágrafo de no máximo 6 linhas."
        ),
        expected_output="Uma resposta com soluções bem escrito, em português do Brasil, "
            "com no máximo 10 linhas. Ao final, as referências utilizadas no documento.",
        agent=supervisor,
)

