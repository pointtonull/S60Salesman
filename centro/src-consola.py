#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import smtplib

def enviar(mensaje):
    fromaddr = '"MINUMERO" <MINUMERO@sms.cmail.com.ar>"'
    toaddrs = ["TOADDRS"]
    subject = "src-Milva"

    mensaje = mensaje + "CTI MOVIL SMS E-MAIL\n"

    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (\
            fromaddr,\
            ", ".join(toaddrs),\
            subject,\
            mensaje\
           ))

    server = smtplib.SMTP("SMTPSERVER")
    server.set_debuglevel(0)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


def main():
    print("CLI de src:")
    entrada = sys.stdin.readline()
    while (entrada):
        enviar(entrada)
        entrada = sys.stdin.readline()

if __name__ == "__main__":
     main() 
