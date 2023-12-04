from DripVariable import DripVariable

def drip_print(*args):
  def boolstr(b):
    if b == True:
      return 'onGod'
    elif b == False:
      return 'cap'
    return str(b)
  print(*(boolstr(arg) for arg in args))
  
std_funcs = { 'yap': drip_print }