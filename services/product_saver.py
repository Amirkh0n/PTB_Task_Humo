import config as conf 

def save_product(product):
    return conf.products.insert(
        title=product.get('title'), 
        description=product.get('description'),
        price=product.get('price'), 
        count=product.get('count'),
        category_id = product.get('category_id'),
        image_path=product.get('image', 'images/1.jpg')
    )
    