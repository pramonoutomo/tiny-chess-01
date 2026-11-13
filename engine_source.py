import os,json,urllib.request,lzma,sys
from functools import lru_cache

ENV=os.environ.get('MAKEFUN_ENV_URL','')
def get_game():
 return json.loads(urllib.request.urlopen(ENV+'/game').read())
def post_move(m):
 req=urllib.request.Request(ENV+'/move',json.dumps({'move':m}).encode(),{'Content-Type':'application/json'},method='POST')
 return json.loads(urllib.request.urlopen(req).read())

# PeSTO tables
MG_PAWN=[0,0,0,0,0,0,0,0,98,134,61,95,68,126,34,-11,8,19,27,8,16,20,22,-6,-9,2,-6,13,13,-6,0,-11,-4,-7,10,42,37,2,-7,-6,-11,2,8,27,45,22,-12,-17,-14,0,20,27,27,20,0,-14,0,0,0,0,0,0,0,0]
EG_PAWN=[0,0,0,0,0,0,0,0,178,173,158,134,147,132,165,187,94,100,85,67,56,53,82,84,32,24,13,5,-2,4,17,17,13,9,-3,-7,-7,-8,3,-1,4,7,-6,1,0,-5,-1,-8,13,8,8,10,13,0,2,7,0,0,0,0,0,0,0,0]
MG_KNIGHT=[-167,-89,-34,-49,61,-97,-15,-107,-73,-41,72,36,23,62,7,-17,-47,60,37,65,84,129,73,44,-9,17,19,53,37,69,18,22,-13,4,16,13,28,19,21,-8,-23,-9,12,10,19,17,25,-16,-29,-53,-12,-3,-1,18,-14,-19,-105,-21,-58,-33,-17,-28,-19,-23]
EG_KNIGHT=[-58,-38,-13,-28,-31,-27,-63,-99,-25,-8,-25,-2,-9,-25,-24,-52,-24,-20,10,9,-1,-9,-19,-41,-17,3,22,22,22,11,8,-18,-18,-6,16,25,16,17,4,-18,-23,-3,-1,15,10,-3,-20,-22,-42,-20,-10,-5,-2,-20,-23,-44,-29,-51,-23,-15,-22,-18,-50,-64]
MG_BISHOP=[-29,4,-82,-37,-25,-42,7,-8,-26,16,-18,-13,30,59,18,-47,-16,37,43,40,35,50,37,-2,-4,5,19,50,37,37,7,-2,-6,13,13,26,34,12,10,4,-12,10,-4,10,30,27,8,-12,-8,36,9,16,15,10,3,-8,-14,-16,-19,-19,-4,-6,-5,-13]
EG_BISHOP=[-14,-21,-11,-8,-7,-9,-17,-24,-8,-4,7,-12,-3,-13,-4,-14,2,-8,0,-1,-2,6,0,4,-3,9,12,9,14,10,3,2,-6,3,13,19,7,10,-3,-9,-12,-3,8,10,13,3,-7,-15,-14,-18,-7,-1,4,-9,-15,-27,-23,-9,-23,-5,-9,-16,-5,-17]
MG_ROOK=[32,42,32,51,63,9,31,43,27,32,58,62,80,67,26,44,-5,19,26,36,17,45,61,16,-24,-11,7,26,24,35,-8,-20,-36,-26,-12,-1,9,-7,6,-23,-45,-25,-16,-17,3,0,-5,-33,-44,-16,-20,21,21,-2,-8,-33,-33,-28,24,14,16,15,22,-17]
EG_ROOK=[13,10,18,15,12,-2,-2,-2,11,13,13,11,-3,3,8,3,7,7,7,5,4,-3,-5,-3,4,3,13,1,2,1,-1,2,3,5,8,4,-5,-6,-8,-11,-4,0,-5,-1,-7,-12,-8,-16,-6,-6,0,2,-9,-9,-11,-16,-9,2,3,-1,-5,-13,4,-20]
MG_QUEEN=[-28,0,29,12,59,44,43,45,-24,-39,-5,1,-16,57,28,54,-13,-17,7,8,29,56,47,57,-27,-27,-16,-16,-1,17,-2,1,-9,-26,-9,-10,-2,-4,3,-3,-14,2,-11,2,-5,2,14,5,-35,-8,11,2,8,15,-3,1,-1,-18,-9,10,-15,-25,-31,-50]
EG_QUEEN=[-9,22,22,27,27,19,10,20,-17,20,32,41,58,25,30,0,-20,6,9,49,47,35,19,9,3,22,24,45,57,40,57,36,-18,28,19,47,31,34,39,23,-16,-27,15,6,9,17,10,5,-2,-2,20,30,30,24,-16,-12,-6,-23,-11,-8,-10,-14,-24,-20]
MG_KING=[-65,23,16,-15,-56,-34,2,13,29,10,-44,-13,-28,17,15,20,-9,0,25,2,-21,-15,-8,-24,34,30,19,-24,-5,0,10,24,-1,-28,-15,-64,-26,-45,-25,-37,-6,-3,-15,-12,-3,-14,-14,-2,24,4,-9,-24,-15,24,10,33,17,-16,-20,-33,-9,-28,0,25]
EG_KING=[-74,-35,-18,-18,-11,15,4,-17,-12,17,14,17,17,38,23,11,10,17,23,15,20,45,44,13,-8,22,24,27,26,33,26,3,-18,-4,21,24,27,23,9,-11,-19,-3,11,21,23,16,7,-9,-27,-11,4,13,14,4,-5,-17,-53,-34,-21,-11,-28,-14,-24,-43]

