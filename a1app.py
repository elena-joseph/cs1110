"""
User interface for module currency

When run as a script, this module prompts the user for two currencies and
an amount. It prints out the result of converting the first currency to
the second.

Author: Elena Joseph (esj34) & Carly Hu (ch862)
Date:   9/21/2021
"""
import a1

src = input('Enter original currency: ')
dst = input('Enter desired currency: ')
amt = float(input('Enter original amount: '))

print('You can exchange '+ str(amt) + ' ' + src + ' for ' + str(a1.exchange\
(src, dst, amt)) + ' ' + dst + '.')
