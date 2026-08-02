def bank(tax,price,profit):
   tax_rate=price+tax+profit
   final_price = tax_rate+price*profit/2
   print(f"final price {final_price}")

bank(20,40,60)