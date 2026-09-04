from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, ForeignKey, desc, asc, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import json

with open('config.json') as f:
    config = json.load(f)

db_user = config['database']['user']
db_password = config['database']['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/Sales'
engine = create_engine(db_url)

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    sales = relationship("Sale", back_populates='customer')


class Salesman(Base):
    __tablename__ = 'salesmans'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    sales = relationship("Sale", back_populates='salesman')


class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    salesman_id = Column(Integer, ForeignKey('salesmans.id'))
    total = Column(Float)
    customer = relationship("Customer", back_populates='sales')
    salesman = relationship("Salesman", back_populates='sales')


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


def add_customer():
    new_customer = Customer(first_name=input("Enter first name: "), last_name=input("Enter the last name: "))
    session.add(new_customer)
    session.commit()


def add_salesman():
    new_salesman = Salesman(first_name=input("Enter first name: "), last_name=input("Enter the last name: "))
    session.add(new_salesman)
    session.commit()


def add_sale():
    customer = Sale(salesman_id=int(input("Enter id of salesman: ")), customer_id=int(input("Enter id of customer: ")),
                    total=float(input("Enter total: ")))
    session.add(customer)
    session.commit()


def update_customer():
    search_id = int(input("Select customer id to update: "))
    customer = session.query(Customer).filter(Customer.id == search_id).first()
    if customer:
        customer.first_name = input("Enter new first name: ")
        customer.last_name = input("Enter new last name: ")
        session.commit()
        print("Customer successfully updated")
    else:
        print("Customer is not found")


def update_salesman():
    search_id = int(input("Select salesman id to update: "))
    salesman = session.query(Salesman).filter(Salesman.id == search_id).first()
    if salesman:
        salesman.first_name = input("Enter new first name: ")
        salesman.last_name = input("Enter new last name: ")
        session.commit()
        print("Salesman successfully updated")
    else:
        print("Salesman is not found")


def update_sale():
    search_id = int(input("Select sale id to update: "))
    sale = session.query(Sale).filter(Sale.id == search_id).first()
    if sale:
        sale.customer_id = input("Enter new customer id: ")
        sale.salesman_id = input("Enter new salesman id: ")
        sale.total = input("Enter new total: ")
        session.commit()
        print("sale successfully updated")
    else:
        print("sale is not found")


def delete_customer():
    search_id = int(input("Select customer id to delete: "))
    customer = session.query(Customer).filter(Customer.id == search_id).first()
    if customer:
        session.delete(customer)
        session.commit()
        print("customer successfully deleted")
    else:
        print("customer is not found")


def delete_salesman():
    search_id = int(input("Select customer id to delete: "))
    salesman = session.query(Salesman).filter(Salesman.id == search_id).first()
    if salesman:
        session.delete(salesman)
        session.commit()
        print("salesman successfully deleted")
    else:
        print("salesman is not found")


def delete_sale():
    search_id = int(input("Select sale id to delete: "))
    sale = session.query(Sale).filter(Sale.id == search_id).first()
    if sale:
        session.delete(sale)
        session.commit()
        print("sale successfully deleted")
    else:
        print("sale is not found")


def execute_queries():
    print("Відображення усіх угод; ")
    sales = session.query(Sale).all()
    show_sales(sales)
    print("--" * 20)

    print("Відображення угод конкретного продавця; ")
    salesman_id = int(input("Enter salesman id: "))
    sales = session.query(Sale).filter(Sale.salesman_id == salesman_id).all()
    show_sales(sales)
    print("--" * 20)

    print("Відображення максимальної за сумою угоди; ")
    max_sale = session.query(Sale).order_by(desc(Sale.total)).first()
    show_sales(max_sale)
    print("--" * 20)

    print("Відображення мінімальної за сумою угоди; ")
    min_sale = session.query(Sale).order_by(asc(Sale.total)).first()
    show_sales(min_sale)
    print("--" * 20)

    print("Відображення максимальної суми угоди для конкретного продавця;")
    salesman_id = int(input("Enter salesman id: "))
    sale = session.query(Sale).filter(Sale.salesman_id == salesman_id).order_by(desc(Sale.total)).first()
    show_sales(sale)
    print("--" * 20)

    print("Відображення мінімальної за сумою угоди для конкретного продавця;")
    salesman_id = int(input("Enter salesman id: "))
    sale = session.query(Sale).filter(Sale.salesman_id == salesman_id).order_by(asc(Sale.total)).first()
    show_sales(sale)
    print("--" * 20)

    print("Відображення максимальної за сумою угоди для конкретного покупця;")
    customer_id = int(input("Enter customer id: "))
    sale = session.query(Sale).filter(Sale.customer_id == customer_id).order_by(desc(Sale.total)).first()
    show_sales(sale)
    print("--" * 20)

    print("Відображення мінімальної за сумою угоди для конкретного покупця;")
    customer_id = int(input("Enter customer id: "))
    sale = session.query(Sale).filter(Sale.customer_id == customer_id).order_by(asc(Sale.total)).first()
    show_sales(sale)
    print("--" * 20)

    print("Відображення продавця з максимальною сумою продажів за всіма угодами;")
    result = session.query(Salesman, func.sum(Sale.total).label('total_sales')) \
        .join(Sale, Salesman.id == Sale.salesman_id) \
        .group_by(Salesman.id) \
        .order_by(func.sum(Sale.total).desc()) \
        .first()
    if result:
        salesman, max_sales = result
        print(f"""
            Salesman : {salesman.first_name} {salesman.last_name}
            Total sales: {max_sales}
            """)
    print("--" * 20)

    print("Відображення продавця з мінімальною сумою продажів за всіма угодами;")
    result = session.query(Salesman, func.sum(Sale.total).label('total_sales')) \
        .join(Sale, Salesman.id == Sale.salesman_id) \
        .group_by(Salesman.id) \
        .order_by(func.sum(Sale.total).asc()) \
        .first()
    if result:
        salesman, min_sales = result
        print(f"""
            Salesman : {salesman.first_name} {salesman.last_name}
            Total sales: {min_sales}
            """)
    print("--" * 20)

    print("Відображення покупця з максимальною сумою покупок за всіма угодами;")
    result = session.query(Customer, func.sum(Sale.total).label('total_sales')) \
        .join(Sale, Customer.id == Sale.customer_id) \
        .group_by(Customer.id) \
        .order_by(func.sum(Sale.total).desc()) \
        .first()
    if result:
        customer, max_sales = result
        print(f"""
            Customer : {customer.first_name} {customer.last_name}
            Total sales: {max_sales}
            """)
    print("--" * 20)

    print("Відображення середньої суми покупки для конкретного покупця;")
    customer_id = int(input("Enter customer id: "))
    average_purchase = session.query(func.avg(Sale.total).label('average_purchase')).filter(
        Sale.customer_id == customer_id).scalar()
    print(f"Average purchase for customer with ID {customer_id}: {average_purchase}")
    print("--" * 20)

    print("Відображення середньої суми покупки для конкретного продавця.")
    salesman_id = int(input("Enter salesman id: "))
    average_purchase = session.query(func.avg(Sale.total).label('average_purchase')).filter(
        Sale.salesman_id == salesman_id).scalar()
    print(f"Average purchase for salesman with ID {salesman_id}: {average_purchase}")
    print("--" * 20)


def show_sales(sales):
    if isinstance(sales, list):
        for sale in sales:
            salesman = sale.salesman
            customer = sale.customer
            print(f"""
                Sale Id : {sale.id}
                Salesman : {salesman.first_name} {salesman.last_name}
                Customer : {customer.first_name} {customer.last_name}
                Total: {sale.total}
                """)
    else:
        salesman = sales.salesman
        customer = sales.customer
        print(f"""
            Sale Id : {sales.id}
            Salesman : {salesman.first_name} {salesman.last_name}
            Customer : {customer.first_name} {customer.last_name}
            Total: {sales.total}
            """)


while True:

    choice = str(input("""
    1. add customer
    2. add salesman
    3. add sale
    4.update customer
    5.update salesman
    6.update sale
    7.delete customer
    8.statistics
    0.Exit
    ---->  """))

    try:
        if choice == '0':
            break
        elif choice == '1':
            add_customer()
        elif choice == '2':
            add_salesman()
        elif choice == '3':
            add_sale()
        elif choice == '4':
            update_customer()
        elif choice == '5':
            update_salesman()
        elif choice == '6':
            update_sale()
        elif choice == '7':
            delete_customer()
        elif choice == '8':
            execute_queries()
    except Exception as e:
        print(f"Query error: {e}")