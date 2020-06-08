import csv

fecha = "Fecha"
comercio = "Comercio"
dni = "DNI"
total = "Total"
nombre = "Nombre"
csv_dic={fecha:[], comercio:[], dni:[], total:[], nombre:[]}


def generarFactura(detalleFacT):
    print("Generando factura de : "+detalleFacT[7])
    print("con los siguientes datos :")
    print (detalleFacT )
    print("---------------------------")
    
    
with open('Nominales.csv', 'r') as csvfile:
    sample = csvfile.read()
    has_header = csv.Sniffer().has_header(sample)
    # sprint(has_header)

    deduced_dialect = csv.Sniffer().sniff(sample)

with open('Nominales.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, deduced_dialect)

    for row in reader:
       generarFactura(row)
       # print (row )

