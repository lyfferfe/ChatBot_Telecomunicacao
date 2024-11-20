from crewai import Task
from agentes import identificador, tecnico, juridico, supervisor

identificacao = Task(
    description=(
        "1. Analisar o {problema} e identificar se ele corresponde a área técnica ou jurídica, caso ele não seja da área de telecomunicações retorne 0.\n"
        "2. Criar uma resposta curta, baseando-se nas respostas da Anatel sobre o problema.\n"
        "3. Envie seu texto para o próximo agente, baseado na sua área de atuação (jurídico ou técnico)."
    ),
    expected_output="Passar o problema para o agente responsável pela área ",
    agent=identificador,
)

solucao_tecnica = Task(
    description=(
        "1. Com base no texto do agente identificador, melhorar o conteúdo do texto com base em datasheets e a documentação necessária sobre o equipamento, para, dessa forma, solucionar o {problema}. \n"
        "2. Através das pesquisas, fazer um texto mais aprofundado, com um máximo de 10 parágrafos, mas dê a preferência por textos curtos e com menos parágrafos, se for possível, que apresente os pontos principais para resolver o problema. \n"
        "3. Após a criação do texto, encaminhá-lo ao agente supervisor."
    ),
    expected_output="Um documento com informações técnicas confiáveis e que respeite as normas da Anatel a fim de ajudar um cliente a resolver seu {problema}",
    agent=tecnico,
)

solucao_juridica = Task(
    description=(
        "1. Com base no texto do agente identificador, melhorar o conteúdo do texto com base nas normas e informações da Anatel (Agência Nacional de Telecomunicações), complementando com as referências de leis, normas e resoluções. Dessa forma, você será capaz de solucionar o {problema} \n"
        "2. Através das pesquisas, fazer um texto mais aprofundado, com um máximo de 10 parágrafo, mas dê a preferência por textos curtos e com menos parágrafos, se for possível, que apresente os pontos principais para resolver o problema. \n"
        "3. Após a criação do texto, encaminhá-lo ao agente supervisor."
    ),
    expected_output="Um documento com informações técnicas confiáveis e que respeite as normas da Anatel a fim de ajudar um cliente a resolver seu {problema}",
    agent=juridico,
)

supervisar = Task(
        description=(
        "1. Após receber o texto anterior, seja do agente técnico ou jurídico, você deve revisar todo o texto produzido a fim de encaminhar a melhor solução para o cliente resolver o seu problema: {problema}. \n"
        "2. Verificar se o texto está claro, objetivo e se está de acordo com as normas da Anatel e com as informações dos datasheets. \n"
        "3. Corrigir possíveis erros gramaticais e de concordância. \n"
        "4. Após a revisão, encaminhar o texto para o cliente."
        ),
        expected_output="Uma resposta com soluções claras e concisas para o problema do cliente, baseadas nas normas da Anatel e nos datasheets dos equipamentos.",
        agent=supervisor,
)

