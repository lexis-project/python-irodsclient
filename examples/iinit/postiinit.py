import hashlib
import re

# using same method as auth_microservice/token_service/util.py:sha256
def sha256(s):
      hasher = hashlib.sha256()
      hasher.update(s.encode('utf-8'))
      return hasher.hexdigest()

f= open(".irodsA","r")
contents=f.read()
f.close()

m=re.search ("act=([^;]*);sid=(.*)", contents)

token=m.group(1)
sid=m.group(2)

if len(token)>1024:
   token=sha256(token)

f=open (".irodsA", "w+")
f.write ("act="+token+";sid="+sid)
f.close()

