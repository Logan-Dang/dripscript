def drip_print(*args):
  def boolstr(b):
    if type(b) != bool:
      return str(b)
    if b == True:
      return 'onGod'
    elif b == False:
      return 'cap'
  print(*(boolstr(arg) for arg in args))
  
std_funcs = { 'yap': drip_print }