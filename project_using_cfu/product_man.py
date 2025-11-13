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
    print("3. Update Value")
    print("4. Delete Product")
    print("5. Search Product")
    print("6. Add New Column")
    print("7. Exit")


def search_product():
    """This function 'cfu.search_column' converts the dictionary data searched by this function into formatting data Searches"""
    product = input("Enter product name: ")

    pd = cfu.search_column("products", product)
    
    if not pd:
        print(f"'{product}' Not found")
        return
    print(f"Name: {pd['products']}| Prict: {pd['price']}| Quantity{pd['quantity']}")


search_product()


def operation():
    while True:
        interface()
        choise = input("-> ")

        if choise == "1":
            cfu.add_data()
        elif choise == "2":
            pass
        elif choise == "3":
            pass
            # terget_name = input("Enter terget: ")
            # old_value = input("Enter old value: ")
            # new_value = input("Enter new value: ")
            # cfu.update_value(terget_name, old_value, new_value, file_name=FILE)
        elif choise == "4":
            product_name = input("Enter product name: ").strip()
            cfu.del_data(product_name, key="products", file_name=FILE)
        elif choise == "5":
            search_product()
        elif choise == "6":
            pass
        elif choise == "7":
            break 
        else:
            print(f"Invalid input: {choise}")


if __name__ == "__main__":
    main()