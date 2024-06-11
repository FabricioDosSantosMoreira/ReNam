import hashlib

str_art = """
                _____      _   _
                |  __ \\    | \\ | |
                | |__) |___|  \\| | __ _ _ __ ___ 
                |  _  // _ \\ . ` |/ _` | '_ ` _ \\   
                | | \\ \\  __/ |\\  | (_| | | | | | | 
                |_|  \\_\\___|_| \\_|\\__,_|_| |_| |_|  
            """   

# Calculando o hash SHA-256 da string
hash_object = hashlib.sha256(str_art.encode())
hex_dig = hash_object.hexdigest()

hashlib.new
print("SHA-256 Hash da string:")
print(hex_dig)

# Convertendo o hash de volta para bytes
bytes_from_hash = bytes.fromhex(hex_dig)

print(bytes_from_hash)
