import scrapy
from datetime import date
import os
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class EcomSpider(scrapy.Spider):
    name = "scrapy4_bnw"

    start_urls = ['https://www.belezanaweb.com.br/busca/?q=creme%20facial']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []

        # Configurações de conexão com o banco de dados
        db_host = os.getenv('DATABASE_HOST')
        db_port = os.getenv('DATABASE_PORT')
        db_user = os.getenv('DATABASE_USER')
        db_password = os.getenv('DATABASE_PASSWORD')
        db_name = os.getenv('DATABASE_NAME')

        # Cria a conexão com o banco de dados usando SQLAlchemy
        self.engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def parse(self, response):
        for product in response.css('.showcase-item'):
            try:
                def parse_price(price_str):
                    if price_str:
                        price_str = price_str.replace('.', '').replace(',', '.')
                        return float(price_str)
                    return None

                # Coleta os dados desejados
                brand = product.css('.showcase-item-brand::text').get().strip()
                title = product.css('.showcase-item-title::text').get().strip()

                price_full = product.css('.item-price-max::text').get()
                price_full = parse_price(price_full.split(' ')[1]) if price_full else None

                if price_full is None:
                    continue

                price_soft = product.css('.price-value::text').get()
                price_soft = parse_price(price_soft.split(' ')[1]) if price_soft else None

                review_count = product.css('div.showcase-item-rating.pointer::attr(title)').get()
                if review_count:
                    review_count = review_count.split()[0]
                    if review_count.lower() == "avalie":
                        review_count = 0
                    else:
                        review_count = int(review_count)
                else:
                    review_count = 0

                rating = product.css('img.star::attr(alt)').get()
                if rating:
                    rating = parse_price(rating.split(' ')[1])
                else:
                    rating = 0.0

                if price_full and price_soft:
                    priceoff = round(((price_soft / price_full) - 1) * (-100))
                else:
                    priceoff = None

                def format_price(price):
                    if price is not None:
                        return f"{price:.2f}".replace('.', ',')
                    return None

                price_full = format_price(price_full)
                price_soft = format_price(price_soft)
                rating = format_price(rating)

                # Captura a URL da imagem do produto
                image_url = product.css('img.showcase-image::attr(data-src)').get() or \
                            product.css('img.showcase-image::attr(src)').get()

            except Exception as e:
                self.log(f"Error parsing item: {e}")
                continue

            item_data = {
                'Date': date.today().strftime('%Y-%m-%d'),
                'Brand': brand,
                'Title': title,
                'price_full': price_full,
                'price_soft': price_soft,
                'priceoff': priceoff,
                'Rating': rating,
                'Review Count': review_count,
                'Image': image_url,
            }

            self.data.append(item_data)

            # Insere os dados no banco de dados
            self.insert_into_db(item_data)

        next_page = response.css('.btn-load-more::attr(data-ajax)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def insert_into_db(self, item_data):
        try:
            # Inserção segura usando SQLAlchemy's text e parâmetros
            insert_query = text("""
                INSERT INTO "Dados Beleza na Web" ("Date", "Brand", "Title", "price_full", "price_soft", "priceoff", "Rating", "Review Count", "Image")
                VALUES (:Date, :Brand, :Title, :price_full, :price_soft, :priceoff, :Rating, :review_count, :image_url)
            """)
            self.session.execute(insert_query, {
                'Date': item_data['Date'],
                'Brand': item_data['Brand'],
                'Title': item_data['Title'],
                'price_full': item_data['price_full'],
                'price_soft': item_data['price_soft'],
                'priceoff': item_data['priceoff'],
                'Rating': item_data['Rating'],
                'review_count': item_data['Review Count'],
                'image_url': item_data['Image']
            })
            self.session.commit()
            
            # Adiciona uma mensagem de confirmação
            print(f"Dados inseridos com sucesso na tabela 'Dados Beleza na Web': {item_data['Title']}")
            
        except Exception as e:
            self.log(f"Error inserting data into DB: {e}")
            self.session.rollback()

    def close(self, reason):
        # Fecha a sessão do banco de dados
        self.session.close()
