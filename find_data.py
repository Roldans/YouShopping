#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from urllib2 import *
from bs4 import BeautifulSoup
from principal.models import Producto 
import sys
import sqlite3
#IMPORTANTE!!!!! PERMITE EL USO DE URLS CON TILDES SIN PROBLEMAS 
#USAMOS EL ENCODE UTF-8 EN VEZ DE UNICODE!!!!
reload(sys)

sys.setdefaultencoding("utf-8")



root="http://www.foody.es"

##-------------------------------crawl html of a web----------------------------------------
# obtiene el html de una url
def recuperarhtml(url):
    try:
        f = urllib2.urlopen(url)
        page = f.read()
        f.close()
        return page
        
    except HTTPError, e:
        print "Ocurrió un error"
        print e.code
    except URLError, e:
        print "Ocurrió un error"
        print e.reason
    except ValueError, e:

        print e.message


#   filtra los datos del producto desde su html
#	Los campos a guardar en la base de datos son:
#	name:			el nombre del producto
#	price:			el precio del producto
#	description:	La descripcion del producto dada por la tienda
#	fields:			Filtros del buscador(en esta tienda son alergenos) 
def filtrarProduct(html):
    soup = BeautifulSoup(str(html), 'html.parser')
    name = soup.find('h1').string
    price = soup.find('span',class_='PricesalesPrice').string
    description_table = soup.find(class_='product-description')
    description=""
    fields=""
    URL=soup.find('base').get('href')
    

    #El bloque if es devido a que algunos productos no tienen description
    if description_table != None:
    #Se ha usado dos fors debido que el html contenia el tag "strong" en algunas palabrassin seguir un patron
    #por lo que para facilitar su analisis se ha realizado de esta manera
        for description_data1 in description_table.find_all('p'):
            for description_data2 in  description_data1.strings:
                description += description_data2
            description += "\n"    
        
    fields_table = soup.find('table',class_='marca_calidad')
    #El bloque if es devido a que algunos productos no tienen fields
    if fields_table != None:
        fields_table=fields_table.find_all(class_='product-fields-title')
        for fields_data in fields_table:
            if "Logo" not in fields_data.string:
                fields+=fields_data.string+","
        fields=fields[:-1]
    #print "name=="+name
    #print "price=="+price
    #print "DESCRIPTION:\n"+description
    #print fields
    # Conexion con la DB
    conn = sqlite3.connect('db.sqlite3')
    conn.text_factory = str
    # Almacenamos los datos
    conn.execute("INSERT INTO principal_producto (name,price,descripcion,categorias,url) \
                             VALUES (?,?,?,?,?);", [name, price, description,fields,URL])
    # commit y close connection
    conn.commit()
    conn.close()

# filter products pages of a category page
def filtrarcategorypage(html):
    soup = BeautifulSoup(str(html), 'html.parser')
    table = soup.find_all(class_='vm-details-button')
    urls=[]
    for a in table:
    	urls.append(root +a.find('a').get('href'))
   
    return urls


# filter pages of a category page
def filtrarpagescategory(html):
    soup = BeautifulSoup(str(html), 'html.parser')
    table = soup.find('nav',class_="pagination")
    urls=[]
    if table!=None:
        for a in table.find_all('a'):
        	urls.append(root +a.get('href'))
    else:
        urls.append( soup.find('base').get('href'))
    return urls

# take the urls from the html
def filtrarcategories(html):
    soup = BeautifulSoup(str(html), 'html.parser')
    table = soup.find(class_="VMmenu").children
    urls=[]
    
    while(True):
        
    	try:
            table.next()
            row=table.next()
            if(row.find(class_='menu')!=None):
                for a in  row.find(class_='menu').find_all('a'):
                    urls.append(root + a.get('href'))
            else:
                urls.append(root + row.find('a').get('href'))
        except StopIteration,e:
            break
    return urls
def crawl():
    conn = sqlite3.connect('db.sqlite3')
    conn.text_factory = str
    # Almacenamos los datos
    conn.execute("DELETE FROM principal_producto")
    # commit y close connection
    conn.commit()
    conn.close()
    print "Cleaned database successfully";
    contador = 0

    #la root es la pagina principal
    page = recuperarhtml(root)
    #obtenemos las url de cada categoria
    categoryurls=filtrarcategories(page)    
    for categoryurl in categoryurls:
        page = recuperarhtml(categoryurl)
    	#recuperamos todas las paginas(paginacion) de la categoria
    	#(no aparecen todos los productos en la primera pagina)
    	categorypages=filtrarpagescategory(page)
    	for categorypage in categorypages:
    		#Buscamos las paginas de cada producto
    		Producturls=filtrarcategorypage(page)
    		
            	for Producturl in Producturls:
                	contador =contador +1
			if contador%10==0:                	
				print str(contador) + " items stored"
	                #print "Articulo " + str(contador)
	                #print Producturl
	                page = recuperarhtml(Producturl) 
	                filtrarProduct(page)
	                #print "================================================"
	                #print "================================================"


     
crawl()

