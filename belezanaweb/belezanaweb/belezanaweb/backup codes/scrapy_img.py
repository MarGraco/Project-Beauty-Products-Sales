import scrapy
from datetime import date
import csv
import os

class EcomSpider(scrapy.Spider):
    name = "scrapy_img"

    start_urls = ['https://www.belezanaweb.com.br/busca/?q=creme%20facial']  # Insira a URL do site aqui

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []
        self.file_name = date.today().strftime('%d_%m_%Y_dados_img_belezanaweb.csv')

    def parse(self, response):
        # Itera sobre cada item na página de resultados
        for product in response.css('.showcase-item'):
            try:
                # Coleta os dados desejados
                brand = product.css('.showcase-item-brand::text').get().strip()
                title = product.css('.showcase-item-title::text').get().strip()
                
                # Captura a URL da imagem do produto
                image_url = product.css('img.showcase-image::attr(data-src)').get() or \
                            product.css('img.showcase-image::attr(src)').get()

                self.data.append({
                    'Date': date.today().strftime('%d/%m/%Y'),
                    'Brand': brand,
                    'Title': title,
                    'Image': image_url,
                })

            except Exception as e:
                self.log(f"Error parsing item: {e}")
                continue

        # Paginação para a próxima página
        next_page = response.css('.btn-load-more::attr(data-ajax)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def close(self, reason):
        # Caminho base onde os arquivos serão salvos
        base_path = './bases_historicas_img'

        # Cria a pasta 'bases_historicas' se não existir
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            self.log(f"Directory created: {base_path}")

        # Define o caminho completo do arquivo
        file_path = os.path.join(base_path, self.file_name)

        # Salva os dados no arquivo CSV
        keys = self.data[0].keys() if self.data else []
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.data)

        self.log(f"Data saved to {file_path}")
