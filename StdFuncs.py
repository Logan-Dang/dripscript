from DripVariable import DripVariable

def drip_print(*args):
  formatted_args = ()
  for arg in args:
    if isinstance(arg, DripVariable):
      formatted_args += (arg.value,)
    else:
      formatted_args += (arg,)
  print(*formatted_args)
  
std_funcs = { 'yap': drip_print }