PIECE_SQ={1:(MG_PAWN,EG_PAWN),2:(MG_KNIGHT,EG_KNIGHT),3:(MG_BISHOP,EG_BISHOP),4:(MG_ROOK,EG_ROOK),5:(MG_QUEEN,EG_QUEEN),6:(MG_KING,EG_KING)}
MG_VAL=[0,82,337,365,477,1025,20000]
EG_VAL=[0,94,281,297,512,936,20000]
PHASE_VAL=[0,0,1,1,2,4,0]

MAILBOX=[
 -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
 -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
 -1, 0, 1, 2, 3, 4, 5, 6, 7,-1,
 -1, 8, 9,10,11,12,13,14,15,-1,
 -1,16,17,18,19,20,21,22,23,-1,
 -1,24,25,26,27,28,29,30,31,-1,
 -1,32,33,34,35,36,37,38,39,-1,
 -1,40,41,42,43,44,45,46,47,-1,
 -1,48,49,50,51,52,53,54,55,-1,
 -1,56,57,58,59,60,61,62,63,-1,
 -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
 -1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
MAILBOX64=[21,22,23,24,25,26,27,28,31,32,33,34,35,36,37,38,41,42,43,44,45,46,47,48,51,52,53,54,55,56,57,58,61,62,63,64,65,66,67,68,71,72,73,74,75,76,77,78,81,82,83,84,85,86,87,88,91,92,93,94,95,96,97,98]

SLIDE=[False,False,False,True,True,True,False]
OFFSETS=[[],[],[],[10,-10,21,-21,19,-19,12,-12],[11,-11,10,-10,1,-1],
 [11,-11,10,-10,1,-1,9,-9],[9,-9,11,-11,10,-10,1,-1],[1,-1,10,-10,9,-9,11,-11]]

INF=100000
NODES=0
MAX_NODES=50000
TT={}
TT_SIZE=1<<16
KILLER=[[0,0]for _ in range(64)]
HIST=[[0]*64 for _ in range(64)]

def sq(name):
 f=ord(name[0])-ord('a')
 r=int(name[1])-1
 return r*8+f

def sq_name(s):
 return'abcdefgh'[s%8]+str(s//8+1)

def flip(s):return 63-s

class Board:
 __slots__=['pc','color','side','ep','castle','half','full','hist']
 def __init__(self):
  self.pc=[0]*64;self.color=[0]*64;self.side=1
  self.ep=-1;self.castle=15;self.half=0;self.full=1;self.hist=[]
 def parse_fen(self,fen):
  parts=fen.split()
  rows=parts[0].split('/')
  for r,row in enumerate(rows):
   c=0
   for ch in row:
    if ch.isdigit():c+=int(ch)
    else:
     p='PNBRQK'.index(ch.upper())+1
     sq_=(7-r)*8+c
     self.pc[sq_]=p;self.color[sq_]=1 if ch.isupper() else 2
     c+=1
  self.side=1 if parts[1]=='w' else 2
  self.ep=-1
  if parts[3]!='-':self.ep=sq(parts[3])
  self.castle=0
  for ch in parts[2]:
   if ch=='K':self.castle|=1
   elif ch=='Q':self.castle|=2
   elif ch=='k':self.castle|=4
   elif ch=='q':self.castle|=8
  self.half=int(parts[4]);self.full=int(parts[5])
 def copy(self):
  b=Board();b.pc=self.pc[:];b.color=self.color[:]
  b.side=self.side;b.ep=self.ep;b.castle=self.castle
  b.half=self.half;b.full=self.full;b.hist=list(self.hist)
  return b

def attacked(b,sq_,by):
 for s in range(64):
  if b.color[s]!=by:continue
  p=b.pc[s]
  if p==1:
   d=1 if by==1 else -1
   for df in[-1,1]:
    t=s+d*8+df
    if 0<=t<64 and t==sq_:return True
  elif p==6:
   if max(abs(sq_%8-s%8),abs(sq_//8-s//8))<=1:return True
  else:
   offs=OFFSETS[p]
   for off in offs:
    t=MAILBOX[MAILBOX64[s]+off]
    while t!=-1:
     if t==sq_:return True
     if b.pc[t]!=0:break
     if not SLIDE[p]:break
     t=MAILBOX[MAILBOX64[t]+off]
 return False

def gen_moves(b):
 moves=[]
 side=b.side;opp=3-side
 for s in range(64):
  if b.color[s]!=side:continue
  p=b.pc[s]
  if p==1:
   d=1 if side==1 else -1;start=1 if side==1 else 6;promo_r=7 if side==1 else 0
   # forward
   t=s+d*8
   if 0<=t<64 and b.pc[t]==0:
    if t//8==promo_r:
     for pp in[5,4,3,2]:moves.append((s,t,pp))
    else:
     moves.append((s,t,0))
     if s//8==(1 if side==1 else 6):
      t2=s+d*16
      if b.pc[t2]==0:moves.append((s,t2,0))
   for df in[-1,1]:
    t=s+d*8+df
    if 0<=t<64 and abs(t%8-s%8)==1:
     if b.color[t]==opp:
      if t//8==promo_r:
       for pp in[5,4,3,2]:moves.append((s,t,pp))
      else:moves.append((s,t,0))
     elif t==b.ep:moves.append((s,t,0))
  elif p==6:
   for off in OFFSETS[6]:
    t=MAILBOX[MAILBOX64[s]+off]
    if t!=-1 and b.color[t]!=side:moves.append((s,t,0))
   # castling
   if side==1 and s==4:
    if b.castle&1 and b.pc[5]==0 and b.pc[6]==0 and not attacked(b,4,opp) and not attacked(b,5,opp) and not attacked(b,6,opp):
     moves.append((4,6,0))
    if b.castle&2 and b.pc[3]==0 and b.pc[2]==0 and b.pc[1]==0 and not attacked(b,4,opp) and not attacked(b,3,opp) and not attacked(b,2,opp):
     moves.append((4,2,0))
   elif side==2 and s==60:
    if b.castle&4 and b.pc[61]==0 and b.pc[62]==0 and not attacked(b,60,opp) and not attacked(b,61,opp) and not attacked(b,62,opp):
     moves.append((60,62,0))
    if b.castle&8 and b.pc[59]==0 and b.pc[58]==0 and b.pc[57]==0 and not attacked(b,60,opp) and not attacked(b,59,opp) and not attacked(b,58,opp):
     moves.append((60,58,0))
  else:
   for off in OFFSETS[p]:
    t=MAILBOX[MAILBOX64[s]+off]
    while t!=-1:
     if b.color[t]==side:break
     moves.append((s,t,0))
     if b.color[t]==opp or not SLIDE[p]:break
     t=MAILBOX[MAILBOX64[t]+off]
 return moves

def make_move(b,mv):
 s,t,promo=mv
 nb=b.copy()
 p=nb.pc[s];nb.hist.append((nb.ep,nb.castle,nb.half,nb.pc[t],nb.color[t]))
 nb.ep=-1
 if p==1:
  nb.half=0
  if abs(t-s)==16:nb.ep=(s+t)//2
  if t==b.ep and b.ep!=-1:
   cap=t+(-8 if nb.side==1 else 8)
   nb.pc[cap]=0;nb.color[cap]=0
 elif p==4:
  if s==0:nb.castle&=~2
  elif s==7:nb.castle&=~1
  elif s==56:nb.castle&=~8
  elif s==63:nb.castle&=~4
  if nb.pc[t]:nb.half=0
  else:nb.half+=1
 elif p==6:
  if nb.side==1:nb.castle&=~3
  else:nb.castle&=~12
  if abs(t-s)==2:
   if t==6:nb.pc[5]=4;nb.color[5]=nb.side;nb.pc[7]=0;nb.color[7]=0
   elif t==2:nb.pc[3]=4;nb.color[3]=nb.side;nb.pc[0]=0;nb.color[0]=0
   elif t==62:nb.pc[61]=4;nb.color[61]=nb.side;nb.pc[63]=0;nb.color[63]=0
   elif t==58:nb.pc[59]=4;nb.color[59]=nb.side;nb.pc[56]=0;nb.color[56]=0
  if nb.pc[t]:nb.half=0
  else:nb.half+=1
 else:
  if nb.pc[t]:nb.half=0
  else:nb.half+=1
 nb.pc[t]=promo if promo else p;nb.color[t]=nb.side
 nb.pc[s]=0;nb.color[s]=0
 nb.side=3-nb.side
 if nb.side==1:nb.full+=1
 return nb

def find_king(b,side):
 for i in range(64):
  if b.pc[i]==6 and b.color[i]==side:return i
 return-1

def in_check(b,side):
 k=find_king(b,side)
 return k!=-1 and attacked(b,k,3-side)

def phase_eval(b):
 phase=0
 for i in range(64):
  if b.pc[i]:phase+=PHASE_VAL[b.pc[i]]
 phase=min(phase,24)
 mg=eg=0
 for i in range(64):
  p=b.pc[i];col=b.color[i]
  if not p:continue
  si=flip(i) if col==1 else i
  mgt,egt=PIECE_SQ[p]
  v_mg=MG_VAL[p]+mgt[si]
  v_eg=EG_VAL[p]+egt[si]
  if col==1:mg+=v_mg;eg+=v_eg
  else:mg-=v_mg;eg-=v_eg
 score=(mg*phase+eg*(24-phase))//24
 return score if b.side==1 else -score

def move_score(b,mv,tt_move,ki,depth):
 s,t,promo=mv
 if(s,t,promo)==tt_move:return 20000
 if b.pc[t]:
  return 10000+MG_VAL[b.pc[t]]-MG_VAL[b.pc[s]]//10
 if mv==KILLER[depth][0] or mv==KILLER[depth][1]:return 9000
 return HIST[s][t]

def quiesce(b,alpha,beta,depth=0):
 global NODES
 NODES+=1
 stand=phase_eval(b)
 if stand>=beta:return beta
 if stand>alpha:alpha=stand
 if depth>8:return alpha
 moves=[(move_score(b,m,None,0,0),m)for m in gen_moves(b) if b.pc[m[1]] or m[1]==b.ep]
 moves.sort(reverse=True)
 for _,mv in moves:
  nb=make_move(b,mv)
  if in_check(nb,b.side):continue
  score=-quiesce(nb,-beta,-alpha,depth+1)
  if score>=beta:return beta
  if score>alpha:alpha=score
 return alpha

def pvs(b,depth,alpha,beta,null_ok=True):
 global NODES,TT,KILLER,HIST
 NODES+=1
 if NODES>=MAX_NODES:return phase_eval(b)
 key=hash(tuple(b.pc+b.color+[b.side,b.ep,b.castle]))%TT_SIZE
 tt_move=None
 if key in TT:
  td,tf,ts,tm=TT[key]
  tt_move=tm
  if td>=depth:
   if tf==0:return ts
   if tf==1 and ts<=alpha:return alpha
   if tf==2 and ts>=beta:return beta
 if depth==0:return quiesce(b,alpha,beta)
 side=b.side
 ck=in_check(b,side)
 if not ck and null_ok and depth>=3 and phase_eval(b)>=beta:
  nb=b.copy();nb.side=3-nb.side;nb.ep=-1
  score=-pvs(nb,depth-3,-beta,-beta+1,False)
  if score>=beta:return beta
 moves=gen_moves(b)
 moves_scored=[(move_score(b,m,tt_move,KILLER,depth),m)for m in moves]
 moves_scored.sort(reverse=True)
 legal=0;best=-INF;best_mv=None;flag=1
 for i,(sc,mv) in enumerate(moves_scored):
  nb=make_move(b,mv)
  if in_check(nb,side):continue
  legal+=1
  red=0
  if legal>4 and depth>=3 and not ck and not in_check(nb,3-side) and not nb.pc[mv[1]] and not mv[2]:
   red=1
  if legal==1:
   score=-pvs(nb,depth-1-red,-beta,-alpha)
  else:
   score=-pvs(nb,depth-1-red,-alpha-1,-alpha)
   if score>alpha and red:
    score=-pvs(nb,depth-1,-beta,-alpha)
   elif score>alpha and score<beta:
    score=-pvs(nb,depth-1,-beta,-alpha)
  if score>best:
   best=score;best_mv=mv
   if score>alpha:
    alpha=score;flag=0
    if not mv[1] in[mv[1] for _,mv in moves_scored if b.pc[mv[1]]]:
     HIST[mv[0]][mv[1]]+=depth*depth
  if alpha>=beta:
   if not b.pc[mv[1]]:
    if KILLER[depth][0]!=mv:KILLER[depth][1]=KILLER[depth][0];KILLER[depth][0]=mv
   flag=2;break
 if legal==0:
  return -INF+1 if ck else 0
 TT[key]=(depth,flag,best,best_mv)
 return best

def best_move(fen,moves_played):
 global NODES,TT,KILLER,HIST
 NODES=0
 KILLER=[[None,None]for _ in range(64)]
 HIST=[[0]*64 for _ in range(64)]
 b=Board();b.parse_fen(fen)
 # Opening book
 BOOK={
  'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1':'e2e4',
  'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1':'e7e5',
  'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2':'g1f3',
  'rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2':'b8c6',
  'r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3':'f1b5',
  'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1':'d7d5',
  'rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6 0 2':'c2c4',
  'rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3 0 2':'e7e6',
  'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1':'d2d4',
 }
 # Use book if available (last entry wins for starting pos, prefer e2e4)
 if fen in BOOK and len(moves_played)<=4:
  return BOOK[fen]
 all_moves=gen_moves(b)
 legal=[]
 for mv in all_moves:
  nb=make_move(b,mv)
  if not in_check(nb,b.side):legal.append(mv)
 if not legal:return'0000'
 if len(legal)==1:
  s,t,p=legal[0]
  return sq_name(s)+sq_name(t)+('nbrq'[p-2] if p else '')
 best_mv=legal[0];best_sc=-INF
 for depth in range(1,20):
  if NODES>=MAX_NODES//2:break
  sc=pvs(b,depth,-INF,INF)
  if key:=None:pass
  TT_MOVE=None
  key2=hash(tuple(b.pc+b.color+[b.side,b.ep,b.castle]))%TT_SIZE
  if key2 in TT:TT_MOVE=TT[key2][3]
  if TT_MOVE:best_mv=TT_MOVE;best_sc=sc
  if abs(sc)>INF-100:break
 s,t,p=best_mv
 return sq_name(s)+sq_name(t)+('nbrq'[p-2] if p else '')

while True:
 g=get_game()
 if g['status']!='playing':break
 mv=best_move(g['fen'],g.get('moves',[]))
 post_move(mv)
