from store.models import Product
import csv
from PIL import Image
from django.core.files.base import ContentFile


from store.models import Product
# import random
# for item in Product.objects.all():
#     item.quantity=random.randint(5,50)
#     item.price=random.randint(5,100)
#     item.save()


productTitles=[]
images=[]
def run():

    with open('D:/nata/efashion/efashionshop/scripts/fashionWomen.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

    #    # Film.objects.all().delete()
    #     #Genre.objects.all().delete()

        for row in reader:
            print(row)

            if row[7] not in productTitles:
                product = Product(id=row[0],
                            gender=row[1],
                            category=row[2],
                            subCategory=row[3],
                            productType=row[4],
                            colour=row[5],
                            usage=row[6],
                            productTitle=row[7],
                            productImage=row[8],
                            imageUrl=row[9]
                            )
                
                
            
                duplicate=product.get_remote_image(images=images)
                if (not duplicate):
                    productTitles.append(row[7])
                    product.save()

            
            #'D:/nata/archive/data/allImages/'+ row[8]
            #with open('D:/nata/archive/data/allImages/'+ row[8], errors="ignore") as f:
            #     data = f.read()
            # image = Image.open("image_path.jpg")
            # product.productImage.save(row[8], image)
        