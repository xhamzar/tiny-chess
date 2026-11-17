import json,os,urllib.request as u
V=[0,100,320,330,500,900,0]
ND=[31,33,14,18,-31,-33,-14,-18]
BD=[15,17,-15,-17]
RD=[1,16,-1,-16]
KD=RD+BD
DT=[0,0,(ND,0),(BD,1),(RD,1),(BD+RD,1),(KD,0)]
C='206550330200220'
P=[[0]*128 for _ in range(7)]
for s in range(128):
 if s&0x88:continue
 f,r=s&7,s>>4;a=min(f,7-f);b=min(r,7-r)
 for t in range(5):x,y,z=map(int,C[t*3:t*3+3]);P[t+1][s]=x*a+y*b+z*r
Z={4:3,116:12,0:2,7:1,112:8,119:4}
S=[];K=[0]*98
def ps(u):return ord(u[0])+16*ord(u[1])-881
def sn(s):return chr(97+s%8)+chr(49+s//16)
def fp(f):
 global B,T,R,Y
 B=[0]*128;a=f.split();r=7;x=0
 for c in a[0]:
  if c<'1':r-=1;x=0
  elif c<'9':x+=int(c)
  else:B[r*16+x]=('pnbrqk'.index(c.lower())+1)*(2*(c<'a')-1);x+=1
 T=a[1]>'v';R=sum(1<<'KQkq'.index(c) for c in a[2] if c in 'KQkq')
 Y=ps(a[3]) if a[3]!='-' else -1
def at(s,w):
 u=2*w-1
 for o in (s-15*u,s-17*u):
  if not o&0x88 and B[o]==u:return 1
 for D,v in ((ND,2),(KD,6)):
  for d in D:
   o=s+d
   if not o&0x88 and B[o]==u*v:return 1
 for D,v in ((BD,3),(RD,4)):
  for d in D:
   o=s+d
   while not o&0x88:
    if B[o] in (u*v,5*u):return 1
    if B[o]:break
    o+=d
 return 0
def ap(m,s,o):m+=[(s,o,q) for q in (5,4,3,2)] if o>>4 in (0,7) else [(s,o,0)]
def gn():
 m=[]
 for s,p in enumerate(B):
  if not p or (p>0)!=T:continue
  t=abs(p)
  if t==1:
   d=32*T-16
   for o in (s+d,s+d-1,s+d+1):
    if o&0x88:continue
    c=B[o]
    if o==s+d:
     if c:continue
     ap(m,s,o)
     if (s>>4)==6-5*T and not B[e:=s+2*d]:m.append((s,e,0))
    elif (c and (c>0)!=T) or o==Y:
     ap(m,s,o)
  else:
   D,sl=DT[t]
   for d in D:
    o=s+d
    while not o&0x88 and (not B[o] or (B[o]>0)!=T):
     m.append((s,o,0))
     if not sl or B[o]:break
     o+=d
   if t==6 and s%112==4:
    for b,d,n in ((1 if s==4 else 4,1,2),(2 if s==4 else 8,-1,3)):
     if R&b and not any(B[s+d*i] for i in range(1,n+1)) and not any(at(s+d*i,not T) for i in range(3)):m.append((s,s+2*d,0))
 return m
def cr(f,t):
 x,y=(t-1,t+1) if t>f else (t+1,t-2);B[x],B[y]=B[y],B[x]
def mk(m):
 global T,R,Y
 f,t,q=m;p=B[f];z=abs(p);c=B[t];y=t
 if z==1 and t==Y and not c:y=t+16-32*T;c=B[y];B[y]=0
 S.append((m,c,y,R,Y))
 B[t]=q*(2*T-1) if q else p;B[f]=0
 if z==6 and abs(t-f)==2:cr(f,t)
 R&=~(Z.get(f,0)|Z.get(t,0))
 Y=(f+t)//2 if abs(t-f)==32 and z==1 else -1
 T=not T
def un():
 global T,R,Y
 m,c,y,R,Y=S.pop();f,t,q=m;p=B[t]
 B[f]=(1-2*T) if q else p;B[t]=0;B[y]=c
 if abs(p)==6 and abs(t-f)==2:cr(f,t)
 T=not T
def sr(d,a,b,pl):
 global N,T
 N+=1
 if N>8e4:return None
 k=(tuple(B),T,R,Y);q=d<=0
 if q:
  s=0
  for x,p in enumerate(B):
   if p:
    z=abs(p);v=V[z]+P[z][x^(112*(p<0))];s+=v*(p>0 or -1)
  if not T:s=-s
  if pl>50:return s
  if s>=b:return b
  if s>a:a=s
  ms=[m for m in gn() if B[m[1]]]
 else:
  e=TT.get(k);mo=0
  if e:
   mo=e[3]
   if e[0]>=d and(e[1]==0 or e[2]>=b and e[1]==1 or e[2]<=a and e[1]==2):return e[2]
  ks=B.index(6*(2*T-1))
  if d>2 and not at(ks,not T):
   T=not T;r=sr(d-2,-b,-b+1,pl+1);T=not T
   if N<=8e4 and -r>=b:return b
  ms=gn();ms.sort(key=lambda m:-(m==mo)*1e4-(m==K[pl])*1e4-V[abs(B[m[1]])])
 be=0;nl=0;fl=2
 for m in ms:
  mk(m)
  if at(B.index(6*(1-2*T)),T):un();continue
  nl+=1
  r=sr(max(d-1,0),-b,-a,pl+1);un()
  if r is None:return None
  s=-r
  if s>=b:K[pl]=m;TT[k]=(d,1,s,m);return s
  if s>a:a=s;be=m;fl=0
 if not nl and not q:return(-1e5+pl)*at(ks,not T)
 TT[k]=(d,fl,a,be)
 return a
def uc(m):
 f,t,q=m;return sn(f)+sn(t)+(q and 'nbrq'[q-2] or '')
def ch(f,legal):
 fp(f)
 ms=[(ps(u[:2]),ps(u[2:4]),('nbrq'.find(u[4:])+2)*(len(u)>4)) for u in legal]
 global N,TT,K
 N=0;TT={};K=[0]*98
 bm=ms[0]
 for d in range(1,99):
  a=-1e6;be=0
  for m in ms:
   mk(m);r=sr(d-1,-1e6,-a,1);un()
   if r is None:return uc(bm)
   s=-r
   if s>a:a=s;be=m
  bm=be
 return uc(bm)
def post(p,b):return json.load(u.urlopen(U+p,json.dumps(b).encode()))
if __name__=='__main__':
 U=os.environ['MAKEFUN_ENV_URL']
 while 1:
  g=post('/game',{})
  if g['status']=='done':break
  while g['status'][0]=='y':
   L=g['legal_moves']
   try:mv=ch(g['fen'],L)
   except:mv=L[0]
   g=post('/move',{'game':g['game'],'move':mv})
