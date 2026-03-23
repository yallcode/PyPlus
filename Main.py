#!/usr/bin/env python3
"""
py+ Interpreter v1.0
Usage:
  python pyplus.py              # REPL
  python pyplus.py prog.pyp     # run file
  python pyplus.py -c "say 'Hi'"# snippet
"""
import sys,os,re,math,time,random as _rnd

# ── 1. TOKEN TYPES ────────────────────────────────────────────────────────────
class T:
    NUM="NUM";STR="STR";BOOL="BOOL";IDENT="IDENT";NOTHING="NOTHING"
    NEWLINE="NEWLINE";INDENT="INDENT";DEDENT="DEDENT";EOF="EOF"
    COLON=":";COMMA=",";DOT=".";LPAREN="(";RPAREN=")"
    LBRACKET="[";RBRACKET="]";LBRACE="{";RBRACE="}"
    PLUS="+";MINUS="-";STAR="*";SLASH="/";PERCENT="%";STARSTAR="**"
    EQ="==";NEQ="!=";GT=">";LT="<";GTE=">=";LTE="<="
    SET="set";CHANGE="change";TO="to";AS="as";DEFINE="define"
    WITH="with";AND="and";OR="or";NOT="not";RETURNS="returns"
    GIVE="give";BACK="back"
    CLASS="class";EXTENDS="extends";HAS="has";SETUP="setup"
    MY="my";PARENT="parent";NEW="new";IS="is";AN="an";A="a"
    IF="if";ELSE="else";WHILE="while";REPEAT="repeat";TIMES="times"
    FOR="for";EACH="each";IN="in";FROM="from";STEP="step"
    AT="at";IDX="index";STOP="stop";SKIP="skip";NEXT="next";LOOP="loop"
    SAY="say";ASK="ask";USE="use"
    TRY="try";CATCH="catch";FINALLY="finally";RAISE="raise"
    GREATER="greater";LESS="less";THAN="than";EQUAL="equal"
    BY="by";MOD="mod";POWER="power";THE="the";OF="of"
    DIVIDED="divided";PLUSW="plus";MINUSW="minus";TIMESW="times_w"
    COUNT="count";LENGTH="length"
    ADD="add";REMOVE="remove";CONTAINS="contains"
    UPPER="uppercase";LOWER="lowercase";TRIMMED="trimmed"
    STARTS="starts";ENDS="ends";SPLIT="split";REPLACED="replaced"
    MSG="message";NUMKW="number"

_KW={
    "set":T.SET,"change":T.CHANGE,"to":T.TO,"as":T.AS,"define":T.DEFINE,
    "with":T.WITH,"and":T.AND,"or":T.OR,"not":T.NOT,"returns":T.RETURNS,
    "give":T.GIVE,"back":T.BACK,
    "class":T.CLASS,"extends":T.EXTENDS,"has":T.HAS,"setup":T.SETUP,
    "my":T.MY,"parent":T.PARENT,"new":T.NEW,"is":T.IS,"an":T.AN,"a":T.A,
    "if":T.IF,"else":T.ELSE,"while":T.WHILE,"repeat":T.REPEAT,"times":T.TIMES,
    "for":T.FOR,"each":T.EACH,"in":T.IN,"from":T.FROM,"step":T.STEP,
    "at":T.AT,"index":T.IDX,"stop":T.STOP,"skip":T.SKIP,"next":T.NEXT,"loop":T.LOOP,
    "say":T.SAY,"ask":T.ASK,"use":T.USE,
    "try":T.TRY,"catch":T.CATCH,"finally":T.FINALLY,"raise":T.RAISE,
    "greater":T.GREATER,"less":T.LESS,"than":T.THAN,"equal":T.EQUAL,
    "by":T.BY,"mod":T.MOD,"power":T.POWER,"the":T.THE,"of":T.OF,
    "divided":T.DIVIDED,"plus":T.PLUSW,"minus":T.MINUSW,"times":T.TIMESW,
    "true":T.BOOL,"false":T.BOOL,"nothing":T.NOTHING,
    "count":T.COUNT,"length":T.LENGTH,"add":T.ADD,"remove":T.REMOVE,
    "contains":T.CONTAINS,"uppercase":T.UPPER,"lowercase":T.LOWER,
    "trimmed":T.TRIMMED,"starts":T.STARTS,"ends":T.ENDS,"split":T.SPLIT,
    "replaced":T.REPLACED,"message":T.MSG,"number":T.NUMKW,
}

class Tok:
    __slots__=("ty","val","line","col")
    def __init__(self,ty,val,line=0,col=0):
        self.ty=ty;self.val=val;self.line=line;self.col=col
    def __repr__(self):return f"Tok({self.ty!r},{self.val!r})"

# ── 2. LEXER ──────────────────────────────────────────────────────────────────
class LexError(Exception):
    def __init__(self,msg,line=0):super().__init__(msg);self.line=line

def lex(src,filename="<input>"):
    if not src.endswith("\n"):src+="\n"
    toks=[];i=0;line=1;col=1;stack=[0]
    sym2={"**":T.STARSTAR,"==":T.EQ,"!=":T.NEQ,">=":T.GTE,"<=":T.LTE}
    sym1={"+":T.PLUS,"-":T.MINUS,"*":T.STAR,"/":T.SLASH,"%":T.PERCENT,
          ">":T.GT,"<":T.LT,":":T.COLON,",":T.COMMA,".":T.DOT,
          "(":T.LPAREN,")":T.RPAREN,"[":T.LBRACKET,"]":T.RBRACKET,
          "{":T.LBRACE,"}":T.RBRACE}
    def err(m):
        raise LexError(f"\n\033[1;31mERROR\033[0m '{filename}' line {line}: {m}\n",line)
    while i<len(src):
        ch=src[i]
        # newline + indent logic
        if ch=="\n":
            toks.append(Tok(T.NEWLINE,"\n",line,col));i+=1;line+=1;col=1
            j=i;ind=0
            while j<len(src) and src[j]==" ":ind+=1;j+=1
            if j<len(src) and src[j]=="\t":err("Use 4 spaces, not tabs")
            if j>=len(src) or src[j]=="\n":continue
            if src[j:j+2]=="--":continue
            cur=stack[-1]
            if ind>cur:stack.append(ind);toks.append(Tok(T.INDENT,ind,line,1))
            elif ind<cur:
                while stack[-1]>ind:
                    stack.pop();toks.append(Tok(T.DEDENT,0,line,1))
                if stack[-1]!=ind:err(f"Indentation mismatch: expected {stack[-1]} spaces, got {ind}")
            continue
        if ch==" ":i+=1;col+=1;continue
        # comments
        if src[i:i+3]=="---":
            i+=3
            while i<len(src) and src[i:i+3]!="---":
                if src[i]=="\n":line+=1
                i+=1
            i+=3;continue
        if src[i:i+2]=="--":
            while i<len(src) and src[i]!="\n":i+=1
            continue
        # strings
        if ch in('"',"'"):
            q=ch
            if src[i:i+3]==q*3:
                i+=3;buf=[]
                while i<len(src):
                    if src[i:i+3]==q*3:i+=3;break
                    if src[i]=="\n":line+=1
                    buf.append(src[i]);i+=1
                toks.append(Tok(T.STR,"".join(buf),line,col));continue
            i+=1;buf=[]
            while i<len(src) and src[i]!=q:
                if src[i]=="\n":err("String not closed")
                if src[i]=="\\" and i+1<len(src):
                    e=src[i+1];i+=2
                    buf.append({"n":"\n","t":"\t","r":"\r","\\":"\\"}.get(e,e))
                else:buf.append(src[i]);i+=1
            if i>=len(src):err("String not closed at end of file")
            i+=1;toks.append(Tok(T.STR,"".join(buf),line,col));continue
        # numbers
        if ch.isdigit():
            s=i
            while i<len(src) and src[i].isdigit():i+=1
            if i<len(src) and src[i]=="." and i+1<len(src) and src[i+1].isdigit():
                i+=1
                while i<len(src) and src[i].isdigit():i+=1
                toks.append(Tok(T.NUM,float(src[s:i]),line,col));continue
            toks.append(Tok(T.NUM,int(src[s:i]),line,col));continue
        # words
        if ch.isalpha() or ch=="_":
            s=i
            while i<len(src) and(src[i].isalnum() or src[i]=="_"):i+=1
            w=src[s:i];lo=w.lower();kw=_KW.get(lo)
            if kw==T.BOOL:toks.append(Tok(T.BOOL,lo=="true",line,col))
            elif kw==T.NOTHING:toks.append(Tok(T.NOTHING,None,line,col))
            elif kw:toks.append(Tok(kw,lo,line,col))
            else:toks.append(Tok(T.IDENT,w,line,col))
            col+=i-s;continue
        # two-char ops
        two=src[i:i+2]
        if two in sym2:toks.append(Tok(sym2[two],two,line,col));i+=2;col+=2;continue
        # one-char ops
        if ch in sym1:toks.append(Tok(sym1[ch],ch,line,col));i+=1;col+=1;continue
        err(f"Unknown character: {ch!r}")
    while len(stack)>1:stack.pop();toks.append(Tok(T.DEDENT,0,line,1))
    toks.append(Tok(T.EOF,None,line,1))
    return toks

# ── 3. AST NODES ──────────────────────────────────────────────────────────────
class N:pass
# Statements
class SVarDecl(N):
    def __init__(self,nm,ex,ln):self.nm=nm;self.ex=ex;self.line=ln
class SVarChange(N):
    def __init__(self,nm,ex,ln):self.nm=nm;self.ex=ex;self.line=ln
class SIdxChange(N):
    def __init__(self,nm,idx,v,ln):self.nm=nm;self.idx=idx;self.v=v;self.line=ln
class SConst(N):
    def __init__(self,nm,ex,ln):self.nm=nm;self.ex=ex;self.line=ln
class SFunc(N):
    def __init__(self,nm,ps,body,rt,ln):self.nm=nm;self.ps=ps;self.body=body;self.rt=rt;self.line=ln
class SClass(N):
    def __init__(self,nm,par,flds,ctor,meths,ln):
        self.nm=nm;self.par=par;self.flds=flds;self.ctor=ctor;self.meths=meths;self.line=ln
