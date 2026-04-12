N = int(input())
hex_value = hex(N)[2:].upper()
if len(hex_value) == 1:
    hex_value = "0" + hex_value
print(hex_value)