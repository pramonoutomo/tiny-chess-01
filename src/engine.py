import json,os,sys,urllib.request as W
bb=[0]*128
sd=1
ep=-1
cs=0
hm=0
kk=[0,0]
uu=[]
nn=[0,0]
oo={2:(14,18,-14,-18,31,33,-31,-33),3:(15,17,-15,-17),4:(1,16,-1,-16),5:(1,16,-1,-16,15,17,-15,-17),6:(1,16,-1,-16,15,17,-15,-17)}
ss=(0,0,0,1,1,1,0)
Y=lambda i:(i>>3)*16+(i&7)
def load(fen):
    global sd,ep,cs,hm
    bb[:]=[0]*128
    rk,fl=7,0
    p=fen.split()
    for ch in p[0]:
        if ch=='/':
            rk-=1;fl=0
        elif ch.isdigit():
            fl+=int(ch)
        else:
            bb[rk*16+fl]=("PNBRQK".index(ch.upper())+1)*(1 if ch.isupper() else -1)
            fl+=1
    sd=1 if p[1]=='w' else -1
    cs=0
    for ch in p[2]:
        cs|={"K":1,"Q":2,"k":4,"q":8}.get(ch,0)
    ep=-1 if p[3]=='-' else Y((ord(p[3][1])-49)*8+ord(p[3][0])-97)
    hm=int(p[4]) if len(p)>4 else 0
    for i in range(128):
        if bb[i] and abs(bb[i])==6:
            kk[bb[i]>0]=i
def hit(sq,by):
    b=bb; o=oo
    t=sq-by*16-1
    if not t&0x88 and b[t]==by:
        return 1
    t=sq-by*16+1
    if not t&0x88 and b[t]==by:
        return 1
    kb=2*by
    nb=6*by
    for d in o[2]:
        t=sq+d
        if not t&0x88 and b[t]==kb:
            return 1
    for d in o[6]:
        t=sq+d
        if not t&0x88 and b[t]==nb:
            return 1
    b3=3*by; b5=5*by
    for d in o[3]:
        t=sq+d
        while not t&0x88:
            p=b[t]
            if p:
                if p==b3 or p==b5:
                    return 1
                break
            t+=d
    b4=4*by
    for d in o[4]:
        t=sq+d
        while not t&0x88:
            p=b[t]
            if p:
                if p==b4 or p==b5:
                    return 1
                break
            t+=d
    return 0
def genm(cp=0):
    mv=[]
    b=bb; o=oo; us=sd; e=ep; c=cs; h=hit; ap=mv.append
    lst=7 if us>0 else 0
    home=1 if us>0 else 6
    for sq in range(128):
        pc=b[sq]
        if pc*us<=0:
            continue
        k=pc if pc>0 else -pc
        if k==1:
            dd=16*us
            to=sq+dd
            if not to&0x88 and b[to]==0:
                if (to>>4)==lst:
                    for pm in PP:ap((sq,to,pm))
                elif not cp:
                    ap((sq,to,0))
                    if (sq>>4)==home and b[to+dd]==0:
                        ap((sq,to+dd,0))
            to=sq+dd-1
            if not to&0x88 and (b[to]*us<0 or to==e):
                if (to>>4)==lst:
                    for pm in PP:ap((sq,to,pm))
                else:
                    ap((sq,to,0))
            to=sq+dd+1
            if not to&0x88 and (b[to]*us<0 or to==e):
                if (to>>4)==lst:
                    for pm in PP:ap((sq,to,pm))
                else:
                    ap((sq,to,0))
        elif k==6:
            for d in o[6]:
                to=sq+d
                if not to&0x88 and b[to]*us<=0 and (not cp or b[to]):
                    ap((sq,to,0))
            if not cp and us>0 and sq==4:
                if c&1 and b[5]==0 and b[6]==0 and not h(4,-1) and not h(5,-1) and not h(6,-1):
                    ap((4,6,0))
                if c&2 and b[1]==0 and b[2]==0 and b[3]==0 and not h(4,-1) and not h(3,-1) and not h(2,-1):
                    ap((4,2,0))
            elif not cp and us<0 and sq==116:
                if c&4 and b[117]==0 and b[118]==0 and not h(116,1) and not h(117,1) and not h(118,1):
                    ap((116,118,0))
                if c&8 and b[113]==0 and b[114]==0 and b[115]==0 and not h(116,1) and not h(115,1) and not h(114,1):
                    ap((116,114,0))
        else:
            for d in o[k]:
                to=sq+d
                while not to&0x88:
                    q2=b[to]
                    if q2*us>0:
                        break
                    if q2 or not cp:
                        ap((sq,to,0))
                    if q2 or not ss[k]:
                        break
                    to+=d
    return mv
