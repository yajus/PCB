import sys
import json
import urllib
import httplib
server_host = '10.10.0.2'
server_port=80
def summit(team_token,flag,host=server_host,port=server_port,timeout=5):
    if not team_token or not flag:
        raise  Exception('team token or flag not found')
    conn = httplib.HTTPConnection(host,port,timeout=timeout)
    params=urllib.urlencode({
        'token':team_token,
        'flag:':flag,
    })
    headers={
        "Content-type":"application/x-www-form-urlencoded"
    }
    conn.request('POST','/api/sumit_flag',params,headers)
    response=conn.getresponse()
    data=response.read()
    return json.loads(data)
if __name__=='__main__':
    if len(sys.argv)<3:
        print 'usage: ./submitflag.py $team_token $flag'
        sys.exit()
    host=server_host
    if len(sys.argv)>3:
        host=sys.argv[3]
    print json.dumps(summit(sys.argv[1],sys.argv[2],host=host),indent=4)