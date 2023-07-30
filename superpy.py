import argparse
from datetime import date
from rich.console import Console
from functions import (
    valid_date,
    inventory,
    inventory_export,
    advance_date,
    revenue,
    profit,
    buy,
    buy_show,
    sell,
    sell_show,
)


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Create a console object
console = Console()

# SyperPy's welcome
print("")
console.print(
    "[blue]    _____                       ____                ___ ___   [/blue]"
)
console.print(
    "[blue]   / ___/__  ______  ___  _____/ __ \__  __   _   _<  /|__ \  [/blue]"
)
console.print(
    "[blue]   \__ \/ / / / __ \/ _ \/ ___/ /_/ / / / /  | | / / / __/ /  [/blue]"
)
console.print(
    "[blue]  ___/ / /_/ / /_/ /  __/ /  / ____/ /_/ /   | |/ / / / __/   [/blue]"
)
console.print(
    "[blue] /____/\__,_/ .___/\___/_/  /_/    \__, /    |___/_(_)____/   [/blue]"
)
console.print(
    "[blue]           /_/                    /____/                      [/blue]"
)
print("")
print("")

console.print(
    "[yellow]-[/yellow]" * 26, "[blue]WELCOME![/blue]", "[yellow]-[/yellow]" * 26
)
print("")


def main():
    ########################################## PARSER #######################################
    # The base parser of the CLI tool
    parser = argparse.ArgumentParser(
        prog="SuperPy v1.2",
        usage="%(prog)s [options]",
        description="Welcome to the ulitmate tool for tracking your supermarket inventory!",
        epilog=(
            "--------------------------- Thanks for using SuperPy! --------------------------"
        ),
    )

    #  Subparser
    subparsers = parser.add_subparsers(
        title="subcommands", prog="python super.py", dest="subcommand"
    )

    ######################################### DATE ##########################################
    # create the parser for the "advance-time" subcommand
    parser_advance_time = subparsers.add_parser(
        "advance-date",
        help="enter the numbers of days to change the SuperPy's working date",
    )

    parser_advance_time.add_argument(
        "days",
        type=int,
        help="advance date [number of days] (e.g. 1 is tomorrow, -1 is yesterday)",
    )

    parser_advance_time.set_defaults(func=advance_date)

    ######################################### BUY ###########################################
    # buy parser
    parser_buy = subparsers.add_parser(
        "buy",
        usage="%(prog)s [options]",
        help="add and show your bought product",
    )
    parser_buy_sub = parser_buy.add_subparsers(
        dest="sub-subcommand",
        help="add and show your bought product",
    )
    # buy add parser with its arguments
    parser_buy_add_sub = parser_buy_sub.add_parser(
        "add", usage="%(prog)s [options]", help="add your bought product"
    )

    parser_buy_add_sub.add_argument("product", help="enter here the name of product")
    parser_buy_add_sub.add_argument(
        "price",
        type=float,
        help="enter here the buy price of product (format: 88.88)",
    )
    parser_buy_add_sub.add_argument(
        "expiration",
        type=valid_date,
        help="enter here the expiration date of product (format: yyyy-mm-dd)",
    )
    parser_buy_add_sub.add_argument(
        "quantity", type=int, help="enter here the quantity of product"
    )
    parser_buy_add_sub.set_defaults(func=buy)

    # buy show parser
    parser_buy_show_sub = parser_buy_sub.add_parser(
        "show",
        usage="%(prog)s [options]",
        help="show your bought product",
    )
    parser_buy_show_sub.set_defaults(func=buy_show)

    ######################################### SELL ##########################################
    # sell parser
    parser_sell = subparsers.add_parser(
        "sell",
        help="add and show your sold products",
    )

    parser_sell_sub = parser_sell.add_subparsers(
        dest="sub-subcommand",
        help="add and show your sold product",
    )
    # sell add subparser and its arguments
    parser_sell_add_sub = parser_sell_sub.add_parser(
        "add",
        usage="%(prog)s [options]",
        help="add your sold products",
    )

    parser_sell_add_sub.add_argument("product", help="enter here the name of product")
    parser_sell_add_sub.add_argument(
        "price",
        type=float,
        help="enter here the sell price of product (format: 88.88)",
    )
    parser_sell_add_sub.add_argument(
        "quantity", type=int, help="enter here the quantity of product"
    )
    parser_sell_add_sub.set_defaults(func=sell)

    # sell show parser
    parser_sell_show_sub = parser_sell_sub.add_parser(
        "show",
        usage="%(prog)s [options]",
        help="show your sold products",
    )
    parser_sell_show_sub.set_defaults(func=sell_show)

    ######################################### INVENTORY #######################################
    # inventory parser
    parser_inventory_show = subparsers.add_parser(
        "inventory",
        help="show the inventory",
    )
    parser_inventory_show.add_argument(
        "show",
        type=str,
        help="show the inventory on today",
    )
    parser_inventory_show.set_defaults(func=inventory)

    # inventory export parser and its format argument (choose between csv or xlsx)
    parser_inventory_export = subparsers.add_parser(
        "inventory-export",
        help="export inventory",
    )
    parser_inventory_export.add_argument(
        "format",
        type=str,
        choices=["csv", "xlsx"],
        help="enter [csv] or [xlsx] to export to format to .csv or .xlsx",
    )

    parser_inventory_export.set_defaults(func=inventory_export)

    ######################################## REVENUE ########################################
    # revenue parser and its date arguments
    parser_revenue = subparsers.add_parser(
        "revenue",
        help="show the revenue, options: today, yesterday, choosen date, date range",
    )
    parser_revenue.add_argument(
        "-today", action="store_const", const="today", help="show the revenue on today"
    )
    parser_revenue.add_argument(
        "-yesterday",
        action="store_const",
        const="yesterday",
        help="show the revenue on yesterday",
    )
    parser_revenue.add_argument(
        "-choose_date",
        type=valid_date,
        metavar="",
        help="show the revenue on a choosen date",
    )
    parser_revenue.add_argument(
        "-start_date",
        type=valid_date,
        metavar="",
        help="show the revenue from a choosen start date, also to combine with -end_date",
    )
    parser_revenue.add_argument(
        "-end_date",
        type=valid_date,
        metavar="",
        help="show the revenue till a choosen end date, also to combine with -start_date",
    )
    parser_revenue.set_defaults(func=revenue)

    ######################################### PROFIT ########################################
    # profit argument and its date arguments
    parser_profit = subparsers.add_parser(
        "profit",
        description="show the profit",
        help="show the profit, options: today, yesterday, choosen date and date range",
    )
    parser_profit.add_argument(
        "-today", action="store_const", const="today", help="show the profit on today"
    )
    parser_profit.add_argument(
        "-yesterday",
        action="store_const",
        const="yesterday",
        help="show the profit on yesterday",
    )
    parser_profit.add_argument(
        "-choose_date",
        type=valid_date,
        metavar="",
        help="show the profit on a choosen date",
    )
    parser_profit.add_argument(
        "-start_date",
        type=valid_date,
        metavar="",
        help="show the profit from a choosen start date, also to combine with -end_date",
    )
    parser_profit.add_argument(
        "-end_date",
        type=valid_date,
        metavar="",
        help="show the profit till a choosen end date, also to combine with -start_date",
    )
    parser_profit.set_defaults(func=profit)

    # Parse the arguments with the function
    args = parser.parse_args()

    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)


# print the date on welcome
console.print(f"The SuperPy's working date is today: [blue]{date.today()}[/blue]")
print("")


if __name__ == "__main__":
    main()
