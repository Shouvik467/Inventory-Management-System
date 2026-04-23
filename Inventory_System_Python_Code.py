import mysql.connector
from mysql.connector import Error

class InventorySystem:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="inventory_system"
            )
            self.cursor = self.conn.cursor()
            print("✅ Connected to Inventory DB")
        except Error as e:
            print("❌ Connection Error:", e)
            exit()

    # --------------------------
    # CATEGORY
    # --------------------------
    def add_category(self):
        name = input("Enter category name: ")
        try:
            self.cursor.execute(
                "INSERT INTO categories (name) VALUES (%s)", (name,))
            self.conn.commit()
            print("✅ Category added")
        except Error as e:
            print("❌ Error:", e)

    # --------------------------
    # PRODUCT
    # --------------------------
    def add_product(self):
        name = input("Product name: ")
        category_id = int(input("Category ID: "))
        price = float(input("Price: "))

        try:
            self.cursor.execute(
                "INSERT INTO products (name, category_id, price) VALUES (%s, %s, %s)",
                (name, category_id, price)
            )
            self.conn.commit()
            print("✅ Product added")
        except Error as e:
            print("❌ Error:", e)

    def view_products(self):
        query = """
        SELECT p.product_id, p.name, c.name, p.price, p.stock
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        print("\n--- PRODUCTS ---")
        for r in rows:
            print(f"ID:{r[0]} | Name:{r[1]} | Category:{r[2]} | Price:{r[3]} | Stock:{r[4]}")

    # --------------------------
    # SUPPLIER
    # --------------------------
    def add_supplier(self):
        name = input("Supplier name: ")
        contact = input("Contact: ")

        try:
            self.cursor.execute(
                "INSERT INTO suppliers (name, contact) VALUES (%s, %s)",
                (name, contact)
            )
            self.conn.commit()
            print("✅ Supplier added")
        except Error as e:
            print("❌ Error:", e)

    # --------------------------
    # PURCHASE (STOCK IN)
    # --------------------------
    def purchase(self):
        product_id = int(input("Product ID: "))
        supplier_id = int(input("Supplier ID: "))
        qty = int(input("Quantity: "))

        try:
            self.cursor.execute(
                "INSERT INTO purchases (product_id, supplier_id, quantity) VALUES (%s, %s, %s)",
                (product_id, supplier_id, qty)
            )
            self.conn.commit()
            print("📥 Purchase recorded (Stock Updated)")
        except Error as e:
            print("❌ Error:", e)

    # --------------------------
    # SALE (STOCK OUT)
    # --------------------------
    def sale(self):
        product_id = int(input("Product ID: "))
        qty = int(input("Quantity: "))

        try:
            self.cursor.execute(
                "INSERT INTO sales (product_id, quantity) VALUES (%s, %s)",
                (product_id, qty)
            )
            self.conn.commit()
            print("📤 Sale recorded (Stock Updated)")
        except Error as e:
            print("❌ Error:", e)

    # --------------------------
    # REPORTS
    # --------------------------
    def low_stock(self):
        self.cursor.execute("SELECT * FROM products WHERE stock < 5")
        rows = self.cursor.fetchall()

        print("\n⚠️ LOW STOCK ITEMS:")
        for r in rows:
            print(f"{r[1]} (Stock: {r[4]})")

    def sales_report(self):
        query = """
        SELECT product_id, SUM(quantity)
        FROM sales
        GROUP BY product_id
        """
        self.cursor.execute(query)

        print("\n📊 SALES REPORT:")
        for r in self.cursor.fetchall():
            print(f"Product ID: {r[0]} | Sold: {r[1]}")

    # --------------------------
    # MENU
    # --------------------------
    def menu(self):
        while True:
            print("\n==== INVENTORY SYSTEM ====")
            print("1. Add Category")
            print("2. Add Product")
            print("3. View Products")
            print("4. Add Supplier")
            print("5. Purchase Product")
            print("6. Sell Product")
            print("7. Low Stock Report")
            print("8. Sales Report")
            print("9. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                self.add_category()
            elif choice == '2':
                self.add_product()
            elif choice == '3':
                self.view_products()
            elif choice == '4':
                self.add_supplier()
            elif choice == '5':
                self.purchase()
            elif choice == '6':
                self.sale()
            elif choice == '7':
                self.low_stock()
            elif choice == '8':
                self.sales_report()
            elif choice == '9':
                break
            else:
                print("❌ Invalid choice")

        self.cursor.close()
        self.conn.close()
        print("🔒 Connection closed")


# RUN
if __name__ == "__main__":
    app = InventorySystem()
    app.menu()
