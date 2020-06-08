import csv
import datetime

File = 'FACTURACION.csv'
def reader():
    log("inicializando lectura de archivo")
    listado_de_facturas= []
    with open(File) as csv_file:
        csv_reader= csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            listado_de_facturas.append(formatear(row))
    log("finalizando lectura de archivo")
    return listado_de_facturas      
    
                
def formatear(row):
    formato= {
             'DocNro': DocNro(row), 
             'Fecha': row['FECHA'],
             'Servdesde': row['SERVDESDE'],
             'Servhasta': row['SERVHASTA'],
             'ImpNeto': ImpNeto(row),
             'ImpIVA': Iva(row),
             'Total': Total(row),
             'FchVtoPago': vtopago()
            }
    return formato
    
def DocNro(row):
    doc = row['CLIENTE']
    log("formateando nro documento "+doc)
    DocNro = doc.split("1-")[1]
    log("Numero Formateado "+DocNro)
    return int(DocNro)
def ImpNeto(row):
    importe = row['NETONOGRAVADO']
    return float(importe)
def Iva(row):
    iva = row['IVA']
    return float(iva)
def Total(row):
    Total = row['TOTAL']
    return float(Total)

def log(cadena):
    True
    print(cadena)
    
def vtopago():
    hoy = datetime.datetime.today()
    ven = hoy + datetime.timedelta(days=4)
    vence = str(ven).rsplit( )[0]
    vencio= vence.split('-')
    vencimiento = vencio[0] + vencio[1] + vencio[2] 
    log("fecha vencimiento de pago "+vencimiento)
    return vencimiento