def doit(m):
    global sd,ep,cs,hm
    sq,to,pm=m
    pc=bb[sq]
    us=1 if pc>0 else -1
    cq=to
    cp=bb[to]
    if abs(pc)==1 and to==ep:
        cq=to-16*us
        cp=bb[cq]
    uu.append((sq,to,pm,pc,cq,cp,ep,cs,hm,kk[0],kk[1]))
    bb[sq]=0
    if cp:
        bb[cq]=0
    nn[us>0]-=(1 if 1<abs(pc)<6 else 0)
    if cp:
        nn[us<0]-=(1 if 1<abs(cp)<6 else 0)
    if pm:
        nn[us>0]+=1
    bb[to]=(pm or abs(pc))*us
    if abs(pc)==6:
        kk[us>0]=to
        if abs(to-sq)==2:
            if to==6:
                bb[5]=4;bb[7]=0
            elif to==2:
                bb[3]=4;bb[0]=0
            elif to==118:
                bb[117]=-4;bb[119]=0
            else:
                bb[115]=-4;bb[112]=0
    hm=0 if abs(pc)==1 or cp else hm+1
    if abs(pc)==6:
        cs&=~ (3 if us>0 else 12)
    if sq in (0,7,112,119) or to in (0,7,112,119):
        cs&=~{0:2,7:1,112:8,119:4}.get(sq,0)
        cs&=~{0:2,7:1,112:8,119:4}.get(to,0)
    ep=sq+16*us if abs(pc)==1 and abs(to-sq)==32 else -1
    sd=-sd
def undo():
    global sd,ep,cs,hm
    sq,to,pm,pc,cq,cp,e2,c2,f2,k0,k1=uu.pop()
    sd=-sd
    if abs(pc)==6 and abs(to-sq)==2:
        if to==6:
            bb[5]=0;bb[7]=4
        elif to==2:
            bb[3]=0;bb[0]=4
        elif to==118:
            bb[117]=0;bb[119]=-4
        else:
            bb[115]=0;bb[112]=-4
    bb[to]=0
    bb[sq]=pc
    if cp:
        bb[cq]=cp
    mi=1 if pc>0 else 0
    nn[mi]+=(1 if 1<abs(pc)<6 else 0)
    if pm:
        nn[mi]-=1
    if cp and 1<abs(cp)<6:
        nn[1-mi]+=1
    ep,cs,hm=e2,c2,f2
    kk[0],kk[1]=k0,k1
def fmt(sq,to,pm):
    def sqn(q):
        return "abcdefgh"[q&7]+str((q>>4)+1)
    return sqn(sq)+sqn(to)+("  nbrq"[pm] if pm else "")
N=0
CAP=30000
STOP=0
TT={}
INF=100000
MATE=90000
MV=[0,100,320,330,500,900,20000]
PR=[0,0,8,12,20,40,70,0]
PP=(5,4,3,2)
KI=[[None,None] for _ in range(96)]
H=set()
HI=[0]*16384
PH=(0,0,1,1,2,4,0)
def _pt():
    mg=[[0]*128 for _ in range(13)]
    eg=[[0]*128 for _ in range(13)]
    for pc in range(-6,7):
        if not pc:
            continue
        k=pc if pc>0 else -pc
        sg=1 if pc>0 else -1
        for sq in range(128):
            fl,rk=sq&7,sq>>4
            rw=rk if pc>0 else 7-rk
            m=MV[k]+(3-abs(fl-3))*(3-abs(rk-4))
            e=MV[k]
            if k==1:
                m+=PR[rw]
                e+=(0,0,10,16,24,40,70,0)[rw]
            elif k==6:
                m-=(3-abs(fl-3))*8+(0,8,6,2,0,2,6,8)[rw]
                e+=(3-abs(fl-3)+3-abs(rw-3))*6
            elif k in (2,3):
                m+=(3-abs(fl-3)+3-abs(rk-3))*3
            mg[pc+6][sq]=m*sg
            eg[pc+6][sq]=e*sg
    return mg,eg
