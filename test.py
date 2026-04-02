import smtplib

server = smtplib.SMTP_SSL("smtp.hostinger.com", 465)
server.login("admin@cr-ai.cloud", "Crai@1357")
print("Login OK")
server.quit()