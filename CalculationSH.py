import numpy as np

def recirc(Recirc, Geom, StackMat, StackCount, FeatCount):
    Recirc.loc["Bs"] = Geom.loc["B":"H"].min()
    Recirc.loc["Bl"] = Geom.loc["B":"H"].max()
    Recirc.loc["R"] = (Recirc.loc["Bs"]**.67)*(Recirc.loc["Bl"]**.33)
    Recirc.loc["Hc"] = Recirc.loc["R"]*.22
    Recirc.loc["Xc"] = Recirc.loc["R"]*.5
    Recirc.loc["Lc"] = Recirc.loc["R"]*.9
    Recirc.loc["upxr"] = Geom.loc["xp"]+Recirc.loc["Xc"]
    Recirc.loc["upzr"] = Geom.loc["zp"]+Geom.loc["H"]+Recirc.loc["Hc"]
    Recirc.loc["dpxr"] = Geom.loc["xp"]+Geom.loc["L"]+Recirc.loc["R"]
    Recirc.loc["dpzr"] = Geom.loc["zp"]+Geom.loc["H"]
    for n in range(StackCount):
        for m in range(FeatCount+1):
            Recirc.at[f"D S{n+1}",f"{m+1} F{m}"] = Recirc.at["dpzr",f"{m+1} F{m}"] + ((Recirc.at["dpxr",f"{m+1} F{m}"]-StackMat.at["xp",f"S{n+1}"])*.2)
            Recirc.at[f"U S{n+1}",f"{m+1} F{m}"] = Recirc.at["upzr",f"{m+1} F{m}"] + ((Recirc.at["upxr",f"{m+1} F{m}"]-StackMat.at["xp",f"S{n+1}"])*.2)
    Recirc.loc["PeakRecircU"] = Recirc.loc["upzr"]-(Recirc.loc["upxr"]/5)
    Recirc.loc["PeakRecircD"] = Recirc.loc["dpzr"]-(Recirc.loc["dpxr"]/5)
    print(f"Recirc\n{Recirc}\n")
    return Recirc

def cond(Cond, Conditions, Geom):
    Cond.loc["A z0"] = [Conditions.at['A','z0']*.5,Conditions.at['A','z0'],Conditions.at['A','z0']*1.5]
    Cond.loc["B z0"] = [Conditions.at['B','z0']*.5,Conditions.at['B','z0'],Conditions.at['B','z0']*1.5]
        # DEL IS BOUNDARY LAYER THICKNESS
        # a could be albedo? pending
        # The low and high roughness cases are just guesses, they are likely greatly incorrect and will require attention
    Cond.loc["A a"] = [Conditions.at["A","a"]*.5,Conditions.at["A","a"],Conditions.at["A","a"]*1.5]
    Cond.loc["A del"] = [Conditions.at["A","del"]*.5,Conditions.at["A","del"],Conditions.at["A","del"]*1.5]
    Cond.loc["B a"] = [Conditions.at["B","a"]*.5,Conditions.at["B","a"],Conditions.at["B","a"]*1.5]
    Cond.loc["B del"] = [Conditions.at["B","del"]*.5,Conditions.at["B","del"],Conditions.at["B","del"]*1.5]
    U1P = Conditions.iat[1,0]*2.5
    Cond.loc["UhUstar"] = np.log((Geom.at['H','1 F0']/Cond.loc['B z0']))
    Cond.loc["Uh"] = [U1P*pow(Cond.at["A del","L z0"]/Conditions.at["A","H"],Cond.at["A a","L z0"])*pow(Conditions.at["B","H"]/Cond.at["B del","L z0"],Cond.at["B a","L z0"]),\
                        U1P*pow(Cond.at["A del","Avg z0"]/Conditions.at["A","H"],Cond.at["A a","Avg z0"])*pow(Conditions.at["B","H"]/Cond.at["B del","Avg z0"],Cond.at["B a","Avg z0"]),\
                        U1P*pow(Cond.at["A del","H z0"]/Conditions.at["A","H"],Cond.at["A a","H z0"])*pow(Conditions.at["B","H"]/Cond.at["B del","H z0"],Cond.at["B a","H z0"]),]
    Cond.loc["n"] = [0.24+(0.096*np.log10(Cond.at["B z0","L z0"]))+(0.016*pow(np.log10(Cond.at["B z0","L z0"]),2)),\
                    0.24+(0.096*np.log10(Cond.at["B z0","Avg z0"]))+(0.016*pow(np.log10(Cond.at["B z0","Avg z0"]),2)),\
                        0.24+(0.096*np.log10(Cond.at["B z0","H z0"]))+(0.016*pow(np.log10(Cond.at["B z0","H z0"]),2))]
    print(f"\nCond\n{Cond}")
    return Cond

def htop(htopframe):
    htop = htopframe.max()
    print(f"htop\n{htop}")
    return htop

def distance(Rnum, Snum, StackMat, Stack, RecMat, answer):
    if answer < 0:
        z = StackMat.at["zp",f"S{Snum}"]
    elif answer > 2:
        z = Stack.at["hsr",f"S{Snum}"]
    else:
        z = input(f"Enter stackheight for S{Snum+1}")
    return pow(pow(StackMat.at["xp",f"S{Snum}"]-RecMat.at["xp",f"R{Rnum}"],2)+\
    pow(StackMat.at["yp",f"S{Snum}"]-RecMat.at["yp",f"R{Rnum}"],2)+\
    pow(z-RecMat.at["zp",f"R{Rnum}"],2),0.5)

