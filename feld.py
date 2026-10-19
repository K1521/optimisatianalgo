import numpy as np
import copy
class Rect:
    def __init__(self,w,h):
        self.w=w
        self.h=h

    def __iter__(self):
        yield self.w
        yield self.h

class Box:
    def __init__(self,L):
        self.L=L
        self.gesetzt=dict()
        self.feld=np.zeros((L,L),bool)


    def setze(self,rect,orientation,pos,check=True):
        if check:
            assert self.setzenmoeglich(rect,orientation,pos)
        self.gesetzt[rect]=(pos,orientation)
        x,y=pos
        w,h=rect
        if orientation:
            w,h=h,w
        self.feld[y:y+h,x:x+w]=True

    def remove(self,rect):
        # assert rect in self.gesetzt
        # (pos,orientation)=self.gesetzt[rect]
        # del self.gesetzt[rect]
        (pos,orientation)=self.gesetzt.pop(rect)
        x,y=pos
        w,h=rect
        if orientation:
            w,h=h,w
        self.feld[y:y+h,x:x+w]=False
        

    
    def setzenmoeglich(self,rect,orientation,pos):
        if rect in self.gesetzt:
            return False
        x,y=pos
        w,h=rect
        L=self.L
        if orientation:
            w,h=h,w
        if x+w>L or y+h>L:
            return False
        return not self.feld[y:y+h,x:x+w].any()
    def posibleplaces(self,rect,orientation):
        w,h=rect
        if orientation:
            w,h=h,w
        #self.spacetotop=np.zeros((self.L,self.L),np.int16)
        acc=np.full(self.L,0,np.int16)
        #m=[]
        for i in reversed(range(self.L)):
            #acc=np.where(self.feld[i],-1,acc)+1
            acc+=1
            acc[self.feld[i]]=0
            #self.spacetotop[i]=acc

            heightfitcount=0
            for j in reversed(range(self.L)):
                if acc[j]>=h:
                    heightfitcount+=1
                    if heightfitcount>=w:
                        yield j,i
                        #m.append((j,i))
                else:
                    heightfitcount=0

        #return m
    
    def mkfieldint(self,edges=False):
        intfield=np.zeros((self.L,self.L),np.int16)
        for i,(rect,(pos,orientation)) in enumerate(self.gesetzt.items(),start=1):
            #(pos,orientation)=self.gesetzt[rect]
            x,y=pos
            w,h=rect
            if orientation:
                w,h=h,w
            if edges:
                intfield[y:y+h,x:x+w]=-i
                intfield[y+1:y+h-1,x+1:x+w-1]=i
            else:
                intfield[y:y+h,x:x+w]=i
        return intfield



    def print(self,printids=True):
        intfield=self.mkfieldint()
        import random
        r=random.Random(1234567)
        reset="\x1b[0m"
        colors=[f"\x1b[48;2;{r.randint(10,245)};{r.randint(10,245)};{r.randint(10,245)}m" for i in range(len(self.gesetzt))]
        colors.insert(0,"\x1b[48;2;0;0;0m")
        #resetcolors = "\x1b[0m"
        #errorcolor = "\x1b[48;2;255;255;255m"
        #print(intfield)
        import string
        ids=" "+ string.digits + string.ascii_letters + string.punctuation
        
        for row in intfield:
            lastcolor=reset
            s=[]
            for cell in row:
                color=colors[cell]
                
                if color!=lastcolor:
                    s.append(color)
                    lastcolor=color
                if printids:
                    s.append(ids[cell%len(ids)]*2)
                else:
                    s.append("  ")
            s.append(reset)
            print("".join(s))



        



# box=Box(5)
# rect=Rect(2,3)
# rect2=Rect(3,2)
# rect3=Rect(3,3)
# for pos in box.posibleplaces(rect,False):
#     #if box.setzenmoeglich(rect,False,pos):
#     box.setze(rect,False,pos)
#     for pos in box.posibleplaces(rect2,False):
#         box.setze(rect2,False,pos)
#         for pos in box.posibleplaces(rect3,False):
#             box.setze(rect3,False,pos)
#             box.print()
#             print()
#             box.remove(rect3)
#         box.remove(rect2)
        

#     #print(box.feld)
#     box.remove(rect)
    

def bruteforceandprintsolutions(rects,L,maxsteps=1000000):
    steps=0
    nbest=-1
    boxbest=None
    box=Box(L)
    def rec(i,n):
        nonlocal nbest,boxbest,steps,box
        if steps>maxsteps:
            return
        steps+=1
        if n>nbest:
            nbest=n
            boxbest=copy.deepcopy(box)
            box.print()
            print()

        if i>=len(rects):
            return
        #     box.print()
        #     print()
        #     return
        
        
        rect=rects[i]
        n2=n+rect.w*rect.h
        if n2<=L*L:
            for pos in box.posibleplaces(rect,False):
                box.setze(rect,False,pos)
                rec(i+1,n2)
                box.remove(rect)
            if rect.w!=rect.h:
                for pos in box.posibleplaces(rect,True):
                    box.setze(rect,True,pos)
                    rec(i+1,n2)
                    box.remove(rect)
        rec(i+1,n)
    rec(0,0)
    print("bestfound")
    boxbest.print()
    print()
    print("steps=",steps)

    
#bruteforceandprintsolutions([Rect(2,3),Rect(2,3),Rect(2,3),Rect(2,3),Rect(2,2)],5)

L = 20
rects = [
    (8, 7), (8, 7),
    (7, 8), (7, 8),
    (5, 5), (5, 5), (5, 5),
    (5, 5), (5, 5), (5, 5),
    (5, 5), (5, 5), (5, 5),
]
import cProfile
import pstats
profiler = cProfile.Profile()
profiler.enable()

bruteforceandprintsolutions(
    [Rect(*x) for x in rects],
    L,
    maxsteps=100_000
)

profiler.disable()

stats = pstats.Stats(profiler)
stats.strip_dirs().sort_stats("cumulative").print_stats(25)