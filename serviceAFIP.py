#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:53:48 2020

@author: matias
"""

import datetime
import zeep
import certificados
import xmltodict
import LectorDeArchivo
import Consulta

wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'
wsdlAFIP = 'https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL'
wsdlLOGIN='https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl'

# Funcion que genera el certificado con el id de llamada obtenido en certificados.py get_id   
def Generarcertificadoauth(id):
    
    certificados.generarCMS(id)
    certificado = certificados.get_certificado()
   
    client = zeep.Client(wsdl=wsdlLOGIN)
    
    response = client.service.loginCms(in0=certificado)

    certificados.save_authcredentials(id,response)

# funcion que chequea que el certificado no este vencido y en caso de que lo este, ejecuta la funcion para generar uno nuevo
def Get_auth():
    response = certificados.get_authcredentials()
    #print(response)
    xpars = xmltodict.parse(response) 
    exptime = xpars['loginTicketResponse']['header']['expirationTime']  

    date_str = exptime
    date_str = date_str.split('.')
    date_time_obj = datetime.datetime.strptime(date_str[0],"%Y-%m-%dT%H:%M:%S")
    #print(date_time_obj)
    today = datetime.datetime.today()
    #print(today)
    if date_time_obj < today:
        id = certificados.get_id()
        Generarcertificadoauth(id)
        Get_auth()
    else:
            cuit = 30715054120
            token = xpars['loginTicketResponse']['credentials']['token']  
            sign = xpars['loginTicketResponse']['credentials']['sign']  
            auth ={
                    'Token': token,
                    'Sign': sign,
                    'Cuit': cuit 
                }
            
            return auth   
def fecab_request(cantidad):
    client = zeep.Client(wsdl=wsdlAFIP)
    fecab_request_type = client.get_type('ns0:FECAECabRequest')
    fecab_request = fecab_request_type(
        CantReg= cantidad,
        PtoVta= 2,
        CbteTipo= 6
    )
    return fecab_request



def set_iva():
     
    client = zeep.Client(wsdl=wsdlAFIP)
    array_iva = client.get_type('ns0:ArrayOfAlicIva')
     
    alic = client.get_type('ns0:AlicIva')
    
    iva = array_iva(alic(Id=5,BaseImp=diccionario['ImpNeto'], Importe=diccionario['ImpIVA']))
    return iva


def formato_fecae_Det_Request(cbte, diccionario):
  
    # "El campo  'Importe Total' ImpTotal, debe ser igual  a la 
    #suma de ImpTotConc + ImpNeto + ImpOpEx + ImpTrib + ImpIVA."
    client = zeep.Client(wsdl=wsdlAFIP)
    fecae_det = client.type_factory('ns0').FECAEDetRequest()
    fecae_det.Concepto = 2
    fecae_det.DocTipo = 96
    fecae_det.DocNro = diccionario['DocNro']
    fecae_det.CbteDesde = cbte
    fecae_det.CbteHasta = cbte
    fecae_det.CbteFch = diccionario['Fecha']
    fecae_det.ImpTotal = diccionario['Total']
    fecae_det.ImpTotConc = 0
    fecae_det.ImpNeto = diccionario['ImpNeto']
    fecae_det.ImpOpEx = 0
    fecae_det.ImpIVA = diccionario['ImpIVA']
    fecae_det.ImpTrib = 0
    fecae_det.FchServDesde=diccionario['Servdesde']
    fecae_det.FchServHasta=diccionario['Servhasta']
    fecae_det.FchVtoPago=diccionario['FchVtoPago']
    fecae_det.MonId="PES"
    fecae_det.MonCotiz=1
    fecae_det.CbtesAsoc=None 
    fecae_det.Tributo=None
    fecae_det.Iva=set_iva()
    fecae_det.Opcionales=None
    #     'Compradores'
    
    
    
    
    return fecae_det
    
   
    
def formato_fecae_request(cantidad_registros, diccionario_fecaereq):
    client = zeep.Client(wsdl=wsdlAFIP)
   
    fecae_request = client.get_type('ns0:FECAERequest')
  
    
    array_fecae= client.get_type('ns0:ArrayOfFECAEDetRequest')
    
    
    retorno= fecae_request(FeCabReq = fecab_request(cantidad_registros),
                           FeDetReq = array_fecae(diccionario_fecaereq))
    
    
    print(retorno)
    return retorno

def callService_FECAESolicitar(cantidad_registros, diccionario_fecaereq):
    client = zeep.Client(wsdl=wsdlAFIP)
    auth_soap = Get_auth()
    fecae_request = formato_fecae_request(cantidad_registros, diccionario_fecaereq)

    
    retorno = client.service.FECAESolicitar(Auth=auth_soap, FeCAEReq=fecae_request)
    archivo = open("facturacion.txt", 'w')  
    archivo.write(str(retorno))
    archivo.close()       
    print("respuesta")
    print(retorno)

listado = LectorDeArchivo.reader()
ArrayOfFECAEDetReq = []
UltimoCbte=Consulta.FECompUltimoAutorizado()
cbte = int(UltimoCbte)
for diccionario in listado:
     cbte+=1 
     ArrayOfFECAEDetReq.append(formato_fecae_Det_Request(cbte,diccionario))
# callService_FECAESolicitar(len(listado),ArrayOfFECAEDetReq)
# 


#ArrayOfFECAEDetReq.append(formato_fecae_Det_Request(3,[]))
#print(ArrayOfFECAEDetReq)
    
callService_FECAESolicitar(len(ArrayOfFECAEDetReq),ArrayOfFECAEDetReq)
# 
# formato_fecae_Det_Request([])