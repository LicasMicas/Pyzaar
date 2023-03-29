# modules
import requests
from pynput import keyboard

# explains how to start
print('Press F10 to update bazaar \nPress ESC to exit')

# checks for key input
def on_release(key):
    if key == keyboard.Key.f10:

        # user choice to filter enchantments
        filter = input('Would you like to filter enchantments? y/n \n')

        # calls sort_products
        sort_products(filter)

    elif key == keyboard.Key.esc:

        # exits program
        return False

# takes all useful information from products and places it into dict to be sorted
def sort_products(filter):

    # creates dictionary
    dict = {}

    # all products on bazaar as a dictionary
    products = requests.get('https://api.hypixel.net/skyblock/bazaar').json()['products']

    # iterates through products
    for i in products:

        # checks for filter
        if (filter.lower() == 'y' and 'ENCHANTMENT' not in products[i]['quick_status']['productId']) or (filter.lower() == 'n'):
                
            # calculate profit of each item
            profit = products[i]['quick_status']['buyPrice']-products[i]['quick_status']['sellPrice']

            # calculates profit percentage
            if products[i]['quick_status']['buyPrice'] != 0:
                percentage = round((profit/products[i]['quick_status']['buyPrice'])*100, 1)
            else:
                percentage = 0

            # adds a key (profit) and value (string of information) to the dictionary
            if profit >= 0:
                dict[profit] = (f"\u001b[1m {products[i]['quick_status']['productId'].center(40)} \u001b[22m|\u001b[32m {str(round(profit, 1)).center(20)} profit per item \u001b[m|{str(products[i]['quick_status']['sellVolume']).center(10)} sell volume |{str(products[i]['quick_status']['buyVolume']).center(10)} buy volume | {str(percentage).center(5)}% profit")
            else:
                dict[profit] = (f"\u001b[1m {products[i]['quick_status']['productId'].center(40)} \u001b[22m|\u001b[31m {str(round(abs(profit), 1)).center(20)} loss per item   \u001b[m|{str(products[i]['quick_status']['sellVolume']).center(10)} sell volume |{str(products[i]['quick_status']['buyVolume']).center(10)} buy volume | {str(percentage).center(5)}% profit")

    # sorts the dictionary by key(profit)
    for i in sorted(dict):
        print(dict[i])

# collects keyboard events
with keyboard.Listener(on_release=on_release) as listener:
    listener.join()

# starts the listener for the keyboard
listener = keyboard.Listener(on_release=on_release)
listener.start()