class SIf(N):
    def __init__(self,brs,eb,ln):self.brs=brs;self.eb=eb;self.line=ln
class SWhile(N):
    def __init__(self,cond,body,ln):self.cond=cond;self.body=body;self.line=ln
class SRepeat(N):
    def __init__(self,cnt,var,body,ln):self.cnt=cnt;self.var=var;self.body=body;self.line=ln
class SForEach(N):
    def __init__(self,var,idx,it,body,ln):self.var=var;self.idx=idx;self.it=it;self.body=body;self.line=ln
class SForRange(N):
    def __init__(self,var,st,en,sp,body,ln):
        self.var=var;self.st=st;self.en=en;self.sp=sp;self.body=body;self.line=ln
class SReturn(N):
    def __init__(self,ex,ln):self.ex=ex;self.line=ln
class STry(N):
    def __init__(self,body,catches,fin,ln):self.body=body;self.catches=catches;self.fin=fin;self.line=ln
class SRaise(N):
    def __init__(self,et,msg,ln):self.et=et;self.msg=msg;self.line=ln
class SImport(N):
    def __init__(self,nms,src,ln):self.nms=nms;self.src=src;self.line=ln
class SSay(N):
    def __init__(self,ex,ln):self.ex=ex;self.line=ln
class SCtrl(N):
    def __init__(self,k,ln):self.k=k;self.line=ln
class SExpr(N):
    def __init__(self,ex,ln):self.ex=ex;self.line=ln
class SMySet(N):
    def __init__(self,at,v,ln):self.at=at;self.v=v;self.line=ln
class SAdd(N):
    def __init__(self,item,tgt,ln):self.item=item;self.tgt=tgt;self.line=ln
class SRemove(N):
    def __init__(self,item,tgt,ln):self.item=item;self.tgt=tgt;self.line=ln
# Expressions
class ENum(N):
    def __init__(self,v,ln):self.v=v;self.line=ln
class EStr(N):
    def __init__(self,v,ln):self.v=v;self.line=ln
class EBool(N):
    def __init__(self,v,ln):self.v=v;self.line=ln
class ENone(N):
    def __init__(self,ln):self.line=ln
class EId(N):
    def __init__(self,nm,ln):self.nm=nm;self.line=ln
class EBinOp(N):
    def __init__(self,l,op,r,ln):self.l=l;self.op=op;self.r=r;self.line=ln
class EUnary(N):
    def __init__(self,op,x,ln):self.op=op;self.x=x;self.line=ln
class ECmp(N):
    def __init__(self,l,op,r,ln):self.l=l;self.op=op;self.r=r;self.line=ln
class ELogic(N):
    def __init__(self,l,op,r,ln):self.l=l;self.op=op;self.r=r;self.line=ln
class ECall(N):
    def __init__(self,f,args,ln):self.f=f;self.args=args;self.line=ln
class EMeth(N):
    def __init__(self,obj,nm,args,ln):self.obj=obj;self.nm=nm;self.args=args;self.line=ln
class EAttr(N):
    def __init__(self,obj,nm,ln):self.obj=obj;self.nm=nm;self.line=ln
class EIndex(N):
    def __init__(self,obj,idx,ln):self.obj=obj;self.idx=idx;self.line=ln
class ENew(N):
    def __init__(self,cls,args,ln):self.cls=cls;self.args=args;self.line=ln
class EList(N):
    def __init__(self,items,ln):self.items=items;self.line=ln
class EMap(N):
    def __init__(self,pairs,ln):self.pairs=pairs;self.line=ln
class EMyAttr(N):
    def __init__(self,at,ln):self.at=at;self.line=ln
class EInterp(N):
    def __init__(self,parts,ln):self.parts=parts;self.line=ln
class EAsk(N):
    def __init__(self,prompt,num,ln):self.prompt=prompt;self.num=num;self.line=ln
class EIsType(N):
    def __init__(self,obj,tn,ln):self.obj=obj;self.tn=tn;self.line=ln
class ELen(N):
    def __init__(self,obj,ln):self.obj=obj;self.line=ln
class EParent(N):
    def __init__(self,meth,args,ln):self.meth=meth;self.args=args;self.line=ln

# ── 4. PARSER ─────────────────────────────────────────────────────────────────
class ParseError(Exception):
    def __init__(self,msg,line=0):super().__init__(msg);self.line=line

# Keywords that can also act as identifiers (variable names, param names, etc.)
_SOFT={T.COUNT,T.LENGTH,T.ADD,T.REMOVE,T.CONTAINS,T.UPPER,T.LOWER,
       T.TRIMMED,T.STARTS,T.ENDS,T.SPLIT,T.REPLACED,T.MSG,T.NUMKW,
       T.A,T.AN,T.BY,T.THE,T.IN,T.OF,T.MOD,T.PLUSW,T.MINUSW,T.TIMESW}

