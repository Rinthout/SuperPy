import os
import argparse
import csv
import pandas as pd
from datetime import datetime, date, timedelta
from tabulate import tabulate
from rich.console import Console


# working path and directory
wd = os.getcwd()
bought_path = os.path.join(wd, "bought.csv")
sold_path = os.path.join(wd, "sold.csv")

# create a console object
console = Console()


# thanks after every run in terminal
def footnote():
    print("")
    console.print(
        "[yellow]-[/yellow]" * 17,
        "[blue]Thanks for using SuperPy![/blue]",
        "[yellow]-[/yellow]" * 18,
    )
    print("")


# convert date string in right format
def valid_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        msg = f"{date_string} - Please enter a date in the format yyyy-mm-dd".format(
            date_string
        )
        raise argparse.ArgumentTypeError(msg)


# get next id in file
def get_id(file):
    with open(file, "r") as csv_file:
        reader = csv.reader(csv_file)
        reader_list = list(reader)
        id = len(reader_list)
        return id


# get products from bought file by dictreader
def product_list():
    product_list = []
    with open("bought.csv") as csvfile:
        dictreader = csv.DictReader(csvfile)

        for row in dictreader:
            product = row["product"]
            if product not in product_list:
                product_list.append(product)
    product_list.sort()
    return product_list


# compare available quantity to sell from bought and sold file by dictreader
def product_inventory(product, date):
    def quantity_sell():
        # bought and not expired products
        quantity_sell = 0
        with open("bought.csv") as csvfile:
            dictreader = csv.DictReader(csvfile)
            for row in dictreader:
                if (
                    row["product"] == product
                    and row["date"] <= date.strftime("%Y-%m-%d")
                    and row["expiration"] > date.strftime("%Y-%m-%d")
                ):
                    quantity_sell += int(row["quantity"])
            return quantity_sell

    def quantity_sold():
        quantity_sold = 0
        with open("sold.csv") as csvfile:
            dictreader = csv.DictReader(csvfile)
            for row in dictreader:
                if row["product"] == product and row["date"] <= date.strftime(
                    "%Y-%m-%d"
                ):
                    quantity_sold += int(row["quantity"])
            return quantity_sold

    quantity_sell = quantity_sell()
    quantity_sold = quantity_sold()
    product_inventory = quantity_sell - quantity_sold
    return product_inventory


# show product inventory in SuperPy
def inventory(args):
    offered_products = product_list()
    today = date.today()
    if len(offered_products) == 0:
        print("No products found, so SuperPy has no inventory to show")
    else:
        table = []
        for product in offered_products:
            inventory = product_inventory(product, today)
            table.append([product, inventory])
            table_headers = ["Product", "Quantity"]
        print(f'{tabulate(table, headers=table_headers, tablefmt="pretty")}')
    footnote()


