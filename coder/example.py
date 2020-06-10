AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' * 2  # заданный алфавит

def f(mc, key, op):  
   key *= len(mc)  
   return ''.join([AZ[AZ.index(j) + int(key[i]) * op] for i, j in enumerate(mc)])  

def encrypt(text, key):  
   return f(text, key, 1)  

def decrypt(chiftext, key):  
   return f(chiftext, key, -1)  

if __name__ == "__main__":

    print(encrypt('GRONSFELD', '2015'))  # шифрование  
    print(decrypt('IRPSUFFQF', '2015'))  # расшифровывание