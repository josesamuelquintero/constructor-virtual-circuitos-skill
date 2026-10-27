"""Generador y verificador de circuitos .txt v0.9.7 (ver SKILL.md, seccion 7)."""
from dataclasses import dataclass, field
TIPOS = {0:("Protoboard",877,276,132),1:("Interruptores",206,81,10),2:("Pulsadores",206,81,10),
         3:("Leds",203,58,9),4:("FuenteDC",77,128,2),5:("Temporizador",206,81,6),6:("SieteSeg",449,130,33),8:("PLA",0,0,0)}
def hit(v,o,p,n):
    r=v-o
    if r<0 or r//p>=n or r%p>8: return None
    return r//p
def pb_hole(ex,ey,reg,a,b):
    return {1:(ex+27+13*a,ey+66+13*b),2:(ex+27+13*a,ey+157+13*b),3:(ex+53+13*a,ey+14+13*b),4:(ex+53+13*a,ey+248+13*b)}[reg]
def pb_port_at(ex,ey,x,y):
    for reg,ox,oy,na,nb in ((1,23,62,64,5),(2,23,153,64,5),(3,49,10,60,2),(4,49,244,60,2)):
        a=hit(x,ex+ox,13,na); b=hit(y,ey+oy,13,nb)
        if a is not None and b is not None: return {1:a,2:64+a,3:128+b,4:130+b}[reg]
sw_hole=lambda ex,ey,c,r:(ex+56+19*c,ey+11+13*r)
SW_VCC=lambda ex,ey:(ex+15,ey+11); SW_GND=lambda ex,ey:(ex+15,ey+69)
led_hole=lambda ex,ey,c:(ex+46+20*c,ey+44); LED_GND=lambda ex,ey:(ex+11,ey+37)
DC_VCC=lambda ex,ey,r:(ex+61,ey+14+13*r); DC_GND=lambda ex,ey,r:(ex+61,ey+74+13*r)
TM_HOLE=lambda ex,ey,c,r:(ex+59+38*c,ey+11+13*r)
SEG_VCC=lambda ex,ey:(ex+16,ey+27)
SEG_PORT=lambda ex,ey,disp,s:(ex+37+13*(8*disp+s),ey+123)   # s: 0..7 = a,b,c,d,e,f,g,punto

def pin_col(a,n,p):
    """Pin p (1..n) de un DIP de n pines con el chip colocado en la columna a -> (region, columna).
    region 2 = tira inferior (pines 1..n/2), region 1 = tira superior (pines n/2+1..n)."""
    return (2,a+p-1) if p<=n//2 else (1,a+(n-p))
def libre(pb,reg,col,k):
    """k-esimo agujero libre (0..3) de la columna: usar uno distinto por cada cable."""
    return pb_hole(pb["ex"],pb["ey"],reg,col,(3-k) if reg==1 else (1+k))

def port_at(t,x,y):
    tipo,ex,ey,tid=t["tipo"],t["ex"],t["ey"],t["id"]
    near=lambda p:abs(x-p[0])<=4 and abs(y-p[1])<=4
    if tipo==0:
        n=pb_port_at(ex,ey,x,y); return None if n is None else (tid,n)
    if tipo in (1,2,5):
        c=hit(x,ex+(52 if tipo!=5 else 55),19 if tipo!=5 else 38,8 if tipo!=5 else 4); r=hit(y,ey+7,13,3)
        if c is not None and r is not None: return (tid,c)
        if near(SW_VCC(ex,ey)): return (tid,"V")
        if near(SW_GND(ex,ey)): return (tid,"G")
    if tipo==3:
        c=hit(x,ex+42,20,8)
        if c is not None and hit(y,ey+40,13,1) is not None: return (tid,c)
        if near(LED_GND(ex,ey)): return (tid,"G")
    if tipo==4:
        for g,oy in (("V",10),("G",70)):
            if 0<=x-(ex+57)<=8 and 0<=y-(ey+oy)<=47 and (y-ey-oy)%13<=8: return (tid,g)
    if tipo==6:
        if near(SEG_VCC(ex,ey)): return (tid,"T")
        c=hit(x,ex+33,13,32)
        if c is not None and hit(y,ey+119,13,1) is not None: return (tid,c)

