I,N=lambda:input().split(),int
*_,y,x,_,_,n=map(N,I())
e={N(f):N(p)for f,p in(I()for _ in range(n))}|{y:x}
while 1:j,k,d=I();print("BLOCK"if(N(k)<(f:=e.get(N(j),y))and d<"M")or(N(k)>f and d>"M")else"WAIT")
