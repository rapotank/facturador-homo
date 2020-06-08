# -*- coding: utf-8 -*-


# openssl genrsa -out FacturaKey.key 2048


from OpenSSL import crypto

import datetime
import subprocess


def generarPrivateKey():
    keypath = "FacturaKey.key"
    
    k = crypto.PKey()
    
    
    print("Generating Key Please standby")
    k.generate_key(crypto.TYPE_RSA, 2048)
    out =str(crypto.dump_privatekey(crypto.FILETYPE_PEM, k), 'utf8')
    f = open(keypath, "w")
    f.write(out)
    f.close()


def generarCMS(id_unico):

    # id_unico="202009"
    
    x = datetime.datetime.now()
    t = x + datetime.timedelta(days = 1) 
    genTime  = x.strftime("%Y-%m-%d")+"T"+x.strftime("%H:%M:%S")
    expTime= t.strftime("%Y-%m-%d")+"T"+t.strftime("%H:%M:%S")
    
   
    out=" <loginTicketRequest>"
    out+=" <header>"
    out+="<uniqueId>"+str(id_unico)+"</uniqueId>"
    out+="<generationTime>"+genTime+"</generationTime>"
    out+="<expirationTime>"+expTime+"</expirationTime>"
    out+="</header>"
    out+="<service>wsfe</service>"
    out+="</loginTicketRequest>"
    
  
    XML = "MiLoginTicketRequest.xml"
    f = open(XML, "w")
    f.write(out)
    f.close()
    
    out_command = "openssl cms -sign -in MiLoginTicketRequest.xml -out MiLoginTicketRequest.xml.cms -signer Facturador.pem -inkey FacturaKey.key -nodetach -outform PEM"
    out_command = out_command.split(" ")
    subprocess.run(out_command)
def save_authcredentials(id, xml_auth):
    xml = "myauthcredentials.xml"
    f = open(xml,"w")
    f.write(xml_auth)
    f.close()
    
    file_id = "myauthid.txt"
    f = open(file_id,"w")
    f.write(str(id))
    f.close()

def get_authcredentials():
    XML_auth= "myauthcredentials.xml"
    f = open(XML_auth, "r")
    Lines = f.readlines() 

    retorno =""
    for line in Lines: 
        retorno+=line   
    f.close()
    
    retorno.replace('\n','')
    return retorno
    

def get_certificado():
    XMLCMS= "MiLoginTicketRequest.xml.cms"
    f = open(XMLCMS, "r")
    Lines = f.readlines() 
    
    retorno =""
    for line in Lines: 
        line_aux=line#.decode("utf-8") 
        if "CMS---" not in line_aux:          
           retorno +=line_aux.replace('\n', '')
    f.close()
    
    retorno.replace('\n','')
    return retorno
#Funcion que obtiene el id del archivo que lo contiene, aumenta en 1 y lo guarda.
def get_id():
    idfile = open('myauthid.txt', 'r+')
    numero_id = idfile.read()
    id = int(numero_id) + 1
    idfile.seek(0)
    idfile.write(str(id))
    idfile.close()
    return id
def log(cadena):
    True
    print(cadena)