class Parser:
    def __init__(self,toks,lines=None,fn="<input>"):
        self.toks=toks;self.pos=0;self.lines=lines or[];self.fn=fn

    def cur(self)->Tok:return self.toks[self.pos]
    def peek(self,n=1)->Tok:
        i=self.pos+n
        return self.toks[i] if i<len(self.toks) else self.toks[-1]

    def adv(self)->Tok:
        t=self.toks[self.pos]
        if self.pos<len(self.toks)-1:self.pos+=1
        return t

    def eat(self,*tys,hint="")->Tok:
        t=self.cur()
        if T.IDENT in tys and t.ty in _SOFT:
            self.adv();return Tok(T.IDENT,t.val,t.line,t.col)
        if t.ty not in tys:
            exp="/".join(tys)
            src=self.lines[t.line-1] if 0<t.line<=len(self.lines) else ""
            raise ParseError(
                f"\n\033[1;31mSYNTAX ERROR\033[0m '{self.fn}' line {t.line}:\n"
                f"  Expected {exp!r} but got {t.ty!r} ({t.val!r})\n"
                +(f"  Hint: {hint}\n" if hint else "")
                +(f"  → {src}\n" if src else ""),t.line)
        return self.adv()

    def chk(self,*tys)->bool:return self.cur().ty in tys
    def match(self,*tys)->bool:
        if self.cur().ty in tys:self.adv();return True
        return False
    def skip_nl(self):
        while self.chk(T.NEWLINE):self.adv()
    def eat_nl(self):
        while self.chk(T.NEWLINE):self.adv()

    def err(self,msg,ln=None):
        l=ln or self.cur().line
        src=self.lines[l-1] if 0<l<=len(self.lines) else ""
        raise ParseError(
            f"\n\033[1;31mSYNTAX ERROR\033[0m '{self.fn}' line {l}:\n  {msg}\n"
            +(f"  → {src}\n" if src else ""),l)

    def name(self)->Tok:
        t=self.cur()
        if t.ty==T.IDENT or t.ty in _SOFT or t.ty==T.SETUP:
            self.adv();return Tok(T.IDENT,t.val,t.line,t.col)
        self.err(f"Expected a name, got {t.ty!r} ({t.val!r})")

    # ── program ────
    def parse(self):
        self.skip_nl();stmts=[]
        while not self.chk(T.EOF):
            s=self.stmt()
            if s:stmts.append(s)
            self.skip_nl()
        return stmts

    def block(self):
        self.eat(T.INDENT,hint="Indent 4 spaces after ':'")
        self.skip_nl();stmts=[]
        while not self.chk(T.DEDENT,T.EOF):
            s=self.stmt()
            if s:stmts.append(s)
            self.skip_nl()
        if self.chk(T.DEDENT):self.adv()
        return stmts

    # ── statements ────
    def stmt(self):
        self.skip_nl();t=self.cur();ty=t.ty;ln=t.line
        if ty==T.SET:    return self.s_set()
        if ty==T.CHANGE: return self.s_change()
        if ty==T.DEFINE: return self.s_define()
        if ty==T.CLASS:  return self.s_class()
        if ty==T.IF:     return self.s_if()
        if ty==T.WHILE:  return self.s_while()
        if ty==T.REPEAT: return self.s_repeat()
        if ty==T.FOR:    return self.s_for()
        if ty==T.GIVE:   return self.s_return()
        if ty==T.TRY:    return self.s_try()
        if ty==T.RAISE:  return self.s_raise()
        if ty==T.USE:    return self.s_import()
        if ty==T.SAY:    return self.s_say()
        if ty==T.STOP:   return self.s_ctrl()
        if ty==T.SKIP:   return self.s_ctrl()
        if ty==T.MY:     return self.s_myset()
        if ty==T.ADD:    return self.s_addrem()
        if ty==T.REMOVE: return self.s_addrem()
        if ty==T.PARENT: return self.s_parent()
        if ty==T.NEWLINE:self.adv();return None
        if ty==T.IDENT or ty in _SOFT:return self.s_expr()
        self.adv();return None

    def s_set(self):
        ln=self.cur().line;self.adv()
        nm=self.name().val;hint=None
        if self.match(T.AS):hint=self.name().val
        self.eat(T.TO,hint="Write: set <name> to <value>")
        ex=self.expr();self.eat_nl()
        return SVarDecl(nm,ex,ln)

    def s_change(self):
        ln=self.cur().line;self.adv()
        nm=self.name().val
        if self.chk(T.AT):
            self.adv();idx=self.expr()
            self.eat(T.TO);val=self.expr();self.eat_nl()
            return SIdxChange(nm,idx,val,ln)
        self.eat(T.TO,hint="Write: change <name> to <value>")
        ex=self.expr();self.eat_nl()
        return SVarChange(nm,ex,ln)

    def s_define(self):
        ln=self.cur().line;self.adv()
        nm=self.name().val
        # constant: "define X as val" with no colon following
        if self.chk(T.AS):
            saved=self.pos;self.adv()
            val=self.expr()
            if not self.chk(T.COLON,T.RETURNS):
                self.eat_nl();return SConst(nm,val,ln)
            self.pos=saved
        ps=[]
        if self.match(T.WITH):ps=self.params()
        rt=None
        if self.match(T.RETURNS):rt=self.name().val
        self.eat(T.COLON,hint=f"Add ':' after 'define {nm}'");self.eat_nl()
        return SFunc(nm,ps,self.block(),rt,ln)

    def params(self):
        ps=[];nm=self.name().val;hint=None
        if self.match(T.AS):hint=self.name().val
        ps.append((nm,hint,None))
        while self.match(T.AND) or self.match(T.COMMA):
            nm=self.name().val;hint=None
            if self.match(T.AS):hint=self.name().val
            ps.append((nm,hint,None))
        return ps

    def s_class(self):
        ln=self.cur().line;self.adv()
        nm=self.name().val;par=None
        if self.match(T.EXTENDS):par=self.name().val
        self.eat(T.COLON);self.eat_nl()
        self.eat(T.INDENT,hint="Indent class body")
        self.skip_nl()
        flds=[];ctor=None;meths=[]
        while not self.chk(T.DEDENT,T.EOF):
            self.skip_nl()
            if self.chk(T.DEDENT,T.EOF):break
            t=self.cur()
            if t.ty==T.HAS:
                self.adv();fn=self.name().val;ft=None
                if self.match(T.AS):ft=self.name().val
                flds.append((fn,ft));self.eat_nl()
            elif t.ty==T.SETUP:
                self.adv();ps=[]
                if self.match(T.WITH):ps=self.params()
                self.eat(T.COLON);self.eat_nl()
                ctor=SFunc("__init__",ps,self.block(),None,t.line)
            elif t.ty==T.DEFINE:
                meths.append(self.s_define())
            else:
                self.adv()
        if self.chk(T.DEDENT):self.adv()
        return SClass(nm,par,flds,ctor,meths,ln)

    def s_if(self):
        ln=self.cur().line;self.adv()
        brs=[];cond=self.expr()
        self.eat(T.COLON);self.eat_nl()
        brs.append((cond,self.block()))
        eb=None
        while self.chk(T.ELSE):
            self.adv()
            if self.chk(T.IF):
                self.adv();c=self.expr()
                self.eat(T.COLON);self.eat_nl()
                brs.append((c,self.block()))
            else:
                self.eat(T.COLON);self.eat_nl()
                eb=self.block();break
        return SIf(brs,eb,ln)

    def s_while(self):
        ln=self.cur().line;self.adv()
        cond=self.expr();self.eat(T.COLON);self.eat_nl()
        return SWhile(cond,self.block(),ln)

    def s_repeat(self):
        ln=self.cur().line;self.adv()
        cnt=self.expr()
        if not self.chk(T.TIMES,T.TIMESW): self.err("Expected 'times' after repeat count")
        self.adv()
        var=None
        if self.match(T.WITH):var=self.name().val
        self.eat(T.COLON);self.eat_nl()
        return SRepeat(cnt,var,self.block(),ln)

    def s_for(self):
        ln=self.cur().line;self.adv()
        self.eat(T.EACH);var=self.name().val;idx=None
        if self.chk(T.AT):self.adv();self.eat(T.IDX);idx=self.name().val
        if self.chk(T.FROM):
            self.adv();st=self.expr();self.eat(T.TO);en=self.expr()
            sp=None
            if self.match(T.STEP):sp=self.expr()
            self.eat(T.COLON);self.eat_nl()
            return SForRange(var,st,en,sp,self.block(),ln)
        self.eat(T.IN,hint="Write: for each <var> in <list>:")
        it=self.expr();self.eat(T.COLON);self.eat_nl()
        return SForEach(var,idx,it,self.block(),ln)

    def s_return(self):
        ln=self.cur().line;self.adv();self.eat(T.BACK)
        ex=None
        if not self.chk(T.NEWLINE,T.EOF,T.DEDENT):ex=self.expr()
        self.eat_nl();return SReturn(ex,ln)

    def s_try(self):
        ln=self.cur().line;self.adv()
        self.eat(T.COLON);self.eat_nl()
        body=self.block();catches=[]
        while self.chk(T.CATCH):
            self.adv();et=None
            if self.chk(T.IDENT) or self.cur().ty in _SOFT:et=self.name().val
            var=None
            if self.match(T.AS):var=self.name().val
            self.eat(T.COLON);self.eat_nl()
            catches.append((et,var,self.block()))
        fin=None
        if self.match(T.FINALLY):self.eat(T.COLON);self.eat_nl();fin=self.block()
        return STry(body,catches,fin,ln)

    def s_raise(self):
        ln=self.cur().line;self.adv()
        et=self.name().val;msg=None
        if self.match(T.WITH):msg=self.expr()
        self.eat_nl();return SRaise(et,msg,ln)

    def s_import(self):
        ln=self.cur().line;self.adv()
        nms=[self.name().val]
        while self.match(T.AND) or self.match(T.COMMA):nms.append(self.name().val)
        src=None
        if self.match(T.FROM):
            if self.chk(T.IDENT) or self.cur().ty in _SOFT:src=self.name().val
            elif self.chk(T.STR):src=self.adv().val
        self.eat_nl();return SImport(nms,src,ln)

    def s_say(self):
        ln=self.cur().line;self.adv()
        ex=self.expr();self.eat_nl();return SSay(ex,ln)

    def s_ctrl(self):
        ln=self.cur().line;ty=self.cur().ty;self.adv()
        if ty==T.STOP:self.eat(T.LOOP);self.eat_nl();return SCtrl("break",ln)
        self.eat(T.TO);self.eat(T.NEXT);self.eat_nl();return SCtrl("continue",ln)

    def s_myset(self):
        ln=self.cur().line;self.adv()
        at=self.name().val;self.eat(T.IS)
        v=self.expr();self.eat_nl();return SMySet(at,v,ln)

    def s_addrem(self):
        ln=self.cur().line;op=self.cur().ty;self.adv()
        item=self.expr()
        if op==T.ADD:self.eat(T.TO,hint="Write: add <item> to <list>")
        else:self.eat(T.FROM,hint="Write: remove <item> from <list>")
        # target can be 'my fieldname' or plain name
        if self.chk(T.MY):
            self.adv();attr=self.name().val
            self.eat_nl()
            # SAdd/SRemove but on 'my attr' - store as special marker
            if op==T.ADD:return SExpr(ECall(EId('__list_add_my__',ln),[EStr(attr,ln),item],ln),ln)
            return SExpr(ECall(EId('__list_rm_my__',ln),[EStr(attr,ln),item],ln),ln)
        tgt=self.name().val;self.eat_nl()
        if op==T.ADD:return SAdd(item,tgt,ln)
        return SRemove(item,tgt,ln)

    def s_parent(self):
        ln=self.cur().line;self.adv()
        if self.chk(T.SETUP):meth="setup";self.adv()
        else:meth=self.name().val
        args=[]
        if self.match(T.WITH):args=self.arglist()
        self.eat_nl();return SExpr(EParent(meth,args,ln),ln)

    def s_expr(self):
        ln=self.cur().line;e=self.expr();self.eat_nl();return SExpr(e,ln)

    # ── expressions ────
    def expr(self):return self.e_logic()

    def e_logic(self):
        left=self.e_cmp()
        while self.chk(T.AND,T.OR):
            op=self.adv().ty;right=self.e_cmp()
            left=ELogic(left,op,right,left.line)
        return left

    def e_cmp(self):
        left=self.e_add();ln=self.cur().line
        if self.chk(T.IS):
            self.adv()
            if self.chk(T.NOT):
                self.adv()
                if self.chk(T.EQUAL):self.adv()
                if self.chk(T.TO):self.adv()
                return ECmp(left,"!=",self.e_add(),ln)
            if self.chk(T.EQUAL):
                self.adv()
                if self.chk(T.TO):self.adv()
                return ECmp(left,"==",self.e_add(),ln)
            if self.chk(T.GREATER):
                self.adv()
                if self.chk(T.THAN):self.adv()
                op=">"
                if self.chk(T.OR):
                    self.adv()
                    if self.chk(T.EQUAL):self.adv()
                    if self.chk(T.TO):self.adv()
                    op=">="
                return ECmp(left,op,self.e_add(),ln)
            if self.chk(T.LESS):
                self.adv()
                if self.chk(T.THAN):self.adv()
                op="<"
                if self.chk(T.OR):
                    self.adv()
                    if self.chk(T.EQUAL):self.adv()
                    if self.chk(T.TO):self.adv()
                    op="<="
                return ECmp(left,op,self.e_add(),ln)
            if self.chk(T.AN,T.A):
                self.adv();tn=self.name().val
                return EIsType(left,tn,ln)
            return ECmp(left,"==",self.e_add(),ln)
        sym={T.EQ:"==",T.NEQ:"!=",T.GTE:">=",T.LTE:"<=",T.GT:">",T.LT:"<"}
        if self.cur().ty in sym:op=sym[self.adv().ty];return ECmp(left,op,self.e_add(),ln)
        return left

    def e_add(self):
        left=self.e_mul()
        while self.chk(T.PLUS,T.MINUS,T.PLUSW,T.MINUSW):
            op="+" if self.cur().ty in(T.PLUS,T.PLUSW) else "-"
            self.adv();right=self.e_mul()
            left=EBinOp(left,op,right,left.line)
        return left

    def e_mul(self):
        left=self.e_pow()
        while True:
            t=self.cur()
            if t.ty in(T.STAR,T.TIMESW) and self.peek().ty not in(T.WITH,T.COLON,T.NEWLINE,T.EOF,T.IDX):self.adv();left=EBinOp(left,"*",self.e_pow(),left.line)
            elif t.ty==T.SLASH:self.adv();left=EBinOp(left,"/",self.e_pow(),left.line)
            elif t.ty in(T.PERCENT,T.MOD):self.adv();left=EBinOp(left,"%",self.e_pow(),left.line)
            elif t.ty==T.DIVIDED:self.adv();self.eat(T.BY);left=EBinOp(left,"/",self.e_pow(),left.line)
            else:break
        return left

    def e_pow(self):
        left=self.e_unary()
        if self.chk(T.STARSTAR):self.adv();return EBinOp(left,"**",self.e_unary(),left.line)
        if self.chk(T.TO) and self.peek().ty==T.THE:
            self.adv();self.adv();self.eat(T.POWER);self.eat(T.OF)
            return EBinOp(left,"**",self.e_unary(),left.line)
        return left

    def e_unary(self):
        ln=self.cur().line
        if self.chk(T.MINUS):self.adv();return EUnary("-",self.e_unary(),ln)
        if self.chk(T.NOT):self.adv();return EUnary("not",self.e_unary(),ln)
        return self.e_post()

    def e_post(self):
        node=self.e_primary()
        while True:
            ln=self.cur().line
            if self.chk(T.DOT):
                self.adv();nm=self.name().val
                args=[];is_call=False
                if self.match(T.WITH):args=self.arglist();is_call=True
                elif self.chk(T.LPAREN):self.adv();args=self.cargs();self.eat(T.RPAREN);is_call=True
                if is_call:node=EMeth(node,nm,args,ln)
                else:node=EAttr(node,nm,ln)
            elif self.chk(T.AT):
                self.adv();idx=self.expr();node=EIndex(node,idx,ln)
            else:break
        return self.e_strops(node)

    def e_strops(self,node):
        ln=self.cur().line
        if self.chk(T.IN):
            self.adv()
            if self.chk(T.UPPER):self.adv();return EMeth(node,"upper",[],ln)
            if self.chk(T.LOWER):self.adv();return EMeth(node,"lower",[],ln)
        if self.chk(T.TRIMMED):self.adv();return EMeth(node,"strip",[],ln)
        if self.chk(T.UPPER):self.adv();return EMeth(node,"upper",[],ln)
        if self.chk(T.LOWER):self.adv();return EMeth(node,"lower",[],ln)
        if self.chk(T.CONTAINS):self.adv();return EMeth(node,"contains",[self.e_primary()],ln)
        if self.chk(T.STARTS):
            self.adv();self.match(T.WITH)
            return EMeth(node,"startswith",[self.e_primary()],ln)
        if self.chk(T.ENDS):
            self.adv();self.match(T.WITH)
            return EMeth(node,"endswith",[self.e_primary()],ln)
        if self.chk(T.SPLIT):
            self.adv();self.match(T.BY)
            return EMeth(node,"split",[self.e_primary()],ln)
        if self.chk(T.REPLACED):
            self.adv();old=self.e_primary();self.match(T.WITH);new=self.e_primary()
            return EMeth(node,"replace",[old,new],ln)
        return node

    def e_primary(self):
        t=self.cur();ln=t.line
        if t.ty==T.NUM:self.adv();return ENum(t.val,ln)
        if t.ty==T.BOOL:self.adv();return EBool(t.val,ln)
        if t.ty==T.NOTHING:self.adv();return ENone(ln)
        if t.ty==T.STR:self.adv();return self.interp(t.val,ln)
        if t.ty==T.LBRACKET:
            self.adv();items=[]
            if not self.chk(T.RBRACKET):
                items.append(self.expr())
                while self.match(T.COMMA):
                    if self.chk(T.RBRACKET):break
                    items.append(self.expr())
            self.eat(T.RBRACKET);return EList(items,ln)
        if t.ty==T.LBRACE:
            self.adv();pairs=[]
            if not self.chk(T.RBRACE):
                k=self.expr();self.eat(T.COLON);v=self.expr();pairs.append((k,v))
                while self.match(T.COMMA):
                    if self.chk(T.RBRACE):break
                    k=self.expr();self.eat(T.COLON);v=self.expr();pairs.append((k,v))
            self.eat(T.RBRACE);return EMap(pairs,ln)
        if t.ty==T.LPAREN:
            self.adv();e=self.expr();self.eat(T.RPAREN);return e
        if t.ty==T.NEW:
            self.adv();cls=self.name().val;args=[]
            if self.match(T.WITH):args=self.arglist()
            elif self.chk(T.LPAREN):self.adv();args=self.cargs();self.eat(T.RPAREN)
            return ENew(cls,args,ln)
        if t.ty==T.MY:self.adv();at=self.name().val;return EMyAttr(at,ln)
        if t.ty==T.ASK:
            self.adv();num=False
            if self.chk(T.NUMKW):self.adv();num=True
            return EAsk(self.expr(),num,ln)
        if t.ty in(T.COUNT,T.LENGTH):
            self.adv();self.eat(T.OF);obj=self.e_primary();return ELen(obj,ln)
        # identifier or soft keyword used as name
        if t.ty==T.IDENT or t.ty in _SOFT:
            self.adv();nm=t.val
            if self.chk(T.LPAREN):
                self.adv();args=self.cargs();self.eat(T.RPAREN)
                return ECall(EId(nm,ln),args,ln)
            if self.chk(T.WITH):
                self.adv();args=self.arglist()
                return ECall(EId(nm,ln),args,ln)
            return EId(nm,ln)
        self.err(f"Unexpected {t.ty!r} ({t.val!r})")

    def arglist(self):
        args=[]
        if self.chk(T.NEWLINE,T.COLON,T.EOF,T.DEDENT):return args
        args.append(self.expr())
        while self.match(T.COMMA) or self.match(T.AND):
            if self.chk(T.NEWLINE,T.COLON,T.EOF,T.DEDENT):break
            args.append(self.expr())
        return args

    def cargs(self):
        args=[]
        if self.chk(T.RPAREN):return args
        args.append(self.expr())
        while self.match(T.COMMA):args.append(self.expr())
        return args

    def interp(self,s,ln):
        parts=[];last=0
        for m in re.finditer(r"\{([^}]+)\}",s):
            if m.start()>last:parts.append(EStr(s[last:m.start()],ln))
            parts.append(EId(m.group(1).strip(),ln));last=m.end()
        if last<len(s):parts.append(EStr(s[last:],ln))
        if not parts:return EStr(s,ln)
        if len(parts)==1:return parts[0]
        return EInterp(parts,ln)

