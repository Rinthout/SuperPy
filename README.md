```
    _____                       ____                ___ ___   
   / ___/__  ______  ___  _____/ __ \__  __   _   _<  /|__ \  
   \__ \/ / / / __ \/ _ \/ ___/ /_/ / / / /  | | / / / __/ /  
  ___/ / /_/ / /_/ /  __/ /  / ____/ /_/ /   | |/ / / / __/   
 /____/\__,_/ .___/\___/_/  /_/    \__, /    |___/_(_)____/   
           /_/                    /____/
```

## Welcome to SuperPy v1.2!
#### The powerfull and handy solution to track your supermarkt inventory and determine you profits

## Intro
With this CLI tool you can track all your supermarkt inventory. Add your bought products with product specific data like buy price, expiration date and quantity. And tell the tool what, when, wich price and wich quantity its sold again by option. You can show your bought and sold products. To power of SuperPy is to see what's on stock with the inventory option. If you have that you can also view your revenue and the profits by chosen date ranges (choosen start and and dates).

## Requirements
For a smooth run and a good user experience you have to install the following modules in Pyton:
- python 3.10
- argparse
- datetime 
- pandas
- tabulate
- rich

By missing a module you can easely install them by typing `pip install <modulename>` in terminal.

## Some note for user
- Productnames has te be singelar names in lowercase, like `orange` or `cheesecake`;
- Prices has te be numbers and seperated by dot for two decimals, like `88.88`;
- Dates are always in yyyy-mm-dd, like `2023-06-11`;
- Quantity are always rounded numbers like `3` or `250`;

## Run SuperPy
To enter the progam type the following command in your terminal, typ:
```
python super.py
```
To see the complete table of content in your terminal and its descriptions, type:
```
python super.py -h
```
### Table of content
**advance-adate**
```
    python super.py date advance-date -h
    python super.py date advance-date <days>
```
**buy**
```
    python super.py buy -h
    python super.py buy add <productname> <buy price> <expiration date> <buy quantity>
    python super.py buy show
```
**sell**
```
    python super.py sell -h
    python super.py sell add <productname> <sell price> <sell quantity>
    python super.py sell show
```
**inventory-show**
```
    python super.py inventory -h
    python super.py inventory show
```
**inventory-export**
```
    python super.py inventory-export -h
    python super.py inventory-export <csv> or <xlsx>
```
**revenue**
```
    python super.py revenue -h
    python super.py revenue -today
    python super.py revenue -yesterday
    python super.py revenue -choose_date
    python super.py revenue -start_date
    python super.py revenue -end_date

``` 
**profit**
```
    python super.py profit -h
    python super.py profit -today
    python super.py profit -yesterday
    python super.py profit -choose_date
    python super.py profit -start_date
    python super.py profit -end_date
```


## SuperPy's date
With this CLI tool you can advance your working date. Working date is today's date and you can see it by opening SuperPy. You can change the date by using the `advance-date` command. Automaticly it will be saved in a txt file called `date.txt`.
Date must be entered in format yyyy-mm-dd.

#### Syntax and example
```
python super.py advance-date <days>
```
Suppose it's is today 2023-06-11, if you want to advance it to tomorrow you enter at prompt:
```
python super.py advance-date 1
```
Now you get to see a confirmation this date is saved to `date.txt`

## SyperPy's Buy
Here you can `add` the product you `buy` to the bought list. Give new products logic singular names in lowercase. Than you can add more properties of this bought wares, like `price` (in format 88.88), `expirition` date and `quantity`. Buy date will be automatic fill in by SuperPy and based on today's date. Also each added bought product gets automaticaly an unique id number. After the `buy add` command you get a confirmation and an overview of other bought products (the new product is the last product in list). If this list does not exists yet it will be created by first entered product. Also you can view the the complete bought list without buying by the `show` command.

#### Syntax and example
```
python super.py buy add <product> <price> <yyyy-mm-dd> <quantity>
```
Suppose you want to buy 300 oranges with a expiration date of 2023-08-25 for €0,50 each, you enter at prompt
```
python super.py buy add orange 0.50 2023-08-25 300
```
To show the bought list, enter:
```
python super.py buy show
```

## SyperPy's Sell
Here you can `add` the product you will sell to the sold list. Give sold products the exact same name as in the bought list. Than you can add the `price` (in format 88.88) and its `quantity`. Sell date will be automatic fill in by SuperPy's working date. Also each added sold product gets automaticaly an unique id number. After the add command you get a confirmation and a overview of other sold products (the new sold product is the last product in list). If the list does not exists it will be created on first to sell product. If you want to sell something is not in bought list or the quantity is more than in stock, you get a error. Like buy, you can view the sold list without selling a product: use the `show` command.

#### Syntax and example
```
python super.py sell add <productname> <price> <quantity>
```
Suppose you want to sell 100 oranges for €0,75 each, you enter at prompt:
```
python super.py sell add orange 0.75 100
```
To show the sold list, enter:
```
python super.py sell show
```
## SuperPy's Inventory

## SuperPy's Revenue

## SuperPy's Profit

## Closing words
I hope you can use this powerful program for all you administration. Millions of supermarktmanagers around the world are really enthusiastic. You can see all positive reviews everywhere. Lots of handy features fur such a low price!

Thanks for using SuperPy!








