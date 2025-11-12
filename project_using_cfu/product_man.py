from cfu import ColMan
import os


FILE = "products.csv"
FIELDS = ["id", "proucts", "price", "quantity"]


cfu = ColMan(file_name=FILE, fields=FIELDS)
cfu.save_csv()


def main():
    ...


def interface():
    print("________Dasbord________")
    print("1. Add Product")
    print("2. View All Products")
    print("3. Update Product")
    print("4. Delete Product")
    print("5. Search Product")
    print("6. Add New Column")
    print("7. Exit")


if __name__ == "__main__":
    main()