# ── 5. RUNTIME ────────────────────────────────────────────────────────────────
class PypError(Exception):
    def __init__(self,et,msg,line=None):
        super().__init__(msg);self.et=et;self.msg=msg;self.line=line
class Ret(Exception):
    def __init__(self,v):self.v=v
class Brk(Exception):pass
class Cont(Exception):pass

class Env:
    def __init__(self,par=None,nm=""):self.v={};self.par=par;self.nm=nm
    def get(self,nm,line=None):
        if nm in self.v:return self.v[nm]
        if self.par:return self.par.get(nm,line)
        raise PypError("NameError",
            f"'{nm}' hasn't been defined.\n  Fix: use  set {nm} to <value>  first.",line)
    def set(self,nm,val):self.v[nm]=val
    def assign(self,nm,val,line=None):
        if nm in self.v:self.v[nm]=val;return
        if self.par:self.par.assign(nm,val,line);return
        raise PypError("NameError",
            f"'{nm}' not defined — can't change it.\n  Use  set {nm} to <value>  first.",line)

class Cls:
    def __init__(self,nm,par,flds,ctor,meths,env):
        self.nm=nm;self.par=par;self.flds=flds;self.ctor=ctor
        self.meths={m.nm:m for m in meths};self.env=env
    def __repr__(self):return f"<class {self.nm}>"

class Inst:
    def __init__(self,cls):self.cls=cls;self.attrs={}
    def get(self,nm,line=None):
        if nm in self.attrs:return self.attrs[nm]
        klass=self.cls
        while klass:
            if nm in klass.meths:return Bound(self,klass.meths[nm])
            klass=klass.par
        avail=list(self.attrs)+list(self.cls.meths)
        raise PypError("AttributeError",
            f"'{self.cls.nm}' has no field or method '{nm}'.\n  Available: {', '.join(avail) or 'none'}",line)
    def set(self,nm,v):self.attrs[nm]=v
    def __repr__(self):return f"<{self.cls.nm}>"

class Func:
    def __init__(self,nm,ps,body,env):self.nm=nm;self.ps=ps;self.body=body;self.env=env
    def __repr__(self):return f"<function {self.nm}>"

class Bound:
    def __init__(self,inst,fn):self.inst=inst;self.fn=fn
    def __repr__(self):return f"<method {self.fn.nm}>"

def _tn(v):
    if v is None:return "Nothing"
    if isinstance(v,bool):return "Boolean"
    if isinstance(v,int):return "Integer"
    if isinstance(v,float):return "Decimal"
    if isinstance(v,str):return "Text"
    if isinstance(v,list):return "List"
    if isinstance(v,dict):return "Map"
    if isinstance(v,Inst):return v.cls.nm
    if isinstance(v,Func):return "Function"
    if isinstance(v,Cls):return "Class"
    return type(v).__name__

def _show(v):
    if v is None:return "nothing"
    if isinstance(v,bool):return "true" if v else "false"
    if isinstance(v,float):return str(int(v)) if v==int(v) else str(v)
    if isinstance(v,list):return"["+", ".join(_show(x) for x in v)+"]"
    if isinstance(v,dict):return"{"+", ".join(f"{_show(k)}: {_show(val)}" for k,val in v.items())+"}"
    return str(v)

def _truthy(v):
    if v is None or v is False:return False
    if isinstance(v,(int,float)):return v!=0
    if isinstance(v,(str,list,dict)):return len(v)>0
    return True

