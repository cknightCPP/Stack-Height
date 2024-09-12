import pandas as pd
import numpy as np

def asgn(CondPath, GeomPath, StackPath, RecPath):
    Conditions = pd.read_csv(CondPath, header = [0], index_col = [0])
    Geom = pd.read_csv(GeomPath, header = [0], index_col = [0])
    StackMat = pd.read_csv(StackPath, header = [0], index_col = [0])
    RecMat = pd.read_csv(RecPath, header = [0], index_col = [0])
    return Conditions, Geom, StackMat, RecMat

def count(Conditions, Geom, StackMat, RecMat):
    FeatCount = Geom.shape[1]-1
    StackCount = StackMat.shape[1]
    RecCount = RecMat.shape[1] 
    Geomy = [""]*(FeatCount+1)
    for n in range (FeatCount+1):
        Geomy[n] = f"{n+1} F{n}"
    Geom.columns = Geomy
    Stacky = [""]*StackCount
    for n in range (StackCount):
        Stacky[n] = f"S{n+1}"
    StackMat.columns = Stacky
    Recky = [""]*RecCount
    for n in range (RecCount):
        Recky[n] = f"R{n+1}"
    RecMat.columns = Recky
    print(f"Weather Conditions\n{Conditions}\
        \nGeometry of Building and Features\n{Geom}\
        \nStack Features\n{StackMat}\
        \nReceptor Positions\n{RecMat}\n")
    print(f"\nFeature Count is {FeatCount}\
          \nReceptor Count is {RecCount}\
          \nStack Count is {StackCount}\n")
    return FeatCount, StackCount, RecCount

def recirc(StackCount, FeatCount):
    RecircDataFramex = ["Bs","Bl","R","Hc","Xc","Lc","upxr","upzr","dpxr","dpzr"]
    StackRecircDataFrame = [""]*StackCount*2
    for n in range(StackCount):
        StackRecircDataFrame[2*n] = f"U S{n+1}"
        StackRecircDataFrame[2*n+1] = f"D S{n+1}"
    RecircDataFrameDatay = [""]*(FeatCount+1)
    for n in range (FeatCount+1):
        RecircDataFrameDatay[n] = f"{n+1} F{n}"
    RecircDataFrameDatax = np.concatenate((RecircDataFramex,StackRecircDataFrame))
    Recirc = pd.DataFrame(np.zeros((len(RecircDataFrameDatax),FeatCount+1)),index = RecircDataFrameDatax)
    Recirc.columns = RecircDataFrameDatay
    return Recirc

def cond():
    CondDataFrameDatax = ["A z0","B z0","A a","B a","A del","B del","UhUstar","Uh","n"]
    CondDataFrameDatay = ["L z0","Avg z0", "H z0"]
    Cond = pd.DataFrame(np.zeros((len(CondDataFrameDatax),len(CondDataFrameDatay))),index = CondDataFrameDatax)
    Cond.columns = CondDataFrameDatay
    return Cond

def stack(RecCount, StackCount):
    StackDataFrameDatax = ["hsr","Uh","UhUstar","VeUh","Bj","Fm","hd","hf","sig0","ix","iy","iz","sigy","sigz"]
    ReceptorDataFrameDatax = [""]*RecCount*7
    StackDataFrameDatay = [""]*(StackCount)
    for n in range (StackCount):
        StackDataFrameDatay[n] = f"S{n+1}"
    for n in range (RecCount):
        ReceptorDataFrameDatax[7*n] = f"R{n+1} x"
        ReceptorDataFrameDatax[(7*n)+1] = f"R{n+1} hx"
        ReceptorDataFrameDatax[(7*n)+2] = f"R{n+1} hr"
        ReceptorDataFrameDatax[(7*n)+3] = f"R{n+1} hs"
        ReceptorDataFrameDatax[(7*n)+4] = f"R{n+1} h plume"
        ReceptorDataFrameDatax[(7*n)+5] = f"R{n+1} zeta"
        ReceptorDataFrameDatax[(7*n)+6] = f"R{n+1} Dr"
    DataFrameX = np.concatenate((StackDataFrameDatax,ReceptorDataFrameDatax,["Min Dr"]))
    Stack = pd.DataFrame(np.zeros((len(DataFrameX),StackCount)),index = DataFrameX)
    Stack.columns = StackDataFrameDatay
#    minDrdf =[""]*RecCount
    return Stack,Stack,Stack

def htop(Recirc, RecMat, Geom, FeatCount):
    htopframe = pd.concat((Recirc.loc["upzr"],Recirc.loc["dpzr"],RecMat.loc["zp"],\
                            Geom.loc["zp","1 F0":f"{FeatCount+1} F{FeatCount}"]+Geom.loc["H","1 F0":f"{FeatCount+1} F{FeatCount}"]))
    return htopframe

