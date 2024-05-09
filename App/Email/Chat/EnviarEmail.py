import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox
import datetime
import sys
sys.path.append(".")
from App.Modules.LerContent import ler_arquivo

data_hora_atual = datetime.datetime.now()
data_hora_formatada = data_hora_atual.strftime("%Y-%m-%d %H:%M:%S")

def substituir_variaveis(template, variaveis):
    for chave, valor in variaveis.items():
        # Converter o valor para uma string se não for None
        if valor is not None:
            valor = str(valor)
        else:
            valor = ""
        template = template.replace('{{' + chave + '}}', valor)
    return template


def enviarEmail(tipo, template, destinatario, assunto, mensagem, remetente, senha, smtp, porta, _prt=None, aluno=None, _ctf=None, _key=None, _context=None):
    
    print(tipo)
    print(template)
    print(destinatario)
    print(assunto)
    print(mensagem)
    print(remetente)
    # Configuração do servidor SMTP
    if tipo == "Aluno":
        # Se aluno não estiver vazio, substituir as variáveis no template
        if aluno:
            caminho_template = ler_arquivo(template)
            template_html = substituir_variaveis(caminho_template, aluno)
        else:
            # Se aluno estiver vazio, usar o template original
            template_html = ler_arquivo(template)
        
        # Configuração da mensagem de e-mail
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(template_html, 'html'))
        
        # Inicialização do servidor SMTP e envio do e-mail
        try:
            server = smtplib.SMTP(smtp, porta)
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
            server.quit()
            
            # Exibir mensagem de sucesso
            messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!")
        except Exception as e:
            # Exibir mensagem de erro se ocorrer um problema no envio do e-mail
            messagebox.showerror("Erro", f"Ocorreu um erro ao enviar o e-mail: {str(e)}")

# Exemplo de como chamar a função enviar_email:
# enviar_email(tipo, template, destinatario, assunto, mensagem, remetente, senha, smtp, porta, tls, aluno)