# ── 6. INTERPRETER ────────────────────────────────────────────────────────────
class Interp:
    def __init__(self,fn="<input>"):
        self.fn=fn;self.G=Env(nm="global")
        self._mods={
            "math":{"pi":math.pi,"e":math.e,
                "sqrt":lambda a:math.sqrt(a[0]),"floor":lambda a:math.floor(a[0]),
                "ceil":lambda a:math.ceil(a[0]),"abs":lambda a:abs(a[0]),
                "round":lambda a:round(a[0],int(a[1]) if len(a)>1 else 0),
                "max":lambda a:max(a),"min":lambda a:min(a),
                "pow":lambda a:math.pow(a[0],a[1]),
                "log":lambda a:math.log(a[0],a[1] if len(a)>1 else math.e),
                "sin":lambda a:math.sin(a[0]),"cos":lambda a:math.cos(a[0]),
                "tan":lambda a:math.tan(a[0])},
            "random":{"random":lambda a:_rnd.random(),
                "randint":lambda a:_rnd.randint(int(a[0]),int(a[1])),
                "choice":lambda a:_rnd.choice(a[0]),
                "shuffle":lambda a:(_rnd.shuffle(a[0]),a[0])[1]},
            "time":{"now":lambda a:time.time(),
                "sleep":lambda a:time.sleep(a[0]),
                "format":lambda a:time.strftime(a[0] if a else"%Y-%m-%d %H:%M:%S")},
        }

    def run(self,stmts):
        for s in stmts:
            if s:self.ex(s,self.G)

    def blk(self,stmts,env):
        for s in stmts:
            if s:self.ex(s,env)

    def ex(self,nd,env):
        t=type(nd)
        if t is SVarDecl:env.set(nd.nm,self.ev(nd.ex,env));return
        if t is SVarChange:env.assign(nd.nm,self.ev(nd.ex,env),nd.line);return
        if t is SIdxChange:
            obj=env.get(nd.nm,nd.line);idx=self.ev(nd.idx,env);val=self.ev(nd.v,env)
            if isinstance(obj,list):obj[int(idx)]=val
            elif isinstance(obj,dict):obj[idx]=val
            else:raise PypError("TypeError",f"Cannot index-assign {_tn(obj)}",nd.line)
            return
        if t is SConst:env.set(nd.nm,self.ev(nd.ex,env));return
        if t is SFunc:env.set(nd.nm,Func(nd.nm,nd.ps,nd.body,env));return
        if t is SClass:
            par=None
            if nd.par:
                par=env.get(nd.par,nd.line)
                if not isinstance(par,Cls):raise PypError("TypeError",f"'{nd.par}' is not a class",nd.line)
            wrapped_meths=[Func(m.nm,m.ps,m.body,env) for m in nd.meths]
            wrapped_ctor=Func(nd.ctor.nm,nd.ctor.ps,nd.ctor.body,env) if nd.ctor else None
            env.set(nd.nm,Cls(nd.nm,par,nd.flds,wrapped_ctor,wrapped_meths,env));return
        if t is SIf:
            for cond,body in nd.brs:
                if _truthy(self.ev(cond,env)):self.blk(body,Env(env,"if"));return
            if nd.eb is not None:self.blk(nd.eb,Env(env,"else"))
            return
        if t is SWhile:
            while _truthy(self.ev(nd.cond,env)):
                try:self.blk(nd.body,Env(env,"while"))
                except Brk:break
                except Cont:continue
            return
        if t is SRepeat:
            n=self.ev(nd.cnt,env)
            if not isinstance(n,(int,float)):raise PypError("TypeError",f"'repeat' needs a Number",nd.line)
            for i in range(int(n)):
                loc=Env(env,"repeat")
                if nd.var:loc.set(nd.var,i)
                try:self.blk(nd.body,loc)
                except Brk:break
                except Cont:continue
            return
        if t is SForEach:
            it=self.ev(nd.it,env)
            if isinstance(it,dict):it=list(it.keys())
            elif not isinstance(it,(list,str)):raise PypError("TypeError",f"Cannot iterate {_tn(it)}",nd.line)
            for i,item in enumerate(it):
                loc=Env(env,"for");loc.set(nd.var,item)
                if nd.idx:loc.set(nd.idx,i)
                try:self.blk(nd.body,loc)
                except Brk:break
                except Cont:continue
            return
        if t is SForRange:
            st=int(self.ev(nd.st,env));en=int(self.ev(nd.en,env))
            sp=int(self.ev(nd.sp,env)) if nd.sp else 1
            for i in range(st,en+1,sp):
                loc=Env(env,"range");loc.set(nd.var,i)
                try:self.blk(nd.body,loc)
                except Brk:break
                except Cont:continue
            return
        if t is SReturn:raise Ret(self.ev(nd.ex,env) if nd.ex else None)
        if t is STry:
            try:self.blk(nd.body,Env(env,"try"))
            except PypError as e:
                ok=False
                for et,var,body in nd.catches:
                    if et is None or et==e.et:
                        loc=Env(env,"catch")
                        if var:loc.set(var,{"message":e.msg,"type":e.et})
                        self.blk(body,loc);ok=True;break
                if not ok:raise
            finally:
                if nd.fin:self.blk(nd.fin,Env(env,"finally"))
            return
        if t is SRaise:
            msg=_show(self.ev(nd.msg,env)) if nd.msg else "An error occurred"
            raise PypError(nd.et,msg,nd.line)
        if t is SImport:self._import(nd,env);return
        if t is SSay:print(_show(self.ev(nd.ex,env)));return
        if t is SCtrl:
            if nd.k=="break":raise Brk()
            raise Cont()
        if t is SMySet:
            inst=env.get("__self__",nd.line)
            inst.set(nd.at,self.ev(nd.v,env));return
        if t is SAdd:
            lst=env.get(nd.tgt,nd.line)
            if not isinstance(lst,list):raise PypError("TypeError",f"'add to' needs a List",nd.line)
            lst.append(self.ev(nd.item,env));return
        if t is SRemove:
            lst=env.get(nd.tgt,nd.line);item=self.ev(nd.item,env)
            if not isinstance(lst,list):raise PypError("TypeError",f"'remove from' needs a List",nd.line)
            if item not in lst:raise PypError("ValueError",f"'{_show(item)}' not in list",nd.line)
            lst.remove(item);return
        if t is SExpr:self.ev(nd.ex,env);return

    def ev(self,nd,env):
        t=type(nd)
        if t is ENum:return nd.v
        if t is EStr:return nd.v
        if t is EBool:return nd.v
        if t is ENone:return None
        if t is EId:return env.get(nd.nm,nd.line)
        if t is EMyAttr:return env.get("__self__",nd.line).get(nd.at,nd.line)
        if t is EInterp:return "".join(_show(self.ev(p,env)) for p in nd.parts)
        if t is EBinOp:
            l=self.ev(nd.l,env);r=self.ev(nd.r,env)
            return self._binop(nd.op,l,r,nd.line)
        if t is EUnary:
            v=self.ev(nd.x,env)
            if nd.op=="-":
                if not isinstance(v,(int,float)):raise PypError("TypeError",f"Can't negate {_tn(v)}",nd.line)
                return -v
            return not _truthy(v)
        if t is ECmp:
            l=self.ev(nd.l,env);r=self.ev(nd.r,env)
            try:
                op=nd.op
                if op=="==":return l==r
                if op=="!=":return l!=r
                if op==">":return l>r
                if op=="<":return l<r
                if op==">=":return l>=r
                if op=="<=":return l<=r
            except TypeError:raise PypError("TypeError",f"Can't compare {_tn(l)} and {_tn(r)}",nd.line)
        if t is ELogic:
            l=self.ev(nd.l,env)
            if nd.op==T.AND:return l if not _truthy(l) else self.ev(nd.r,env)
            return l if _truthy(l) else self.ev(nd.r,env)
        if t is EList:return[self.ev(x,env) for x in nd.items]
        if t is EMap:return{self.ev(k,env):self.ev(v,env) for k,v in nd.pairs}
        if t is ELen:
            obj=self.ev(nd.obj,env)
            if isinstance(obj,(list,dict,str)):return len(obj)
            raise PypError("TypeError",f"'count of' doesn't work on {_tn(obj)}",nd.line)
        if t is EIndex:
            obj=self.ev(nd.obj,env);idx=self.ev(nd.idx,env)
            if isinstance(obj,list):
                try:return obj[int(idx)]
                except IndexError:raise PypError("IndexError",f"Index {idx} out of range (list has {len(obj)} items)",nd.line)
            if isinstance(obj,dict):
                if idx not in obj:raise PypError("KeyError",f"Key '{idx}' not in Map. Keys: {list(obj)}",nd.line)
                return obj[idx]
            if isinstance(obj,str):
                try:return obj[int(idx)]
                except IndexError:raise PypError("IndexError",f"Character index {idx} out of range",nd.line)
            raise PypError("TypeError",f"Can't index into {_tn(obj)}",nd.line)
        if t is EAttr:
            obj=self.ev(nd.obj,env)
            if isinstance(obj,Inst):return obj.get(nd.nm,nd.line)
            if isinstance(obj,dict):
                if nd.nm=="message":return obj.get("message","")
                if nd.nm in obj:return obj[nd.nm]
            if isinstance(obj,(str,list)) and nd.nm=="length":return len(obj)
            raise PypError("AttributeError",f"{_tn(obj)} has no attribute '{nd.nm}'",nd.line)
        if t is ECall:
            args=[self.ev(a,env) for a in nd.args]
            # Handle internal my-list operations
            if isinstance(nd.f,EId) and nd.f.nm in('__list_add_my__','__list_rm_my__'):
                attr=args[0];item=args[1]
                inst=env.get('__self__',nd.line)
                lst=inst.get(attr,nd.line)
                if not isinstance(lst,list):raise PypError('TypeError',f'my {attr} is not a List',nd.line)
                if nd.f.nm=='__list_add_my__':lst.append(item)
                else:
                    if item not in lst:raise PypError('ValueError',f'{_show(item)!r} not in list',nd.line)
                    lst.remove(item)
                return None
            return self._call(nd.f,args,env,nd.line)
        if t is EMeth:
            obj=self.ev(nd.obj,env);args=[self.ev(a,env) for a in nd.args]
            return self._meth(obj,nd.nm,args,nd.line)
        if t is ENew:
            cls=env.get(nd.cls,nd.line)
            if not isinstance(cls,Cls):raise PypError("TypeError",f"'{nd.cls}' is not a class",nd.line)
            args=[self.ev(a,env) for a in nd.args]
            return self._new(cls,args,nd.line)
        if t is EIsType:
            obj=self.ev(nd.obj,env)
            MAP={"Integer":int,"Decimal":float,"Text":str,"Boolean":bool,"List":list,"Map":dict}
            if nd.tn in MAP:return isinstance(obj,MAP[nd.tn])
            if isinstance(obj,Inst):
                klass=obj.cls
                while klass:
                    if klass.nm==nd.tn:return True
                    klass=klass.par
            return False
        if t is EAsk:
            prompt=_show(self.ev(nd.prompt,env))
            try:
                ans=input(prompt)
                if nd.num:
                    try:return int(ans) if "." not in ans else float(ans)
                    except ValueError:raise PypError("ValueError",f"'{ans}' is not a number")
                return ans
            except EOFError:return ""
        if t is EParent:
            inst=env.get("__self__",nd.line)
            pcls=inst.cls.par
            if not pcls:raise PypError("TypeError",f"'{inst.cls.nm}' has no parent",nd.line)
            meth="__init__" if nd.meth=="setup" else nd.meth
            fn=pcls.ctor if meth=="__init__" and pcls.ctor else pcls.meths.get(meth)
            if not fn:raise PypError("AttributeError",f"Parent '{pcls.nm}' has no method '{nd.meth}'",nd.line)
            args=[self.ev(a,env) for a in nd.args]
            return self._callfn(fn,args,pcls.env,inst)
        raise PypError("InternalError",f"Unknown node {type(nd).__name__}")

    def _call(self,fn_node,args,env,line):
        fn=self.ev(fn_node,env)
        if isinstance(fn,Func):return self._callfn(fn,args,fn.env)
        if isinstance(fn,Cls):return self._new(fn,args,line)
        if isinstance(fn,Bound):return self._callfn(fn.fn,args,fn.fn.env,fn.inst)
        if callable(fn):return fn(args)
        raise PypError("TypeError",f"'{getattr(fn_node,'nm','?')}' is not a function (it's a {_tn(fn)})",line)

    def _meth(self,obj,nm,args,line):
        if isinstance(obj,str):
            m={"upper":lambda:obj.upper(),"lower":lambda:obj.lower(),"strip":lambda:obj.strip(),
               "contains":lambda:args[0] in obj,"startswith":lambda:obj.startswith(args[0]),
               "endswith":lambda:obj.endswith(args[0]),
               "split":lambda:obj.split(args[0]) if args else obj.split(),
               "replace":lambda:obj.replace(args[0],args[1]),"length":lambda:len(obj)}
            if nm in m:return m[nm]()
            raise PypError("AttributeError",f"Text has no method '{nm}'",line)
        if isinstance(obj,list):
            if nm=="contains":return args[0] in obj
            if nm=="length":return len(obj)
            if nm=="sort":obj.sort();return obj
            if nm=="reverse":obj.reverse();return obj
            if nm=="join":return args[0].join(_show(x) for x in obj)
            if nm=="append":obj.append(args[0]);return None
            raise PypError("AttributeError",f"List has no method '{nm}'",line)
        if isinstance(obj,dict):
            if nm in("contains","has"):return args[0] in obj
            if nm=="keys":return list(obj.keys())
            if nm=="values":return list(obj.values())
            if nm in obj:fn=obj[nm];return fn(args) if callable(fn) else fn
            raise PypError("AttributeError",f"Map has no method '{nm}'",line)
        if isinstance(obj,Inst):
            attr=obj.get(nm,line)
            if isinstance(attr,Bound):return self._callfn(attr.fn,args,attr.fn.env,obj)
            if callable(attr):return attr(args)
            return attr
        raise PypError("TypeError",f"Cannot call method '{nm}' on {_tn(obj)}",line)

    def _callfn(self,fn,args,cenv,inst=None):
        loc=Env(cenv if isinstance(cenv,Env) else self.G,fn.nm)
        if inst:loc.set("__self__",inst)
        req=[p for p in fn.ps if p[2] is None]
        if len(args)<len(req):
            miss=[p[0] for p in req][len(args):]
            raise PypError("ArgumentError",
                f"'{fn.nm}' needs {len(fn.ps)} arg(s) but got {len(args)}.\n  Missing: {', '.join(miss)}")
        for i,(pnm,_,pdef) in enumerate(fn.ps):
            if i<len(args):loc.set(pnm,args[i])
            elif pdef is not None:loc.set(pnm,self.ev(pdef,cenv))
        try:self.blk(fn.body,loc);return None
        except Ret as r:return r.v

    def _new(self,cls,args,line):
        inst=Inst(cls)
        klass=cls
        while klass:
            for fn,_ in klass.flds:inst.attrs.setdefault(fn,None)
            klass=klass.par
        if cls.ctor:self._callfn(cls.ctor,args,cls.env,inst)
        elif args:raise PypError("TypeError",f"'{cls.nm}' has no setup constructor but got args",line)
        return inst

    def _binop(self,op,l,r,line):
        try:
            if op=="+":
                if isinstance(l,str) or isinstance(r,str):return _show(l)+_show(r)
                return l+r
            if op=="-":return l-r
            if op=="*":return l*r
            if op=="/":
                if r==0:raise PypError("DivisionError",f"Cannot divide {_show(l)} by zero",line)
                return l/r
            if op=="%":
                if r==0:raise PypError("DivisionError","Cannot mod by zero",line)
                return l%r
            if op=="**":return l**r
        except PypError:raise
        except TypeError:
            raise PypError("TypeError",
                f"Cannot do {_tn(l)} {op} {_tn(r)}.\n  Left={_show(l)!r}  Right={_show(r)!r}",line)

    def _import(self,nd,env):
        src=nd.src
        if src in self._mods:
            mod=self._mods[src]
            for nm in nd.nms:
                if nm not in mod:raise PypError("ImportError",f"'{src}' has no '{nm}'",nd.line)
                env.set(nm,mod[nm])
            return
        if src is None:
            for nm in nd.nms:
                if nm in self._mods:env.set(nm,self._mods[nm])
                else:raise PypError("ImportError",
                    f"Unknown module '{nm}'. Built-ins: {', '.join(self._mods)}",nd.line)
            return
        path=src if src.endswith(".pyp") else src+".pyp"
        if not os.path.exists(path):
            raise PypError("ImportError",f"File not found: '{path}'",nd.line)
        with open(path) as f:code=f.read()
        sub=Interp(path)
        toks=lex(code,path);sub.run(Parser(toks,code.splitlines(),path).parse())
        for nm in nd.nms:
            if nm not in sub.G.v:raise PypError("ImportError",f"'{path}' has no '{nm}'",nd.line)
            env.set(nm,sub.G.v[nm])