MG,EG=_pt()
def val():
    a1=a2=ph2=0
    wb=bl=0
    b=bb; mg=MG; eg=EG
    u=[0]*8
    v=[0]*8
    for sq in range(128):
        pc=b[sq]
        if not pc:
            continue
        ix=pc+6
        a1+=mg[ix][sq]
        a2+=eg[ix][sq]
        ph2+=PH[abs(pc)]
        if pc==1:
            u[sq&7]+=1
        elif pc==-1:
            v[sq&7]+=1
        elif pc==3:
            wb+=1
        elif pc==-3:
            bl+=1
        elif pc==5 or pc==-5:
            of=1
            t=sq-16
            while t>=0:
                if b[t]==1 or b[t]==-1:
                    of=0
                    break
                t-=16
            if of:
                t=sq+16
                while t<128:
                    if b[t]==1 or b[t]==-1:
                        of=0
                        break
                    t+=16
            if of:
                a1+=14
                a2+=6
    if wb>1:
        a1+=25
        a2+=40
    if bl>1:
        a1-=25
        a2-=40
    for f in range(8):
        w=u[f]
        d=v[f]
        if w>1:
            a1-=12*(w-1)
            a2-=18*(w-1)
        if d>1:
            a1+=12*(d-1)
            a2+=18*(d-1)
        if w and (f==0 or u[f-1]==0) and (f==7 or u[f+1]==0):
            a1-=8
            a2-=12
        if d and (f==0 or v[f-1]==0) and (f==7 or v[f+1]==0):
            a1+=8
            a2+=12
    f=kk[0]&7
    if not u[f]+(u[f-1] if f else 0)+(u[f+1] if f<7 else 0):
        a1-=16
    f=kk[1]&7
    if not v[f]+(v[f-1] if f else 0)+(v[f+1] if f<7 else 0):
        a1+=16
    ph2=min(ph2,24)
    sc=(a1*ph2+a2*(24-ph2))//24
    return sc if sd>0 else -sc
def rankm(m,t,pl):
    sq,to,pm=m
    if t and m==t:
        return 30000
    cp=abs(bb[to])
    if pm:
        return 25000+pm*10+cp
    if cp or to==ep and abs(bb[sq])==1:
        return 10000+MV[cp or 1]*8-MV[abs(bb[sq])]
    if m in KI[pl]:
        return 8000
    return HI[(sq<<7)+to]
def q(al,be,pl):
    global N,STOP
    N+=1
    if N>CAP:
        STOP=1
        return al
    if hm>=100:
        return 0
    st=val()
    if st>=be:
        return be
    if st>al:
        al=st
    if pl>8:
        return al
    us=sd
    ic=hit(kk[us>0],-us)
    for m in sorted(genm(0 if ic else 1),key=lambda x:rankm(x,None,0),reverse=1):
        doit(m)
        if hit(kk[us>0],-us):
            undo()
            continue
        sc2=-q(-be,-al,pl+1)
        undo()
        if STOP:
            return al
        if sc2>=be:
            return be
        if sc2>al:
            al=sc2
    return al
