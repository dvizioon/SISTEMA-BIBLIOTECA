import tkinter as tk
import webbrowser

# Função para abrir links
def open_link(event):
    url = event.widget.get("current linestart", "current lineend")
    webbrowser.open(url)

# Cria a janela principal
# root = tk.Tk()
# root.title("Página de Ajuda")
# root.geometry("800x600")


def scriptSysHelp(frame):
    # Cria um widget de texto
    text_widget = tk.Text(frame, wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True)

    # Insere o conteúdo HTML na forma de texto formatado
    html_content = """
    Bem-vindo à Página de Ajuda

    Aqui você encontrará informações úteis sobre como usar o nosso aplicativo:

    - Como começar: https://github.com/dvizioon/SISTEMA-BIBLIOTECA/como-comecar
    - Como criar uma nova conta: https://github.com/dvizioon/SISTEMA-BIBLIOTECA/criar-conta
    - Como usar os recursos avançados:https://github.com/dvizioon/SISTEMA-BIBLIOTECA/recursos-avancados

    Para mais informações, chame o suporte no GMAIL: danielprojetos@gmail.com
    """

    # Insere o conteúdo HTML no widget de texto
    text_widget.insert(tk.END, html_content)

    # Configura os links para serem clicáveis
    start = 1.0
    while True:
        start_link = text_widget.search("http", start, stopindex=tk.END)
        if not start_link:
            break
        end_link = text_widget.search(" ", start_link, stopindex=tk.END)
        if not end_link:
            end_link = tk.END
        text_widget.tag_add("link", start_link, end_link)
        text_widget.tag_config("link", foreground="blue", underline=True)
        text_widget.tag_bind("link", "<Button-1>", open_link)
        start = end_link

    # Impede que o widget de texto seja editável
    text_widget.configure(state=tk.DISABLED)

 


# # root.mainloop()