# ── 7. HELPERS ────────────────────────────────────────────────────────────────
def compile_src(code,fn="<input>"):
    toks=lex(code,fn)
    return Parser(toks,code.splitlines(),fn).parse()

def run_code(code,fn="<input>"):
    stmts=compile_src(code,fn)
    interp=Interp(fn);interp.run(stmts)

def fmt_err(e,fn,lines):
    ln=getattr(e,"line",None)
    src=f"\n  \033[90m→ {lines[ln-1]}\033[0m" if ln and 0<ln<=len(lines) else""
    return(f"\n\033[1;31m{'─'*54}\033[0m\n\033[1;31m{e.et}\033[0m"
           +(f" (line {ln})" if ln else "")+f"\n  {e.msg}{src}\n"
           +f"\033[1;31m{'─'*54}\033[0m\n")

# ── 8. REPL ───────────────────────────────────────────────────────────────────
BANNER="\033[1;36m\n  ██████╗ ██╗   ██╗ ██╗\n  ██╔══██╗╚██╗ ██╔╝██╔╝\n  ██████╔╝ ╚████╔╝██╔╝ \n  ██╔═══╝   ╚██╔╝██╔╝  \n  ██║        ██║ ██╔╝   \033[0m\033[1m  py+ v1.0 — type help or quit\033[0m\n"
HELP="""
\033[1;33m── py+ Quick Reference ─────────────────────────────\033[0m
 \033[36mVariables:\033[0m   set x to 5        change x to 10
 \033[36mOutput:\033[0m      say "Hello, {x}!"
 \033[36mInput:\033[0m       set name to ask "Name? "
              set age to ask number "Age? "
 \033[36mMath:\033[0m        x + y  x - y  x * y  x / y  x % y  x ** 2
              x plus y  x minus y  x times y  x divided by y
 \033[36mCompare:\033[0m     x is greater than y    x is equal to y
              x is less than or equal to y    x == y  x != y
 \033[36mLogic:\033[0m       if x > 0 and y > 0:   not active
 \033[36mIf/else:\033[0m     if x > 5:   else if x > 0:   else:
 \033[36mLoops:\033[0m       repeat 10 times with i:
              while x < 100:
              for each item in my_list:
              for each n from 1 to 10:
              for each n from 0 to 100 step 5:
              stop loop    skip to next
 \033[36mFunctions:\033[0m   define add with a, b:
                  give back a + b
              add(3, 4)   add with 3, 4
 \033[36mClasses:\033[0m     class Dog extends Animal:
                  has name
                  setup with name:
                      my name is name
              set d to new Dog with "Rex"
              d.speak()
 \033[36mErrors:\033[0m      try:  catch ValueError as e:  finally:
              raise TypeError with "bad input"
 \033[36mImports:\033[0m     use math    use sqrt from math
 \033[36mLists:\033[0m       add item to my_list    remove item from my_list
              count of my_list    my_list at 0
 \033[36mStrings:\033[0m     msg in uppercase    msg trimmed
              "hello" contains "ell"    "a,b" split by ","
 \033[36mComments:\033[0m    -- single line    --- multi line ---
\033[1;33m────────────────────────────────────────────────────\033[0m
"""

def run_repl():
    print(BANNER)
    interp=Interp("<repl>")
    while True:
        try:line=input("\033[1;32mpy+>\033[0m ")
        except(EOFError,KeyboardInterrupt):print("\n\033[90mGoodbye!\033[0m");break
        cmd=line.strip().lower()
        if not line.strip():continue
        if cmd in("quit","exit","bye"):print("\033[90mGoodbye!\033[0m");break
        if cmd=="help":print(HELP);continue
        if cmd=="clear":print("\033[2J\033[H",end="");continue
        code=line
        if line.rstrip().endswith(":"):
            while True:
                try:cont=input("\033[36m...>\033[0m ")
                except(EOFError,KeyboardInterrupt):break
                if not cont.strip():break
                code+="\n"+cont
        src_lines=code.splitlines()
        try:
            toks=lex(code,"<repl>")
            stmts=Parser(toks,src_lines,"<repl>").parse()
            for s in stmts:
                if not s:continue
                if type(s) is SExpr:
                    r=interp.ev(s.ex,interp.G)
                    if r is not None:print(f"\033[90m→ {_show(r)}\033[0m")
                else:interp.ex(s,interp.G)
        except LexError as e:print(str(e))
        except ParseError as e:print(str(e))
        except PypError as e:print(fmt_err(e,"<repl>",src_lines))
        except Exception as e:print(f"\033[1;31mInternal error: {e}\033[0m")

