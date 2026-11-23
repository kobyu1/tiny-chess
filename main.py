import json,os,urllib.request
V=(0,100,320,330,500,900);C=(0,2,4,6,6,4,2,0)
SQ=[21+10*r+f for r in range(8)for f in range(8)]
KN=(-21,-19,-12,-8,8,12,19,21)
BD=(-11,-9,9,11)
RD=(-10,-1,1,10)
KD=BD+RD
CR={98:1,91:2,28:4,21:8}
CAS=((1,95,97,98,(96,97),(95,96,97)),(2,95,93,91,(92,93,94),(93,94,95)))
ND=[0];TT={};K6=(14,6)
Out=Exception
def at(B,s,w):
 z=8*(not w);d=2*w-1
 if 1+z in (B[s+9*d],B[s+11*d]):return True
 if any(B[s+dd]==2+z for dd in KN):return True
 for dd in KD:
  j=s+dd
  if B[j]==6+z:return True
  while B[j]==0:j+=dd
  if B[j]==5+z or (B[j]==3+z if dd in BD else B[j]==4+z):return True
 return False
def ic(B,w):return at(B,B.index(K6[w]),not w)
def gen(B,w,c,e):
 for i in SQ:
  p=B[i];b=p&7
  if not p or (p<9)!=w:continue
  if b==1:
   d=-10*(2*w-1)
   for dd in (d-1,d,d+1):
    j=i+dd;q=B[j]
    if dd==d and q or dd!=d and not(q and q!=255 and (q<9)!=w or e and j==e):continue
    for pr in (5,4,3,2)if j//10==2+7*(not w) else (0,):yield i,j,pr
    if dd==d and i//10==8-5*(not w) and not B[i+2*d]:yield i,i+2*d,0
  else:
   dirs=(KN,BD,RD,KD,KD)[b-2]
   for d in dirs:
    j=i+d;q=B[j]
    while q==0:
     yield i,j,0
     if b in (2,6):break
     j+=d;q=B[j]
    if q and q!=255 and (q<9)!=w:yield i,j,0
   if b==6:
    o=70*(not w)
    for bit,kf,kt,rf,es,ss in CAS:
     if c&(bit<<2*(not w)) and B[rf-o]==4+8*(not w) and not any(B[x-o] for x in es) and not any(at(B,x-o,not w) for x in ss):yield kf-o,kt-o,0
def do(B,c,e,m):
 i,j,pr=m
 N=B[:];p=N[i];w=p<9;b=p&7;N[i]=0
 N[j]=pr+(not w)*8 if pr else p;ne=0
 if b==1:
  if e and j==e and not B[j] and i%10!=j%10:N[j+10*(2*w-1)]=0
  elif abs(j-i)==20:ne=(i+j)//2
 elif b==6:
  if abs(j-i)==2:
   f,t=(j+1,j-1) if j>i else (j-2,j+1);N[t],N[f]=N[f],0
  c&=~3 if w else ~12
 c&=~CR.get(i,0)&~CR.get(j,0)
 return N,c,ne
def leg(B,w,c,e,q=0):
 ks=B.index(K6[w])
 return [m for m in gen(B,w,c,e) if (not q or B[m[1]] or m[2]) and not at(do(B,c,e,m)[0],m[1] if B[m[0]]&7==6 else ks,not w)]
def ev(B):
 s=0;K=[0,0];nq=0
 for k in range(64):
  p=B[SQ[k]]
  if not p:continue
  b=p&7;kk=k^(56*(p>8))
  if b==6:K[p<9]=kk
  else:s+=(V[b]+(C[kk&7]+C[kk>>3])*(1,5,3,2,2)[b-1]//2+(7-(kk>>3))*6*(b==1))*(2*(p<9)-1);nq+=b==5
 def kg(z):return 5*(C[z&7]+C[z>>3]) if not nq else 30-4*C[z>>3]-3*C[z&7]
 return s+kg(K[1])-kg(K[0])
def od(B,mvs,tt):
 return sorted(mvs,key=lambda m:(m==tt,V[B[m[1]]&7]*16+V[m[2]] if B[m[1]] or m[2] else 0),reverse=True)
def sr(B,w,c,e,dep,al,be,ply):
 ND[0]+=1
 assert ND[0]<=85000
 if dep<=0:
  chk=ic(B,w);tm=None
  if not chk:
   st=ev(B)*(2*w-1)
   if st>=be:return be
   al=max(al,st)
  mvs=leg(B,w,c,e,not chk)
  if not mvs:return -100000+ply if chk else al
 else:
  key=(bytes(B),w);tm=TT.get(key)
  mvs=leg(B,w,c,e)
  if not mvs:return -100000+ply if ic(B,w) else 0
 a=al;bm=mvs[0]
 for m in od(B,mvs,tm):
  N,nc,ne=do(B,c,e,m)
  s=-sr(N,not w,nc,ne,dep-1,-be,-a,ply+1)
  if s>a:a,bm=s,m
  if a>=be:break
 if dep>0:TT[key]=bm
 return a
def top(B,w,c,e):
 mvs=leg(B,w,c,e)
 ND[0]=0;pick=mvs[0]
 for dep in range(9):
  try:
   al=-200000
   for m in od(B,mvs,pick):
    N,nc,ne=do(B,c,e,m)
    s=-sr(N,not w,nc,ne,dep-1,-200000,-al,1)
    if s>al:al,pick=s,m
  except Out:break
 return pick
def fen(f):
 t=f.split();B=[255]*120
 for i in SQ:B[i]=0
 i=21
 for ch in t[0]:
  if ch=="/":i+=2
  elif ch.isdigit():i+=int(ch)
  else:
   b="pnbrqk".index(ch.lower())+1
   B[i]=b if ch.isupper() else b+8
   i+=1
 w=t[1]=="w"
 c=sum(1<<n for n in range(4) if "KQkq"[n] in t[2])
 e=0
 if t[3]!="-":e=(10-int(t[3][1]))*10+ord(t[3][0])-96
 return B,w,c,e
def main():
 url=os.environ["MAKEFUN_ENV_URL"]
 def post(path,body):
  return json.load(urllib.request.urlopen(urllib.request.Request(url+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})))
 while True:
  g=post("/game",{})
  if g["status"]=="done":return
  while g["status"]=="your_move":
   B,w,c,e=fen(g["fen"])
   i,j,pr=top(B,w,c,e)
   u=chr(96+i%10)+str(10-i//10)+chr(96+j%10)+str(10-j//10)+("nbrq"[pr-2] if pr else "")
   g=post("/move",{"game":g["game"],"move":u})
main()