def pv(dep,al,be,pl):
    global N,STOP,sd,ep
    N+=1
    if N>CAP:
        STOP=1
        return al
    if hm>=100:
        return 0
    us=sd
    ic=hit(kk[us>0],-us)
    if ic and dep>0 and pl<24:
        dep+=1
    if dep<=0:
        N-=1
        return q(al,be,pl)
    ky=(tuple(bb),sd,ep,cs)
    te=TT.get(ky)
    tm=te[3] if te else None
    if dep>=3 and not ic and nn[us>0]>0:
        ep0=ep
        ep=-1
        sd=-sd
        sc2=-pv(dep-3,-be,-be+1,pl+1)
        sd=-sd
        ep=ep0
        if STOP:
            return be if sc2>=be else al
        if sc2>=be:
            return be
    if te and te[0]>=dep:
        bd,sc2=te[1],te[2]
        if bd==0:
            return sc2
        if bd==1 and sc2<=al:
            return al
        if bd==2 and sc2>=be:
            return be
    mv=sorted(genm(),key=lambda x:rankm(x,tm,pl),reverse=1)
    lg=0
    bs=-INF
    bm2=None
    fg=1
    for m in mv:
        qt=bb[m[1]]==0 and not m[2] and not (abs(bb[m[0]])==1 and m[1]==ep)
        doit(m)
        if hit(kk[us>0],-us):
            undo()
            continue
        lg+=1
        rd=1 if lg>3 and dep>=3 and not ic and qt else 0
        if lg==1:
            sc2=-pv(dep-1-rd,-be,-al,pl+1)
        else:
            sc2=-pv(dep-1-rd,-al-1,-al,pl+1)
            if not STOP and al<sc2<be:
                sc2=-pv(dep-1,-be,-al,pl+1)
        undo()
        if STOP:
            return bs if bs>-INF else al
        if sc2>bs:
            bs=sc2
            bm2=m
            if sc2>al:
                al=sc2
                fg=0
        if al>=be:
            if qt:
                if KI[pl][0]!=m:
                    KI[pl][1]=KI[pl][0]
                    KI[pl][0]=m
                j=(m[0]<<7)+m[1]
                if HI[j]<7000:
                    HI[j]+=dep*dep
            fg=2
            break
    if lg==0:
        bs=-MATE+pl if ic else 0
        fg=0
    if bm2 and not STOP:
        TT[ky]=(dep,fg,bs,bm2)
    return bs
def best(f,bg):
    global N,CAP,STOP,TT
    CAP=bg
    load(f)
    TT={}
    for row in KI:
        row[0]=row[1]=None
    us=sd
    mv=[]
    for m in genm():
        doit(m)
        if not hit(kk[us>0],-us):
            mv.append(m)
        undo()
    if not mv:
        return "0000"
    if len(mv)==1:
        return fmt(*mv[0])
    bs=mv[0]
    for dep in range(1,24):
        N=0
        STOP=0
        al,be=-INF,INF
        lc=bs
        vl=-INF
        od=sorted(mv,key=lambda x:rankm(x,bs,0),reverse=1)
        for i2,m in enumerate(od):
            doit(m)
            rp2=(tuple(bb),sd,ep,cs) in H
            if i2==0:
                sc3=-pv(dep-1,-be,-al,1)
            else:
                sc3=-pv(dep-1,-al-1,-al,1)
                if not STOP and al<sc3<be:
                    sc3=-pv(dep-1,-be,-al,1)
            undo()
            if rp2:
                sc3=0
            if STOP:
                break
            if sc3>vl:
                vl,lc,al=sc3,m,sc3
        if STOP:
            break
        bs=lc
        if abs(vl)>MATE-300:
            break
    return fmt(*bs)
def net(base,path73,body):
    rq=W.Request(base+path73,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
    with W.urlopen(rq,timeout=30) as r:
        return json.load(r)
def mv12(u):
    qs=lambda z:(ord(z[1])-49)*16+ord(z[0])-97
    return (qs(u[0:2]),qs(u[2:4]),"  nbrq".index(u[4]) if len(u)>4 else 0)
def hist(game):
    H.clear()
    load(game["start_fen"])
    H.add((tuple(bb),sd,ep,cs))
    for u in game["moves"]:
        doit(mv12(u))
        H.add((tuple(bb),sd,ep,cs))
def run():
    base=os.environ.get("MAKEFUN_ENV_URL")
    if not base:
        sys.exit("MAKEFUN_ENV_URL is not set")
    PO=(0,4,4,4,4.5,4.5,5,5,5.5)
    rem=0
    game_no=0
    while 1:
        game=net(base,"/game",{})
        if game.get("status")=="done":
            print("done",game.get("wins"),game.get("draws"),game.get("losses"),file=sys.stderr)
            break
        while game.get("status")=="your_move":
            idx=game.get("game") or 1
            if idx!=game_no:
                game_no=idx
                rem=(PO[idx] if idx<len(PO) else 6)*1000000
            lm=200-game.get("plies",0)
            lm=lm//2 if lm>12 else 6
            bg=rem//lm
            bg=min(bg,80000)
            hist(game)
            m=best(game["fen"],bg)
            rem-=bg
            legal=game.get("legal_moves") or []
            if legal and m not in legal:
                m=legal[0]
            game=net(base,"/move",{"game":game["game"],"move":m})
if __name__=="__main__":
    run()