# ── 9. FILE / CLI ─────────────────────────────────────────────────────────────
def run_file(path):
    if not os.path.exists(path):print(f"\033[1;31mFile not found:\033[0m '{path}'");sys.exit(1)
    with open(path,encoding="utf-8") as f:src=f.read()
    lines=src.splitlines()
    try:
        stmts=compile_src(src,path);interp=Interp(path);interp.run(stmts)
    except LexError as e:print(str(e));sys.exit(1)
    except ParseError as e:print(str(e));sys.exit(1)
    except PypError as e:print(fmt_err(e,path,lines));sys.exit(1)
    except KeyboardInterrupt:print("\n\033[90mStopped.\033[0m");sys.exit(0)

def run_inline(code):
    lines=code.splitlines()
    try:
        stmts=compile_src(code,"-c");interp=Interp("-c");interp.run(stmts)
    except(LexError,ParseError) as e:print(str(e));sys.exit(1)
    except PypError as e:print(fmt_err(e,"-c",lines));sys.exit(1)

def main():
    args=sys.argv[1:]
    if not args:run_repl()
    elif args[0]=="-c" and len(args)>1:run_inline(args[1])
    elif args[0] in("-h","--help"):print(__doc__);print(HELP)
    elif args[0]=="--version":print("py+ 1.0")
    else:run_file(args[0])

if __name__=="__main__":main()


# ── GUI MODULE (tkinter wrapper) ──────────────────────────────────────────────
# Accessed in py+ via:  use window
# All widget objects are py+ Inst-compatible dicts with callable fields.