def stack(Stack, Cond, Recirc, StackMat, RecMat, htop, StackCount, RecCount, answer):
    Stack.loc["Uh"] = Cond.at["Uh"]
    Stack.loc["UhUstar"] = Cond.at["UhUstar"]
    Stack.loc["VeUh"] = StackMat.loc["Ve"]/Stack.loc["Uh"]
    Stack.loc["Bj"] = (1/3)+(1/Stack.loc["VeUh"])
    Stack.loc["Fm"] = StackMat.loc["Ve"].pow(2)*StackMat.loc["de"].pow(2)/4
    Stack.loc["hf"] = 0.9*Stack.loc["Fm"].pow(1/2)*Stack.loc["UhUstar"].pow(1/2)/(Stack.loc["Uh"]*Stack.loc["Bj"])
    Stack.loc["sig0"] = StackMat.loc["de"]*.35
    Stack.loc["ix"] = Cond.at["n"]*np.log(30/Cond.at["B z0"])/np.log(StackMat.loc["zp"]/Cond.at["B z0"])
    Stack.loc["iy"] = Stack.loc["ix"]*.75
    Stack.loc["iz"] = Stack.loc["ix"]*.5
    Stack.loc["sigy"] = ((Stack.loc["iy"]*StackMat.loc["xp"]).pow(2)+Stack.loc["sig0"].pow(2)).pow(.5)
    Stack.loc["sigz"] = ((Stack.loc["iz"]*StackMat.loc["xp"]).pow(2)+Stack.loc["sig0"].pow(2)).pow(.5)
    for n in range(StackCount):
        Stack.at["hsr",f"S{n+1}"] = max(Recirc.loc[f"U S{n+1}"].to_numpy().max(),Recirc.loc[f"D S{n+1}"].to_numpy().max())
        if Stack.at["VeUh",f"S{n+1}"] <= 3:
            Stack.at["hd",f"S{n+1}"] = StackMat.at["de",f"S{n+1}"]*(3.0-(Stack.at["Bj",f"S{n+1}"]*Stack.at["VeUh",f"S{n+1}"]))
        else:
            Stack.at["hd",f"S{n+1}"] = 0
    for m in range(RecCount):
        for n in range(StackCount):
            Stack.at[f"R{m+1} x",f"S{n+1}"] = distance(m+1,n+1, StackMat, Stack, RecMat, answer)
            print(Stack.loc[f"R{m+1} x",f"S{n+1}"])
        Stack.loc[f"R{m+1} hx"] = (3*Stack.loc["Fm"]*Stack.loc[f"R{m+1} x"]/((Stack.loc["Bj"]*Stack.loc["Uh"]).pow(2))).pow(1/3)
        for n in range (StackCount):
            if Stack.at[f"R{m+1} hx",f"S{n+1}"] < Stack.at[f"hf",f"S{n+1}"]:
                Stack.at[f"R{m+1} hr",f"S{n+1}"] = Stack.at[f"R{m+1} hx",f"S{n+1}"]*StackMat.at[f"SCF",f"S{n+1}"]
            else:
                Stack.at[f"R{m+1} hr",f"S{n+1}"] = Stack.at[f"hf",f"S{n+1}"]*StackMat.at[f"SCF",f"S{n+1}"]
        Stack.loc[f"R{m+1} hs"] = Stack.loc[f"hsr"]-Stack.loc[f"R{m+1} hr"]+Stack.loc["hd"]
        Stack.loc[f"R{m+1} h plume"] = Stack.loc[f"R{m+1} hs"]+Stack.loc[f"R{m+1} hr"]-Stack.loc["hd"]
        for n in range(StackCount):
            if (Stack.at[f"R{m+1} h plume",f"S{n+1}"]-htop) < 0:
                Stack.at[f"R{m+1} zeta",f"S{n+1}"] = 0
                Stack.at[f"R{m+1} Dr",f"S{n+1}"] = 4*Cond.at["Uh"]*Stack.at["sigy",f"S{n+1}"]*Stack.at["sigz",f"S{n+1}"] \
                                                        /(StackMat.at["Ve",f"S{n+1}"]*pow(StackMat.at["de",f"S{n+1}"],2))
            else:
                Stack.at[f"R{m+1} zeta",f"S{n+1}"] = Stack.at[f"R{m+1} h plume",f"S{n+1}"]-htop
                Stack.at[f"R{m+1} Dr",f"S{n+1}"] = (4*Cond.at["Uh"]*Stack.at["sigy",f"S{n+1}"]*Stack.at["sigz",f"S{n+1}"]*\
                                    np.exp(pow((Stack.at[f"R{m+1} zeta",f"S{n+1}"]/Stack.at["sigz",f"S{n+1}"]),2)/2))\
                                        /(StackMat.at["Ve",f"S{n+1}"]*pow(StackMat.at["de",f"S{n+1}"],2))

    print(f"Stack\n{Stack}")
    return Stack

