AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_ .,-()' * 2  # заданный алфавит

def f(mc, key, op):  
   key *= len(mc)  
   return ''.join([AZ[AZ.index(j) + int(key[i]) * op] for i, j in enumerate(mc)])  

def encrypt(text, key):  
   return f(text, key, 1)  

def decrypt(chiftext, key):  
   return f(chiftext, key, -1)  
