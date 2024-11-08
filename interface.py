import tkinter as tk
from IPython.display import Markdownfrom tkinter import scrolledtext

from crewai import Task, Crew
from agentes import identificador, juridico, tecnico, supervisor
from tarefas import identificacao, solucao_tecnica, solucao_juridica, supervisar

crew = Crew(
    agents=[identificador, tecnico, juridico, supervisor],
    tasks=[identificacao, solucao_tecnica, solucao_juridica, supervisar],
    verbose=2
)

# Função para enviar mensagem
def send_message():
    user_message = user_input.get()
    if user_message.strip() != "":
        # Habilita a área de chat para inserir texto
        chat_area.config(state="normal")
        
        # Exibe a mensagem do usuário à direita
        chat_area.insert(tk.END, f"Você: {user_message}\n", "user")
        
        # Limpa o campo de entrada de texto
        user_input.delete(0, tk.END)
        
        # Resposta da IA (substitua por uma resposta real se disponível)
        bot_response = crew.kickoff(inputs={"problema": user_message})
        
        # Exibe a resposta da IA à esquerda
        chat_area.insert(tk.END, f"IA: {(bot_response)}\n", "bot")
        
        # Rola o chat para o final, garantindo que a última mensagem apareça
        chat_area.yview(tk.END)
        
        # Desabilita a área de chat para impedir edições
        chat_area.config(state="disabled")

# Criação da janela principal
window = tk.Tk()
window.title("Chat com IA")
window.geometry("400x500")
window.config(bg="#f0f2f5")

# Cabeçalho
header = tk.Label(window, text="Conversa com IA", bg="#4a90e2", fg="white", font=("Arial", 16, "bold"))
header.pack(pady=10, fill=tk.X)

# Área de chat com rolagem
chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 12), bg="#ffffff", state="disabled")
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Definindo estilos de tag para alinhar as mensagens à direita e à esquerda
chat_area.tag_config("user", justify="right", foreground="#333333", background="#f0f2f5", font=("Arial", 12, "italic"))
chat_area.tag_config("bot", justify="left", foreground="#4a4a4a", background="#e5e5e5", font=("Arial", 12))

# Caixa de entrada de texto
user_input = tk.Entry(window, font=("Arial", 12))
user_input.pack(padx=10, pady=5, fill=tk.X)

# Botão de envio
send_button = tk.Button(window, text="Enviar", command=send_message, bg="#4a90e2", fg="white", font=("Arial", 12))
send_button.pack(padx=10, pady=10)

# Evento de teclado para enviar com "Enter"
window.bind("<Return>", lambda event: send_message())

# Função principal do loop
window.mainloop()
