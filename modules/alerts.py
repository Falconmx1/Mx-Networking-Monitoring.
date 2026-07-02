import smtplib
import requests
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertSystem:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def send_alert(self, message):
        """Envía una alerta por todos los canales configurados"""
        if self.config['alerts']['email']['enabled']:
            self._send_email_alert(message)
        if self.config['alerts']['telegram']['enabled']:
            self._send_telegram_alert(message)

    def _send_email_alert(self, message):
        """Envía alerta por correo electrónico"""
        email_config = self.config['alerts']['email']
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config['sender']
            msg['To'] = email_config['recipient']
            msg['Subject'] = "ALERTA - Monitoreo de Red"
            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(email_config['smtp_server'], email_config['port'])
            server.starttls()
            server.login(email_config['sender'], email_config['password'])
            server.send_message(msg)
            server.quit()
            print("Alerta enviada por correo.")
        except Exception as e:
            print(f"Error al enviar correo: {e}")

    def _send_telegram_alert(self, message):
        """Envía alerta por Telegram"""
        tg_config = self.config['alerts']['telegram']
        try:
            url = f"https://api.telegram.org/bot{tg_config['bot_token']}/sendMessage"
            payload = {
                'chat_id': tg_config['chat_id'],
                'text': f"🚨 *ALERTA DE RED* 🚨\n\n{message}",
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("Alerta enviada por Telegram.")
            else:
                print(f"Error al enviar a Telegram: {response.text}")
        except Exception as e:
            print(f"Error al enviar a Telegram: {e}")
