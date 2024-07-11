# app/routes.py

from flask import Flask, request, jsonify
from config import Config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config.from_object(Config)

# Endereços de email para onde os emails serão enviados
RECIPIENT_EMAIL = "drigocamposs@gmail.com"
CC_EMAIL = "rodrigo.rodrigues@sou.inteli.edu.br"

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()

    # Extrair dados do formulário
    nome = data.get("nome", "")
    empresa = data.get("empresa", "")
    funcionarios = data.get("funcionarios", "")
    celular = data.get("celular", "")
    email = data.get("email", "")
    mais = data.get("mais", "")

    sender_email = app.config['SMTP_USERNAME']
    sender_name = "Website Contact Form"
    subject = "Novo envio de formulário de contato"
    html_content = f"""
    <html>
    <head></head>
    <body>
        <p><strong>Nome:</strong> {nome}</p>
        <p><strong>Empresa:</strong> {empresa}</p>
        <p><strong>Número de Funcionários:</strong> {funcionarios}</p>
        <p><strong>Celular:</strong> {celular}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Mais Informações:</strong> {mais}</p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} <{sender_email}>"
    msg['To'] = RECIPIENT_EMAIL
    msg['Cc'] = CC_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    recipients = [RECIPIENT_EMAIL, CC_EMAIL]

    try:
        with smtplib.SMTP(app.config['SMTP_SERVER'], app.config['SMTP_PORT']) as server:
            server.starttls()
            server.login(app.config['SMTP_USERNAME'], app.config['SMTP_PASSWORD'])
            server.sendmail(sender_email, recipients, msg.as_string())
            return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
