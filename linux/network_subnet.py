# Copyright V.V.
import re

def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()

def flog2(x):
    if x <= 0:
        raise ValueError("domain error")
    return x.bit_length() - 1

def mask_to_address(mask):
    return (2**(mask + 1) - 1) * 2**(32 - mask)

def address_to_string(x):
    return f"{x // (256*256*256) % 256}.{x // (256*256) % 256}.{x // 256 % 256}.{x % 256}"

address = [int(x) for x in list(filter(None, re.split(r"\.| |\/", input("Adresa initiala: "))))]
if len(address) == 4:
    mask = int(input("Masca (format X, unde masca e /X): "))
elif len(address) == 5:
    mask = address[4]

address = (address[0] * (2**24)) + (address[1] * (2**16)) + (address[2] * (2**8)) + address[3]
address = address & mask_to_address(mask)

devices = [int(x) for x in input("Dispozitive (separate prin ' ', CU TOT CU router): ").split(' ')]
devices.sort(reverse=True)
log_add_devices = [flog2(next_power_of_2(x + 2)) for x in devices]

print("--------")
for i in range(len(devices)):
    print(f"{devices[i]} => {address_to_string(address)} /{32 - log_add_devices[i]} ({address_to_string(mask_to_address(32 - log_add_devices[i]))})")
    address += 2**log_add_devices[i]