@dataclass
class Circuito:
    tableros:list=field(default_factory=list); timer_visible:int=0
    cables:list=field(default_factory=list); chips:list=field(default_factory=list)
    _id:int=1; _base:int=0
    def __post_init__(self):                       # dos tableros fijos de todo circuito nuevo
        self.dc=self.tablero(4,10,175); self.tm=self.tablero(5,80,400)
    def tablero(self,tipo,ex,ey):
        _,w,h,n=TIPOS[tipo]; t=dict(tipo=tipo,ex=ex,ey=ey,w=w,h=h,base=self._base,id=self._id)
        self._base+=n; self._id+=1; self.tableros.append(t); return t
    def _tab_en(self,p):
        return next((t for t in self.tableros if port_at(t,*p)),None)
    def cable(self,a,b,color=16711680,ancho=5):
        (ax,ay),(bx,by)=a,b; ta,tb=self._tab_en(a),self._tab_en(b)
        assert ta and tb, "extremo fuera de agujero: %s %s"%(a,b)
        self.cables.append(dict(color=color,ancho=ancho,pts=[ax,ay,ax,ay,bx,ay,bx,ay,bx,by,bx,by],ia=ta["id"],ib=tb["id"]))
    def chip(self,codigo,pines,pb=None,a=0):
        """pb=None: chip suelto en (20,50). Con pb y columna a: insertado; (hx,hy) = R1 fila 4 columna a (= pin n)."""
        if pb is None: ux,uy,pid=20,50,0
        else:
            hx,hy=pb_hole(pb["ex"],pb["ey"],1,a,4); ux,uy,pid=hx-6,hy,pb["id"]
        self.chips.append(dict(codigo=codigo,etiqueta=1,pines=pines,ux=ux,uy=uy,dx=5,dy=0,cx=0,cy=0,pb=pid))
    def texto(self):
        L=["Version 0.9.7",str(len(self.tableros))]
        L+=[" %d %d %d %d %d %d %d"%(t["tipo"],t["ex"],t["ey"],t["w"],t["h"],t["base"],t["id"]) for t in self.tableros]
        L+=[" %d"%self.timer_visible,str(len(self.cables))]
        L+=[" %d %d %s 0 %d 0 %d"%(c["color"],c["ancho"]," ".join(map(str,c["pts"])),c["ia"],c["ib"]) for c in self.cables]
        L.append(str(len(self.chips)))
        L+=[" %d %d %d %d %d %d %d %d %d %d"%(k["codigo"],k["etiqueta"],k["pines"],k["ux"],k["uy"],k["dx"],k["dy"],k["cx"],k["cy"],k["pb"]) for k in self.chips]
        return "\n".join(L)+"\n"

def netlist(txt):
    """Relee el texto como el programa; devuelve (chips, grupos_de_nodos_unidos_por_cables, problemas).
    Tambien avisa si dos cables comparten el mismo agujero (el programa solo admite uno)."""
    tok=txt.split(); assert tok[:2]==["Version","0.9.7"]; p=2; n=int(tok[p]); p+=1; tabs=[]
    for _ in range(n):
        tipo,ex,ey,w,h,base,tid=map(int,tok[p:p+7]); p+=7; tabs.append(dict(tipo=tipo,ex=ex,ey=ey,id=tid))
    p+=1; nc=int(tok[p]); p+=1; uf={}; prob=[]; usados={}
    def find(x):
        uf.setdefault(x,x)
        while uf[x]!=x: uf[x]=uf[uf[x]]; x=uf[x]
        return x
    def agujero(t,x,y):   # identificador exacto del agujero (no solo del nodo)
        return (t["id"],) + ((x-t["ex"])//13*0+0,) if False else (t["id"],x,y)
    for i in range(nc):
        v=list(map(int,tok[p:p+18])); p+=18; pts=v[2:14]; ends=[]
        for e in ((pts[0],pts[1]),(pts[10],pts[11])):
            h=next((q for t in tabs if (q:=port_at(t,*e))),None)
            if h is None: prob.append("cable %d: extremo %s fuera de todo agujero"%(i,e))
            else:
                t=next(t for t in tabs if port_at(t,*e)); k=(t["id"],)+tuple(e)
                if k in usados: prob.append("cable %d: agujero %s ya usado por el cable %d"%(i,e,usados[k]))
                usados[k]=i
            ends.append(h)
        if all(ends): uf[find(ends[0])]=find(ends[1])
    nk=int(tok[p]); p+=1; chips=[]
    for _ in range(nk):
        cod,et,pin,ux,uy,dx,dy,cx,cy,pid=map(int,tok[p:p+10]); p+=10
        if pid==0: chips.append((cod,"suelto",None,pin)); continue
        pb=next(t for t in tabs if t["id"]==pid and t["tipo"]==0)
        nodo=pb_port_at(pb["ex"],pb["ey"],ux+dx,uy+dy)
        if nodo is None or nodo>=64 or hit(uy+dy,pb["ey"]+62,13,5)!=4 or nodo+pin//2>64: prob.append("chip %d no insertable"%cod)
        else: chips.append((cod,pid,nodo,pin))
    g={}
    for k in list(uf): g.setdefault(find(k),[]).append(k)
    return chips,[sorted(map(str,x)) for x in g.values()],prob

if __name__=="__main__":
    c=Circuito(); pb=c.tablero(0,300,60); sw=c.tablero(1,10,350); led=c.tablero(3,300,380)
    A=20; c.chip(7000,14,pb,A); D=c.dc
    H=lambda reg,a,b:pb_hole(pb["ex"],pb["ey"],reg,a,b)
    c.cable(DC_VCC(D["ex"],D["ey"],0),SW_VCC(10,350)); c.cable(DC_GND(D["ex"],D["ey"],0),SW_GND(10,350))
    c.cable(DC_GND(D["ex"],D["ey"],1),LED_GND(300,380))
    c.cable(DC_VCC(D["ex"],D["ey"],1),H(3,0,0)); c.cable(DC_GND(D["ex"],D["ey"],2),H(3,0,1))   # rieles
    c.cable(H(3,3,0),H(1,A,3))        # Vcc -> pin 14 (R1, columna A)
    c.cable(H(3,9,1),H(2,A+6,1))      # GND -> pin 7 (R2, columna A+6)
    c.cable(sw_hole(10,350,0,0),H(2,A,1)); c.cable(sw_hole(10,350,1,0),H(2,A+1,1))   # SW0->pin1, SW1->pin2 (R2)
    c.cable(H(2,A+2,1),led_hole(300,380,0))                                          # pin3 -> LED0
    open("nand.txt","w").write(c.texto()); print(netlist(c.texto()))
