import json
x = {'r1': [{'b':'1'}, {'c':2}],
     'r2': [{'b':'.1'}, {'c':.2}]}


print({key: [list(d.values())[0] for d in v1] for key, v1 in x.items()})
  #  print('lll',(key, value) in [d.items() for d in v1])
  #  z = [(k, v) for k,v in d.items() for d in value]
 #   print(z)