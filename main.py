import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':

    # nombre del archivo
    out_filename = "archivo.csv"
    # nombre de las cabeceras
    headers = "Title; Price; Stock; Category; Cover; UPC; Product Type; Price (excl. tax); Price (incl. tax); Tax; Availability; Number of reviews\n"
    # se abre el archivo, y se ingresan las cabeceras
    f = open(out_filename, "w")
    f.write(headers)
    # ciclo encargado de recorrer las 50 paginas del sitio web
    for numero_pag in range(50):

        # la url cambiara en cada ciclo
        url = f'http://books.toscrape.com/catalogue/category/books_1/page-{numero_pag+1}.html'
        # y en cada uno se hara una petición
        response = requests.get(url)
        # y mientras se obtenga una respuesta satisfactoria [200] continuara con cada pagina del sitio web
        if response.status_code == 200:
            # se toma el contenido de la pagina dentro de html_doc
            html_doc = response.content
            # usamos la biblioteca importada para pasarlo a este tipo de objeto
            soup = BeautifulSoup(html_doc, 'html.parser')
            # se obtienen todos las etiquetas div que correspondan a cada libro de la pagina actual
            containers = soup.findAll("div", {"class": "image_container"})
            # variable estandar para hacer peticiones
            url_original = 'http://books.toscrape.com/catalogue'

            # ciclo para encargado de recorrer los div con la clase image_container
            for container in containers:
                

                # dentro de cada ciclo se obtendra una url(incompleta) del detalle del libro para hacer la peticion por cada uno (20 por cada pagina)

                # se completa la url con la variable url_original
                response_link = requests.get(
                    url_original + container.a.get("href")[5:])
                # junto a la etiqueta <a> de la cual solo queremos su href descartando los primeros 5 caracteres

                # si la peticion es [200] continuara con cada libro
                if response_link.status_code == 200:
                    # dentro de la pagina obtenemos todo el contenido del cual tendremos los detalles, titulo, etc
                    content_book = response_link.content
                    # dicho contenido lo consideramos como un documento html
                    html_doc = content_book
                    # lo pasamos a objeto BeautifulSoup para obtener los datos de las etiquetas
                    soup_book = BeautifulSoup(html_doc, 'html.parser')
                    # titulo
                    titulo = soup_book.h1.text
                    # precio
                    precio = soup_book.find("p", {"class": "price_color"}).text
                    # stock
                    stock = soup_book.find(
                        "p", {"class": "instock availability"}).text.strip()[:-14]
                    # categoria
                    categoria = (soup_book.ul.select("li")[2].text.strip())
                    # cover
                    cover = url_original[:-10] + \
                        soup_book.img.get("src").strip()[5:]
                    # UPC
                    upc = soup_book.table.select("tr")[0].td.text.strip()
                    # Product Type
                    product_type = soup_book.table.select(
                        "tr")[1].td.text.strip()
                    #Price (excl. tax)
                    price_excl_tax = soup_book.table.select(
                        "tr")[2].td.text.strip()
                    #Price (incl. tax)
                    price_incl_tax = soup_book.table.select(
                        "tr")[3].td.text.strip()
                    # Tax
                    tax = soup_book.table.select("tr")[4].td.text.strip()
                    # Availability
                    availability = soup_book.table.select(
                        "tr")[5].td.text.strip()[10:-1]
                    # Number of reviews
                    number_reviews = soup_book.table.select(
                        "tr")[6].td.text.strip()
                    # ingresamos los datos al archivo en el orden de las cabeceras
                    f.write(titulo+"; "+precio + "; "+stock +
                            "; "+categoria + "; "+cover + "; "+upc + "; "+product_type +
                            "; "+price_excl_tax + "; " + price_incl_tax + "; " + tax + "; "+availability + "; "+number_reviews)
                    # hacemos un salto de linea dentro del archivo
                    f.write("\n")

                else:  # en caso de que la solicitud no corresponda a 200
                    print("Solicitud incorrecta")

    f.close()  # Se cierra el archivo.csv
    print("Completado")
