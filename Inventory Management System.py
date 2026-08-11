import json
from datetime import datetime


class InventorySystem:

    def __init__(self):

        self.path = "/userdata/administrator/Desktop/git-test/inventory-management-billing-system/Inventory.json"
        self.sales_path = "/userdata/administrator/Desktop/git-test/inventory-management-billing-system/sales.json"

        # Load inventory
        try:
            with open(self.path, "r") as file:
                self.data = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

        # Load sales
        try:
            with open(self.sales_path, "r") as file:
                self.sales = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            self.sales = []

    # =========================================================
    # FILE HANDLING
    # =========================================================

    def save_inventory(self):

        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=4)

    def save_sales(self):

        with open(self.sales_path, "w") as file:
            json.dump(self.sales, file, indent=4)

    # =========================================================
    # 1. ADD PRODUCT
    # =========================================================

    def add_product(self):

        product_id = input("Enter the Id of Product=")

        if product_id in self.data:
            print("Product Already exists")
            return

        name = input("Enter The name of the product=").lower()
        category = input("Enter the category of the Product=").lower()
        purchase_price = float(input("Enter Purchase Price="))
        selling_price = float(input("Enter Selling Price="))
        stock = int(input("Enter the amount of product="))
        minimum_stock = int(input("Enter Minimum Stock="))

        if purchase_price <= 0:
            print("Purchase price must be greater than 0")
            return

        if selling_price <= 0:
            print("Selling price must be greater than 0")
            return

        if stock < 0:
            print("Stock cannot be negative")
            return

        if minimum_stock < 0:
            print("Minimum stock cannot be negative")
            return

        self.data[product_id] = {
            "name": name,
            "category": category,
            "purchase price": purchase_price,
            "selling price": selling_price,
            "stock": stock,
            "ms": minimum_stock
        }

        self.save_inventory()

        print("Product Added Successfully")

    # =========================================================
    # 2. VIEW PRODUCT
    # =========================================================

    def view_product(self):

        product_id = input("Enter the Id of Product=")

        if product_id in self.data:

            product = self.data[product_id]

            print("\n========== PRODUCT DETAILS ==========")
            print("Product Id     :", product_id)
            print("Product Name   :", product["name"])
            print("Category       :", product["category"])
            print("Purchase Price :", product["purchase price"])
            print("Selling Price  :", product["selling price"])
            print("Stock          :", product["stock"])
            print("Minimum Stock  :", product["ms"])

        else:
            print("Product Not Found")

    # =========================================================
    # 3. VIEW ALL PRODUCTS
    # =========================================================

    def view_all_products(self):

        if not self.data:
            print("No Products Found")
            return

        print("\n========== ALL PRODUCTS ==========")

        for product_id, product in self.data.items():

            print("--------------------------------")
            print("Product Id       :", product_id)
            print("Product Name     :", product["name"])
            print("Category         :", product["category"])
            print("Purchase Price   :", product["purchase price"])
            print("Selling Price    :", product["selling price"])
            print("Stock Available  :", product["stock"])

    # =========================================================
    # 4. UPDATE PRODUCT
    # =========================================================

    def update_product(self):

        product_id = input("Enter the Id of Product=")

        if product_id not in self.data:
            print("Product Not Found")
            return

        while True:

            print("\n========== UPDATE PRODUCT ==========")
            print("1. Change Name")
            print("2. Change Stock")
            print("3. Change Selling Price")
            print("4. Exit")

            choice = int(input("Enter Your Choice="))

            if choice == 1:

                self.data[product_id]["name"] = input(
                    "Enter New name of the product="
                ).lower()

                self.save_inventory()
                print("Name Changed Successfully")

            elif choice == 2:

                new_stock = int(input("Enter the updated stock="))

                if new_stock < 0:
                    print("Stock cannot be negative")
                    continue

                self.data[product_id]["stock"] = new_stock

                self.save_inventory()
                print("Stock Updated")

            elif choice == 3:

                new_price = float(input("Enter the new Selling Price="))

                if new_price <= 0:
                    print("Selling price must be greater than 0")
                    continue

                self.data[product_id]["selling price"] = new_price

                self.save_inventory()
                print("Selling Price changed")

            elif choice == 4:
                break

            else:
                print("Invalid Choice")

    # =========================================================
    # 5. DELETE PRODUCT
    # =========================================================

    def delete_product(self):

        product_id = input("Enter Products Id to Delete=")

        if product_id not in self.data:
            print("Product Not Found")
            return

        answer = input(
            "Are you Sure you want to delete Product? (yes/no)="
        ).lower()

        if answer == "yes":

            del self.data[product_id]

            self.save_inventory()

            print("Product Removed Successfully")

        elif answer == "no":
            print("Product Not deleted")

        else:
            print("Invalid Choice")

    # =========================================================
    # 6. ADD STOCK
    # =========================================================

    def add_stock(self):

        product_id = input("Enter the Id of product=")

        if product_id not in self.data:
            print("Product Not Found")
            return

        new_stock = int(input("Enter the amount of stock to add="))

        if new_stock <= 0:
            print("Stock to add must be greater than 0")
            return

        self.data[product_id]["stock"] += new_stock

        self.save_inventory()

        print("New Stock =", self.data[product_id]["stock"])
        print("Stock Updated Successfully")

    # =========================================================
    # 7. LOW STOCK PRODUCTS
    # =========================================================

    def low_stock_products(self):

        low_stock_found = False

        print("\n========== LOW STOCK PRODUCTS ==========")

        for product_id, product in self.data.items():

            if product["stock"] < product["ms"]:

                print("--------------------------------")
                print("Product ID     :", product_id)
                print("Product Name   :", product["name"])
                print("Current Stock  :", product["stock"])
                print("Minimum Stock  :", product["ms"])
                print("LOW STOCK ALERT!")

                low_stock_found = True

        if not low_stock_found:
            print("No Low Stock Products")

    # =========================================================
    # 8. MAKE SALES
    # =========================================================

    def sell_product(self):

        cart = []

        customer_name = input("Enter Customer Name: ")
        customer_phone = input("Enter Customer Phone: ")

        while True:

            product_id = input("\nEnter Product ID: ")

            if product_id not in self.data:
                print("Product Not Found!")
                continue

            product = self.data[product_id]

            print("\nProduct Name :", product["name"])
            print("Selling Price:", product["selling price"])
            print("Available Stock:", product["stock"])

            quantity = int(input("Enter Quantity: "))

            if quantity <= 0:
                print("Quantity must be greater than 0")
                continue

            if quantity > product["stock"]:
                print("Insufficient Stock!")
                continue

            price = product["selling price"]

            total = price * quantity

            profit = (
                product["selling price"] -
                product["purchase price"]
            ) * quantity

            item = {
                "product_id": product_id,
                "product_name": product["name"],
                "quantity": quantity,
                "price": price,
                "total": total,
                "profit": profit
            }

            cart.append(item)

            print("Product added to cart!")

            more = input("Add another product? (yes/no): ").lower()

            if more == "no":
                break

        if not cart:
            print("Cart is empty!")
            return

        grand_total = 0
        total_profit = 0

        for item in cart:
            grand_total += item["total"]
            total_profit += item["profit"]

        while True:

            discount_percent = float(input("Enter Discount (%): "))

            if 0 <= discount_percent <= 100:
                break

            print("Invalid Discount! Enter a value between 0 and 100.")

        discount_amount = (grand_total * discount_percent) / 100

        final_amount = grand_total - discount_amount

        print("\n========== BILL SUMMARY ==========")
        print("Subtotal        :", grand_total)
        print("Discount        :", discount_percent, "%")
        print("Discount Amount :", discount_amount)
        print("----------------------------------")
        print("FINAL AMOUNT    :", final_amount)
        print("==================================")

        # Payment
        print("\n========== PAYMENT ==========")
        print("1. Cash")
        print("2. UPI")
        print("3. Card")

        payment_choice = int(input("Enter Payment Method: "))

        if payment_choice == 1:

            payment_method = "Cash"

            print("\nAmount to Pay: ₹", final_amount)

            while True:

                amount_paid = float(input("Enter Amount Paid: ₹"))

                if amount_paid < final_amount:

                    print("Insufficient Amount!")
                    print("Amount Required:", final_amount)

                else:

                    change = amount_paid - final_amount
                    break

            print("Change to Return:", change)

        elif payment_choice == 2:

            payment_method = "UPI"
            amount_paid = final_amount
            change = 0

            print("\nAmount to Pay: ₹", final_amount)
            print("UPI Payment Received Successfully!")

        elif payment_choice == 3:

            payment_method = "Card"
            amount_paid = final_amount
            change = 0

            print("\nAmount to Pay: ₹", final_amount)
            print("Card Payment Received Successfully!")

        else:

            print("Invalid Payment Method!")
            return

        # Reduce stock
        for item in cart:

            product_id = item["product_id"]

            self.data[product_id]["stock"] -= item["quantity"]

        self.save_inventory()

        # Sale ID and Date
        sale_id = "SALE" + str(len(self.sales) + 1).zfill(3)

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save transaction
        transaction = {
            "sale_id": sale_id,
            "date": date_time,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "items": cart,
            "sub_total": grand_total,
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "final_amount": final_amount,
            "payment_method": payment_method,
            "amount_paid": amount_paid,
            "change": change,
            "total_profit": total_profit
        }

        self.sales.append(transaction)

        self.save_sales()

        # Print receipt
        print("\n========== SALE RECEIPT ==========")

        print("Sale ID        :", sale_id)
        print("Date           :", date_time)
        print("Customer Name  :", customer_name)
        print("Customer Phone :", customer_phone)

        print("----------------------------------------------")
        print("Product\t\tQty\tPrice\tTotal")
        print("----------------------------------------------")

        for item in cart:

            print(
                item["product_name"],
                "\t",
                item["quantity"],
                "\t",
                item["price"],
                "\t",
                item["total"]
            )

        print("----------------------------------------------")

        print("Subtotal        :", grand_total)
        print("Discount        :", discount_percent, "%")
        print("Discount Amount :", discount_amount)
        print("Final Amount    :", final_amount)
        print("Payment Method  :", payment_method)
        print("Amount Paid     :", amount_paid)
        print("Change          :", change)
        print("Total Profit    :", total_profit)

        print("==============================================")

    # =========================================================
    # 9. SALES HISTORY
    # =========================================================

    def sales_history(self):

        if not self.sales:
            print("Sales Not Found")
            return

        print("\n========== SALES HISTORY ==========")

        for transaction in self.sales:

            print("--------------------------------")
            print("Sale ID        :", transaction["sale_id"])
            print("Date           :", transaction["date"])
            print("Customer Name  :", transaction["customer_name"])
            print("Customer Phone :", transaction["customer_phone"])
            print("Final Amount   :", transaction["final_amount"])
            print("Payment Method :", transaction["payment_method"])

    # =========================================================
    # 10. VIEW SALES
    # =========================================================

    def view_sale(self):

        sale_id = input("Enter Sale ID to View Details: ")

        found = False

        for transaction in self.sales:

            if transaction["sale_id"] == sale_id:

                print("\n========== SALE DETAILS ==========")

                print("Sale ID        :", transaction["sale_id"])
                print("Date           :", transaction["date"])
                print("Customer Name  :", transaction["customer_name"])
                print("Customer Phone :", transaction["customer_phone"])

                print("\n----------- PRODUCTS -----------")

                for item in transaction["items"]:

                    print("Product :", item["product_name"])
                    print("Quantity:", item["quantity"])
                    print("Price   :", item["price"])
                    print("Total   :", item["total"])
                    print("--------------------------------")

                print("Subtotal        :", transaction["sub_total"])
                print("Discount        :", transaction["discount_amount"])
                print("Final Amount    :", transaction["final_amount"])
                print("Payment Method  :", transaction["payment_method"])
                print("Amount Paid     :", transaction["amount_paid"])
                print("Change          :", transaction["change"])

                found = True
                break

        if not found:
            print("Sale Not Found!")

    # =========================================================
    # 11. CUSTOMER PURCHASE HISTORY
    # =========================================================

    def customer_purchase_history(self):

        phone = input("Enter Customer Phone: ")

        found = False

        print("\n========== CUSTOMER PURCHASE HISTORY ==========")

        for transaction in self.sales:

            if transaction["customer_phone"] == phone:

                print("--------------------------------")
                print("Sale ID :", transaction["sale_id"])
                print("Date    :", transaction["date"])
                print("Amount  :", transaction["final_amount"])

                found = True

        if not found:
            print("No Purchase History Found!")

    # =========================================================
    # 12. TODAY'S BUSINESS REPORT
    # =========================================================

    def todays_business_report(self):

        today = datetime.now().strftime("%Y-%m-%d")

        total_sales = 0
        total_profit = 0
        total_orders = 0
        products_sold = 0

        cash_sales = 0
        upi_sales = 0
        card_sales = 0

        for transaction in self.sales:

            transaction_date = transaction["date"].split(" ")[0]

            if transaction_date == today:

                total_orders += 1

                total_sales += transaction["final_amount"]
                total_profit += transaction["total_profit"]

                if transaction["payment_method"] == "Cash":
                    cash_sales += transaction["final_amount"]

                elif transaction["payment_method"] == "UPI":
                    upi_sales += transaction["final_amount"]

                elif transaction["payment_method"] == "Card":
                    card_sales += transaction["final_amount"]

                for item in transaction["items"]:
                    products_sold += item["quantity"]

        print("\n========== TODAY'S BUSINESS REPORT ==========")

        print("Date             :", today)
        print("Total Sales      :", total_sales)
        print("Orders           :", total_orders)
        print("Products Sold    :", products_sold)
        print("Total Profit     :", total_profit)

        print("\n------ PAYMENT SUMMARY ------")

        print("Cash Sales       :", cash_sales)
        print("UPI Sales        :", upi_sales)
        print("Card Sales       :", card_sales)

        print("==============================================")

    # =========================================================
    # 13. BEST SELLING PRODUCTS
    # =========================================================

    def best_selling_products(self):

        product_sales = {}

        for transaction in self.sales:

            for item in transaction["items"]:

                product_name = item["product_name"]
                quantity = item["quantity"]

                if product_name in product_sales:

                    product_sales[product_name] += quantity

                else:

                    product_sales[product_name] = quantity

        sorted_products = sorted(
            product_sales.items(),
            key=lambda x: x[1],
            reverse=True
        )

        print("\n========== BEST SELLING PRODUCTS ==========")

        if not sorted_products:

            print("No Sales Found!")

        else:

            rank = 1

            for product_name, quantity in sorted_products:

                print(
                    rank,
                    ".",
                    product_name,
                    "→",
                    quantity,
                    "units"
                )

                rank += 1

        print("============================================")

    # =========================================================
    # 14. INVENTORY REPORT
    # =========================================================

    def inventory_report(self):

        total_products = 0
        total_units = 0
        inventory_value = 0
        low_stock = 0
        out_of_stock = 0

        for product_id, product in self.data.items():

            total_products += 1

            stock = product["stock"]
            purchase_price = product["purchase price"]
            minimum_stock = product["ms"]

            total_units += stock

            inventory_value += purchase_price * stock

            if stock == 0:

                out_of_stock += 1

            elif stock < minimum_stock:

                low_stock += 1

        print("\n========== INVENTORY REPORT ==========")

        print("Total Products       :", total_products)
        print("Total Units in Stock :", total_units)
        print("Inventory Value      :", inventory_value)

        print("Low Stock Products   :", low_stock)
        print("Out of Stock         :", out_of_stock)

        print("======================================")

    # =========================================================
    # 15. MENU
    # =========================================================

    def menu(self):

        while True:

            print("\n========== INVENTORY MANAGEMENT SYSTEM ==========")

            print("1. Add Product")
            print("2. View Product")
            print("3. View All Products")
            print("4. Update Product")
            print("5. Delete Product")
            print("6. Add Stock")
            print("7. Low Stock Products")
            print("8. Make Sales")
            print("9. Sales History")
            print("10. View Sales")
            print("11. Customer Purchase History")
            print("12. Today's Business Report")
            print("13. Best Selling Products")
            print("14. Inventory Report")
            print("15. Exit")

            try:
                choice = int(input("Enter your choice="))

            except ValueError:
                print("Please enter a valid number.")
                continue

            if choice == 1:
                self.add_product()

            elif choice == 2:
                self.view_product()

            elif choice == 3:
                self.view_all_products()

            elif choice == 4:
                self.update_product()

            elif choice == 5:
                self.delete_product()

            elif choice == 6:
                self.add_stock()

            elif choice == 7:
                self.low_stock_products()

            elif choice == 8:
                self.sell_product()

            elif choice == 9:
                self.sales_history()

            elif choice == 10:
                self.view_sale()

            elif choice == 11:
                self.customer_purchase_history()

            elif choice == 12:
                self.todays_business_report()

            elif choice == 13:
                self.best_selling_products()

            elif choice == 14:
                self.inventory_report()

            elif choice == 15:
                print("Exiting the program...")
                break

            else:
                print("Invalid Choice!")


# =============================================================
# MAIN PROGRAM
# =============================================================

system = InventorySystem()
system.menu()
