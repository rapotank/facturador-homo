import certificados
import zeep
import datetime
import xmltodict

wsdlAFIP = 'https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL'
wsdlLOGIN='https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl'

def Generarcertificadoauth(id):
    
    certificados.generarCMS(id)
    certificado = certificados.get_certificado()
   
    client = zeep.Client(wsdl=wsdlLOGIN)
    
    response = client.service.loginCms(in0=certificado)

    certificados.save_authcredentials(id,response)
    
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
def ParamGetTiposDoc():
    client = zeep.Client(wsdl=wsdlAFIP)
    auth_soap = Get_auth()
    
    llamada = client.service.FEParamGetTiposDoc(Auth=auth_soap)
    
    print(llamada)
def ParamGetPtosVenta():
    client = zeep.Client(wsdl=wsdlAFIP)
    auth_soap = Get_auth()
    
    llamada = client.service.FEParamGetPtosVenta(Auth=auth_soap)
    
    print(llamada)
def TypeFECAEDetRequest():
    client = zeep.Client(wsdl=wsdlAFIP)
    auth_soap = Get_auth()
    
    llamada = client.type_factory('ns0').FECAEDetRequest()
    print(llamada)
def FECompUltimoAutorizado():
    client = zeep.Client(wsdl=wsdlAFIP)
    auth_soap = Get_auth()
    
    llamada = client.service.FECompUltimoAutorizado(Auth=auth_soap, PtoVta=2, CbteTipo=6)
    CbteNro = llamada.CbteNro
    return(CbteNro)



ParamGetPtosVenta()
print(FECompUltimoAutorizado())