# export product inventory to a csv and xlsx file
def inventory_export(args):
    offered_products = product_list()
    today = date.today()
    if len(offered_products) == 0:
        print("No products found, so SuperPy has no inventory to export")
    else:
        table = []
        headers = ["Product", "Quantity"]
        table.insert(0, headers)
        for product in offered_products:
            inventory = product_inventory(product, today)
            table.append([product, inventory])

    if args.format == "csv":
        csv_filename = "inventory.csv"

        with open(csv_filename, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(table)

        console.print(
            f"SuperPy created a [yellow].csv[/yellow] file with the inventory!"
        )
        footnote()

    if args.format == "xlsx":
        xlsx_filename = "inventory.xlsx"

        df = pd.DataFrame(table[1:], columns=headers)
        df.to_excel(xlsx_filename, index=False)

        console.print(
            f"SuperPy created a [yellow].xlsx[/yellow] file with the inventory!"
        )
        footnote()


# modify date in date.txt and confirm to user
def advance_date(args):
    today = date.today()
    days_advanced = args.days
    advance_date = today + timedelta(days_advanced)

    filename = "date.txt"

    with open(filename, "w") as textfile:
        textfile.write(str(advance_date))
        console.print(
            f"The SuperPy's date is changed to: [blue]{advance_date}[/blue] and saved in date.txt"
        )
        footnote()


def working_date():
    with open("date.txt", "r") as file:
        get_date = file.read().strip()
    new_date = datetime.strptime(get_date, "%Y-%m-%d").date()
    return new_date


# get result until entered _date
def result_end_date(filename, date):
    with open(filename) as csvfile:
        dictreader = csv.DictReader(csvfile)
        result = 0
        for row in dictreader:
            if row["date"] <= str(date):
                price_product = row["price"]
                quantity_product = row["quantity"]
                result_product = float(price_product) * float(quantity_product)
                result += result_product
        return result


# get result from entered from_date onwards
def result_start_date(filename, date):
    with open(filename) as csvfile:
        dictreader = csv.DictReader(csvfile)
        result = 0
        for row in dictreader:
            if row["date"] >= str(date):
                price_product = row["price"]
                quantity_product = row["quantity"]
                result_product = float(price_product) * float(quantity_product)
                result += result_product
        return result


# if end_date and start_date both are entered get result from that range
def result_range_date(filename, start_date, end_date):
    with open(filename) as csvfile:
        dictreader = csv.DictReader(csvfile)
        result = 0
        for row in dictreader:
            if row["date"] >= str(start_date) and row["date"] <= str(end_date):
                price_product = row["price"]
                quantity_product = row["quantity"]
                result_product = float(price_product) * float(quantity_product)
                result += result_product
        return result


# get result based on a date (today, yesterday or specific date)
def result_day(filename, day):
    with open(filename) as csvfile:
        dictreader = csv.DictReader(csvfile)
        result = 0
        for row in dictreader:
            if row["date"] == str(day):
                price_product = row["price"]
                quantity_product = row["quantity"]
                result_product = float(price_product) * float(quantity_product)
                result += result_product
        return result


# calculate revenue (total of sold products)
def revenue(args):
    if (
        args.today is None
        and args.yesterday is None
        and args.choose_date is None
        and args.end_date is None
        and args.start_date is None
    ):
        print(
            f"Option need to view the revenue, for help type: [python super.py revenue -h]"
        )
    else:
        if args.today:
            today = date.today()
            revenue = result_day("sold.csv", today)
            console.print(
                f"The revenue on today [blue]{today}[/blue] is: [green]{revenue}[/green]"
            )
            footnote()

        if args.yesterday:
            yesterday = date.today() - timedelta(1)
            revenue = result_day("sold.csv", yesterday)
            console.print(
                f"The revenue on yesterday [blue]{yesterday}[/blue] is: [green]{revenue}[/green]"
            )
            footnote()

        if args.choose_date:
            specific_date = args.choose_date
            revenue = result_day("sold.csv", specific_date)
            console.print(
                f"The revenue on [blue]{specific_date}[/blue] is: [green]{revenue}[/green]"
            )
            footnote()

        if args.end_date and args.start_date is None:
            end_date = args.end_date
            revenue = result_end_date("sold.csv", end_date)
            console.print(
                f"The revenue till [blue]{end_date}[/blue] is: [green]{revenue}[/green]"
            )
            footnote()

        if args.start_date and args.end_date is None:
            start_date = args.start_date
            revenue = result_start_date("sold.csv", start_date)
            console.print(
                f"The revenue from [blue]{start_date}[/blue] onwards is: [green]{revenue}[/green]"
            )
            footnote()

        if args.end_date and args.start_date:
            end_date = args.end_date
            start_date = args.start_date
            revenue = result_range_date("sold.csv", start_date, end_date)
            console.print(
                f"The revenue between [blue]{start_date}[/blue] and [blue]{end_date}[/blue] is: [green]{revenue}[/green]"
            )
            footnote()


# calculate profit (revenue - costs)
def profit(args):
    if (
        args.today is None
        and args.yesterday is None
        and args.choose_date is None
        and args.end_date is None
        and args.start_date is None
    ):
        print(
            f"Option need to view the profit, for help type: [python super.py revenue -h]"
        )
    else:
        if args.today:
            today = date.today()
            revenue = result_day("sold.csv", today)
            cost = result_day("bought.csv", today)
            profit = revenue - cost
            if profit >= 0:
                console.print(
                    f"The profit on today [blue]{today}[/blue] is: [green]{profit}[/green]"
                )
            else:
                console.print(
                    f"The profit on today [blue]{today}[/blue] is: [red]{profit}[/red]"
                )
            footnote()

        if args.yesterday:
            yesterday = date.today() - timedelta(1)
            revenue = result_day("sold.csv", yesterday)
            cost = result_day("bought.csv", yesterday)
            profit = revenue - cost
            if profit >= 0:
                console.print(
                    f"The profit on yesterday [blue]{yesterday}[/blue] is: [green]{profit}[/green]"
                )
            else:
                console.print(
                    f"The profit on yesterday [blue]{yesterday}[/blue] is: [red]{profit}[/red]"
                )
            footnote()

        if args.choose_date:
            specific_date = args.choose_date
            revenue = result_day("sold.csv", specific_date)
            cost = result_day("bought.csv", specific_date)
            profit = revenue - cost
            if profit >= 0:
                console.print(
                    f"The profit on on [blue]{specific_date}[/blue] is: [green]{profit}[/green]"
                )
            else:
                console.print(
                    f"The profit on on [blue]{specific_date}[/blue] is: [red]{profit}[/red]"
                )
            footnote()

        if args.end_date and args.start_date is None:
            end_date = args.end_date
            revenue = result_end_date("sold.csv", end_date)
            cost = result_end_date("bought.csv", end_date)
            profit = revenue - cost
            if profit >= 0:
                console.print(
                    f"The profit till [blue]{end_date}[/blue] is: [green]{profit}[/green]"
                )
            else:
                console.print(
                    f"The profit till [blue]{end_date}[/blue] is: [red]{profit}[/red]"
                )
            footnote()

        if args.start_date and args.end_date is None:
            start_date = args.start_date
            revenue = result_start_date("sold.csv", start_date)
            cost = result_start_date("bought.csv", start_date)
            profit = revenue - cost
            if profit >= 0:
                console.print(
                    f"The total profit from [blue]{start_date}[/blue] onwards is [green]{profit}[/green]"
                )
            else:
                console.print(
                    f"The total profit from [blue]{start_date}[/blue] onwards is [red]{profit}[/red]"
                )
            footnote()

        if args.end_date and args.start_date:
            end_date = args.end_date
            start_date = args.start_date
            revenue = result_range_date("sold.csv", start_date, end_date)
            cost = result_range_date("bought.csv", start_date, end_date)
            profit = revenue - cost
            if profit >= 0:
                console.print(
                    f"The total profit from [blue]{start_date}[/blue] till [blue]{end_date}[/blue] is [green]{profit}[/green]"
                )
            else:
                console.print(
                    f"The total profit from [blue]{start_date}[/blue] till [blue]{end_date}[/blue] is [red]{profit}[/red]"
                )
            footnote()


# buy function with its arguments and saves to bought.csv file
def buy(args):
    if os.path.exists(bought_path):
        filename = "bought.csv"
        next_id = get_id(filename)
        today = date.today()
        data = [
            next_id,
            args.product,
            today,
            args.price,
            args.expiration,
            args.quantity,
        ]

        with open(filename, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

        # confirmation of buy to user
        print("")
        console.print(
            f"Thanks for adding; [green]{args.product.upper()}[/green] is now added to [yellow]bought.csv[/yellow]!"
        )
        print("")
        print(tabulate(pd.read_csv("bought.csv"), headers="keys", tablefmt="pretty"))
        footnote()
    else:
        # Parsed arguments of the new purchase are stored in a dictionary.
        buy = {
            "id": [""],
            "product": [args.product],
            "date": [date.today()],
            "price": [args.price],
            "expiration": [args.expiration],
            "quantity": [args.quantity],
        }
        df_buy = pd.DataFrame(buy)
        new_buy_id = "" + str(df_buy.shape[0])
        df_buy.loc[0, "id"] = new_buy_id
        df_buy.to_csv(bought_path, index=False)
        console.print("A new file: [yellow]bought.csv[/yellow] is created!")
        print("")
        print(tabulate(pd.read_csv("bought.csv"), headers="keys", tablefmt="pretty"))
        footnote()


def buy_show(args):
    if os.path.exists(bought_path):
        console.print(f"The [yellow]bought[/yellow] products list:")
        print("")
        print(tabulate(pd.read_csv("bought.csv"), headers="keys", tablefmt="pretty"))
        footnote()
    else:
        console.print("[red]ERROR[/red]")
        console.print(
            "File [yellow]bought.csv[/yellow] doesn't exists, please first [green]buy[/green] some products before you can see them!"
        )
        print("see [python super.py buy add -h]")
        footnote()


# sell function with its arguments and saves to sold.csv file
def sell(args):
    if os.path.exists(sold_path):
        product = args.product
        selling_date = date.today()
        quantity = args.quantity
        # product_stock() excludes expired products
        inventory = product_inventory(product, selling_date)

        # exclude selling more than is in stock on the selling date
        if inventory < quantity:
            console.print(f"[red]STOCK ERROR[/red]")
            print("")
            console.print(
                f"[green]{product.upper()}[/green] in stock on [blue]{selling_date}[/blue]: [red]{inventory}[/red]."
            )
            console.print(f"That's less than [red]{quantity}[/red] you want to sell!")

        else:
            # append data to csv file
            filename = "sold.csv"
            next_id = get_id(filename)
            today = date.today()
            data = [next_id, args.product, today, args.price, args.quantity]

            with open(filename, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)
            print("")
            console.print(
                f"Thanks for adding your sold product; [green]{args.product.upper()}[/green] is now added to [yellow]sold.csv[/yellow]!"
            )

        print("")
        print(tabulate(pd.read_csv("sold.csv"), headers="keys", tablefmt="pretty"))
        footnote()
    else:
        # Parsed arguments of the new purchase are stored in a dictionary.
        sell = {
            "id": [""],
            "product": [args.product],
            "date": [date.today()],
            "price": [args.price],
            "quantity": [args.quantity],
        }
        df_sell = pd.DataFrame(sell)
        new_sell_id = "" + str(df_sell.shape[0])
        df_sell.loc[0, "id"] = new_sell_id
        df_sell.to_csv(sold_path, index=False)
        console.print("A new file: [yellow]sold.csv[/yellow] is created!")
        print("")
        print(tabulate(pd.read_csv("sold.csv"), headers="keys", tablefmt="pretty"))
        footnote()


def sell_show(args):
    if os.path.exists(sold_path):
        console.print(f"The [yellow]sold[/yellow] products list:")
        print("")
        print(tabulate(pd.read_csv("sold.csv"), headers="keys", tablefmt="pretty"))
        footnote()
    else:
        console.print("[red]ERROR[/red]")
        console.print(
            "File [yellow]sold.csv[/yellow] doesn't exists, please first [green]buy[/green] some products before you can sell!"
        )
        footnote()


# some extra styling on welcome
print("")
print("")
console.print("[yellow]-[/yellow]" * 62)