def _build_window_module():
    """Build the 'window' built-in module backed by tkinter."""
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, filedialog, colorchooser, font as tkfont
    except ImportError:
        def _no_tk(a):
            raise PypError("ImportError",
                "tkinter is not installed.\n"
                "  On Windows/Mac it comes with Python.\n"
                "  On Linux: sudo apt install python3-tk")
        return {k: _no_tk for k in ["app","label","button","entry","text","listbox",
                                     "checkbox","radio","slider","dropdown","canvas",
                                     "frame","image","alert","ask_yes_no","open_file",
                                     "save_file","pick_color"]}

    # ── Widget wrapper ──────────────────────────────────────────────────────
    class Widget:
        """Wraps a tk widget as a py+ Map-like object."""
        def __init__(self, w):
            self._w = w
            self._handlers = {}

        def __getitem__(self, key):
            return getattr(self, key)

        # Common config helper
        def _cfg(self, key, val):
            try: self._w.config(**{key: val})
            except tk.TclError: pass

        def get(self, k, line=None):
            m = {
                "show":       lambda: (self._w.pack(padx=5, pady=5), self)[1],
                "hide":       lambda: (self._w.pack_forget(), self)[1],
                "destroy":    lambda: self._w.destroy(),
                "config":     self._do_config,
                "on_click":   self._on_click,
                "on_change":  self._on_change,
                "on_key":     self._on_key,
                "set_text":   self._set_text,
                "get_text":   self._get_text,
                "add_item":   self._add_item,
                "clear":      self._clear,
                "set_color":  self._set_color,
                "set_size":   self._set_size,
                "set_font":   self._set_font,
                "draw_rect":  self._draw_rect,
                "draw_oval":  self._draw_oval,
                "draw_line":  self._draw_line,
                "draw_text":  self._draw_text,
                "clear_canvas": self._clear_canvas,
                "width":      getattr(self._w, 'winfo_width', lambda: 0)(),
                "height":     getattr(self._w, 'winfo_height', lambda: 0)(),
            }
            if k in m:
                v = m[k]
                return (lambda fn: (lambda args: fn()))(v) if callable(v) and not isinstance(v, type) else v
            raise PypError("AttributeError", f"Widget has no property '{k}'", line)

        def _do_config(self, args):
            if len(args) >= 2:
                self._cfg(str(args[0]), args[1])
            return self

        def _on_click(self, args):
            if args: self._w.config(command=lambda: args[0]([]))
            return self

        def _on_change(self, args):
            if args and hasattr(self._w, 'bind'):
                cb = args[0]
                self._w.bind("<KeyRelease>", lambda e: cb([]))
                if hasattr(self._w, 'trace_add'):
                    pass
            return self

        def _on_key(self, args):
            if len(args) >= 2 and hasattr(self._w, 'bind'):
                key, cb = args[0], args[1]
                self._w.bind(f"<{key}>", lambda e: cb([]))
            return self

        def _set_text(self, args):
            val = _show(args[0]) if args else ""
            if isinstance(self._w, (tk.Label, tk.Button)):
                self._w.config(text=val)
            elif isinstance(self._w, tk.Entry):
                self._w.delete(0, tk.END); self._w.insert(0, val)
            elif isinstance(self._w, tk.Text):
                self._w.delete("1.0", tk.END); self._w.insert("1.0", val)
            return self

        def _get_text(self, args):
            if isinstance(self._w, tk.Entry):
                return self._w.get()
            elif isinstance(self._w, tk.Text):
                return self._w.get("1.0", tk.END).rstrip("\n")
            elif isinstance(self._w, tk.Label):
                return self._w.cget("text")
            return ""

        def _add_item(self, args):
            val = _show(args[0]) if args else ""
            if isinstance(self._w, tk.Listbox):
                self._w.insert(tk.END, val)
            elif isinstance(self._w, ttk.Combobox):
                cur = list(self._w["values"])
                cur.append(val)
                self._w["values"] = cur
            return self

        def _clear(self, args):
            if isinstance(self._w, tk.Listbox):
                self._w.delete(0, tk.END)
            elif isinstance(self._w, tk.Text):
                self._w.delete("1.0", tk.END)
            elif isinstance(self._w, tk.Entry):
                self._w.delete(0, tk.END)
            return self

        def _set_color(self, args):
            if args:
                self._cfg("bg", str(args[0]))
                try: self._cfg("fg", str(args[1]) if len(args) > 1 else None)
                except: pass
            return self

        def _set_size(self, args):
            if len(args) >= 2:
                try: self._w.config(width=int(args[0]), height=int(args[1]))
                except: pass
            return self

        def _set_font(self, args):
            if args:
                name  = str(args[0]) if args else "Arial"
                size  = int(args[1]) if len(args) > 1 else 12
                style = str(args[2]) if len(args) > 2 else "normal"
                try: self._cfg("font", (name, size, style))
                except: pass
            return self

        # Canvas drawing helpers
        def _draw_rect(self, args):
            if len(args) >= 4:
                x, y, w, h = int(args[0]), int(args[1]), int(args[2]), int(args[3])
                color = str(args[4]) if len(args) > 4 else "blue"
                self._w.create_rectangle(x, y, x+w, y+h, fill=color, outline=color)
            return self

        def _draw_oval(self, args):
            if len(args) >= 4:
                x, y, w, h = int(args[0]), int(args[1]), int(args[2]), int(args[3])
                color = str(args[4]) if len(args) > 4 else "red"
                self._w.create_oval(x, y, x+w, y+h, fill=color, outline=color)
            return self

        def _draw_line(self, args):
            if len(args) >= 4:
                x1, y1, x2, y2 = int(args[0]), int(args[1]), int(args[2]), int(args[3])
                color = str(args[4]) if len(args) > 4 else "black"
                width = int(args[5]) if len(args) > 5 else 2
                self._w.create_line(x1, y1, x2, y2, fill=color, width=width)
            return self

        def _draw_text(self, args):
            if len(args) >= 3:
                x, y, text = int(args[0]), int(args[1]), str(args[2])
                color = str(args[3]) if len(args) > 3 else "black"
                size  = int(args[4]) if len(args) > 4 else 14
                self._w.create_text(x, y, text=text, fill=color,
                                    font=("Arial", size), anchor="nw")
            return self

        def _clear_canvas(self, args):
            self._w.delete("all"); return self

    # ── App (root window) ──────────────────────────────────────────────────
    class App:
        def __init__(self, title="py+ App", width=400, height=300, bg="#f0f0f0"):
            self._root = tk.Tk()
            self._root.title(title)
            self._root.geometry(f"{width}x{height}")
            self._root.configure(bg=bg)
            self._root.resizable(True, True)
            # Style
            style = ttk.Style()
            try: style.theme_use("clam")
            except: pass

        def get(self, k, line=None):
            m = {
                "run":        lambda: (lambda a: self._root.mainloop()),
                "title":      lambda: (lambda a: self._root.title(str(a[0]))),
                "size":       lambda: (lambda a: self._root.geometry(f"{int(a[0])}x{int(a[1])}")),
                "color":      lambda: (lambda a: self._root.configure(bg=str(a[0]))),
                "on_close":   lambda: (lambda a: self._root.protocol("WM_DELETE_WINDOW", lambda: a[0]([]))),
                "quit":       lambda: (lambda a: self._root.destroy()),
                "center":     lambda: (lambda a: self._center()),
                "resizable":  lambda: (lambda a: self._root.resizable(bool(a[0]), bool(a[0]))),
                "icon":       lambda: (lambda a: None),  # no-op without image file
                "_root":      self._root,
            }
            if k in m:
                v = m[k]
                return v() if callable(v) else v
            raise PypError("AttributeError", f"App has no property '{k}'", line)

        def _center(self):
            self._root.update_idletasks()
            w = self._root.winfo_width()
            h = self._root.winfo_height()
            sw = self._root.winfo_screenwidth()
            sh = self._root.winfo_screenheight()
            x = (sw - w) // 2
            y = (sh - h) // 2
            self._root.geometry(f"+{x}+{y}")

    # ── Module factory functions ────────────────────────────────────────────

    def _get_root(parent):
        if parent is None: return None
        if isinstance(parent, App): return parent._root
        if isinstance(parent, Widget): return parent._w
        return None

    def mk_app(args):
        title  = str(args[0]) if len(args) > 0 else "py+ App"
        width  = int(args[1]) if len(args) > 1 else 500
        height = int(args[2]) if len(args) > 2 else 400
        bg     = str(args[3]) if len(args) > 3 else "#f5f5f5"
        return App(title, width, height, bg)

    def mk_label(args):
        parent = _get_root(args[0]) if args else None
        text   = str(args[1]) if len(args) > 1 else "Label"
        bg     = str(args[2]) if len(args) > 2 else None
        fg     = str(args[3]) if len(args) > 3 else "#222222"
        w = tk.Label(parent, text=text, fg=fg,
                     bg=bg or (parent.cget("bg") if parent else "#f5f5f5"),
                     font=("Arial", 13), pady=4)
        w.pack(padx=8, pady=4)
        return Widget(w)

    def mk_button(args):
        parent  = _get_root(args[0]) if args else None
        text    = str(args[1]) if len(args) > 1 else "Button"
        on_click= args[2] if len(args) > 2 else None
        bg      = str(args[3]) if len(args) > 3 else "#4a90d9"
        fg      = str(args[4]) if len(args) > 4 else "white"
        cmd     = (lambda: on_click([])) if on_click else None
        w = tk.Button(parent, text=text, command=cmd,
                      bg=bg, fg=fg, relief="flat",
                      font=("Arial", 12, "bold"),
                      padx=12, pady=6, cursor="hand2",
                      activebackground="#357abd", activeforeground="white")
        w.pack(padx=8, pady=4)
        return Widget(w)

    def mk_entry(args):
        parent      = _get_root(args[0]) if args else None
        placeholder = str(args[1]) if len(args) > 1 else ""
        secret      = bool(args[2]) if len(args) > 2 else False
        show_char   = "*" if secret else ""
        w = tk.Entry(parent, show=show_char, font=("Arial", 12),
                     relief="solid", bd=1)
        w.pack(padx=8, pady=4, fill="x")
        if placeholder:
            w.insert(0, placeholder)
            w.config(fg="#aaaaaa")
            def _focus_in(e):
                if w.get() == placeholder:
                    w.delete(0, tk.END); w.config(fg="#222222")
            def _focus_out(e):
                if not w.get():
                    w.insert(0, placeholder); w.config(fg="#aaaaaa")
            w.bind("<FocusIn>", _focus_in)
            w.bind("<FocusOut>", _focus_out)
        return Widget(w)

    def mk_text(args):
        parent = _get_root(args[0]) if args else None
        rows   = int(args[1]) if len(args) > 1 else 6
        w = tk.Text(parent, height=rows, font=("Arial", 12),
                    relief="solid", bd=1, wrap="word")
        w.pack(padx=8, pady=4, fill="both", expand=True)
        return Widget(w)

    def mk_listbox(args):
        parent = _get_root(args[0]) if args else None
        rows   = int(args[1]) if len(args) > 1 else 6
        items  = args[2] if len(args) > 2 and isinstance(args[2], list) else []
        frame  = tk.Frame(parent)
        frame.pack(padx=8, pady=4, fill="both")
        sb = tk.Scrollbar(frame)
        sb.pack(side="right", fill="y")
        w = tk.Listbox(frame, height=rows, yscrollcommand=sb.set,
                       font=("Arial", 12), relief="solid", bd=1,
                       selectbackground="#4a90d9", selectforeground="white")
        sb.config(command=w.yview)
        w.pack(side="left", fill="both", expand=True)
        for item in items: w.insert(tk.END, str(item))
        wgt = Widget(w)
        # extra: get_selected
        def _get_selected(a):
            sel = w.curselection()
            if sel: return w.get(sel[0])
            return nothing
        orig_get = wgt.get
        def patched_get(k, line=None):
            if k == "get_selected": return lambda a: _get_selected(a)
            return orig_get(k, line)
        wgt.get = patched_get
        return wgt

    def mk_checkbox(args):
        parent = _get_root(args[0]) if args else None
        text   = str(args[1]) if len(args) > 1 else "Checkbox"
        var    = tk.BooleanVar()
        w = tk.Checkbutton(parent, text=text, variable=var,
                           font=("Arial", 12), pady=4,
                           bg=parent.cget("bg") if parent else "#f5f5f5")
        w.pack(padx=8, pady=2, anchor="w")
        wgt = Widget(w)
        orig_get = wgt.get
        def patched(k, line=None):
            if k == "checked": return lambda a: var.get()
            if k == "on_change":
                return lambda a: (var.trace_add("write", lambda *_: a[0]([])), None)[1]
            return orig_get(k, line)
        wgt.get = patched
        return wgt

    def mk_slider(args):
        parent = _get_root(args[0]) if args else None
        lo     = float(args[1]) if len(args) > 1 else 0
        hi     = float(args[2]) if len(args) > 2 else 100
        init   = float(args[3]) if len(args) > 3 else lo
        var    = tk.DoubleVar(value=init)
        w = tk.Scale(parent, from_=lo, to=hi, orient="horizontal",
                     variable=var, font=("Arial", 10),
                     bg=parent.cget("bg") if parent else "#f5f5f5",
                     troughcolor="#c0d8f0", sliderrelief="flat")
        w.pack(padx=8, pady=4, fill="x")
        wgt = Widget(w)
        orig_get = wgt.get
        def patched(k, line=None):
            if k == "value": return lambda a: var.get()
            if k == "on_change":
                return lambda a: w.config(command=lambda v: a[0]([float(v)]))
            return orig_get(k, line)
        wgt.get = patched
        return wgt

    def mk_dropdown(args):
        parent  = _get_root(args[0]) if args else None
        options = args[1] if len(args) > 1 and isinstance(args[1], list) else []
        var     = tk.StringVar()
        w = ttk.Combobox(parent, textvariable=var, state="readonly",
                         values=[str(o) for o in options], font=("Arial", 12))
        if options: w.current(0)
        w.pack(padx=8, pady=4, fill="x")
        wgt = Widget(w)
        orig_get = wgt.get
        def patched(k, line=None):
            if k == "selected": return lambda a: var.get()
            if k == "on_change":
                return lambda a: w.bind("<<ComboboxSelected>>", lambda e: a[0]([var.get()]))
            return orig_get(k, line)
        wgt.get = patched
        return wgt

    def mk_canvas(args):
        parent = _get_root(args[0]) if args else None
        w_px   = int(args[1]) if len(args) > 1 else 400
        h_px   = int(args[2]) if len(args) > 2 else 300
        bg     = str(args[3]) if len(args) > 3 else "white"
        w = tk.Canvas(parent, width=w_px, height=h_px, bg=bg,
                      relief="solid", bd=1)
        w.pack(padx=8, pady=4)
        return Widget(w)

    def mk_frame(args):
        parent  = _get_root(args[0]) if args else None
        side    = str(args[1]) if len(args) > 1 else "top"
        padding = int(args[2]) if len(args) > 2 else 4
        bg      = str(args[3]) if len(args) > 3 else (parent.cget("bg") if parent else "#f5f5f5")
        w = tk.Frame(parent, bg=bg)
        pack_sides = {"left":"left","right":"right","top":"top","bottom":"bottom"}
        w.pack(side=pack_sides.get(side,"top"), padx=padding, pady=padding,
               fill="both", expand=True)
        wgt = Widget(w)
        # frame acts as parent for child widgets
        wgt._w = w
        return wgt

    nothing = None  # py+ nothing

    # ── Dialog helpers ───────────────────────────────────────────────────────
    def dlg_alert(args):
        title = str(args[0]) if args else "Alert"
        msg   = str(args[1]) if len(args) > 1 else ""
        messagebox.showinfo(title, msg)
        return None

    def dlg_ask_yes_no(args):
        title = str(args[0]) if args else "Question"
        msg   = str(args[1]) if len(args) > 1 else ""
        return messagebox.askyesno(title, msg)

    def dlg_open_file(args):
        filetypes = [("All files", "*.*")]
        result = filedialog.askopenfilename(filetypes=filetypes)
        return result if result else nothing

    def dlg_save_file(args):
        result = filedialog.asksaveasfilename()
        return result if result else nothing

    def dlg_pick_color(args):
        result = colorchooser.askcolor()
        return str(result[1]) if result and result[1] else nothing

    return {
        "app":        mk_app,
        "label":      mk_label,
        "button":     mk_button,
        "entry":      mk_entry,
        "text":       mk_text,
        "listbox":    mk_listbox,
        "checkbox":   mk_checkbox,
        "slider":     mk_slider,
        "dropdown":   mk_dropdown,
        "canvas":     mk_canvas,
        "frame":      mk_frame,
        "alert":      dlg_alert,
        "ask_yes_no": dlg_ask_yes_no,
        "open_file":  dlg_open_file,
        "save_file":  dlg_save_file,
        "pick_color": dlg_pick_color,
    }

# ── Patch GUI into Interp._mods ───────────────────────────────────────────────
_orig_interp_init = Interp.__init__
def _patched_interp_init(self, fn="<input>"):
    _orig_interp_init(self, fn)
    self._mods["window"] = _build_window_module()
    # Also handle widget method calls through _meth
Interp.__init__ = _patched_interp_init

# Patch _meth to handle Widget / App objects from window module
_orig_meth = Interp._meth
def _patched_meth(self, obj, nm, args, line):
    # Widget and App objects from the window module
    if hasattr(obj, 'get') and hasattr(obj, '_w'):  # Widget
        fn = obj.get(nm, line)
        if callable(fn): return fn(args)
        return fn
    if hasattr(obj, 'get') and hasattr(obj, '_root'):  # App
        fn = obj.get(nm, line)
        if callable(fn): return fn(args)
        return fn
    return _orig_meth(self, obj, nm, args, line)
Interp._meth = _patched_meth

# Patch EAttr eval to handle Widget/App attribute access
_orig_ev = Interp.ev
def _patched_ev(self, nd, env):
    if type(nd) is EAttr:
        obj = self.ev(nd.obj, env)
        if hasattr(obj, 'get') and (hasattr(obj, '_w') or hasattr(obj, '_root')):
            fn = obj.get(nd.nm, nd.line)
            if callable(fn): return fn([])
            return fn
    return _orig_ev(self, nd, env)
Interp.ev = _patched_ev
