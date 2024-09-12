import matplotlib.pyplot as plt
import vpython as vp
from vpython import *
def twoD(Stack, Recirc, Geom, StackMat, RecMat, FeatCount, StackCount, RecCount):
# %% Plotting Assembly
    xplot = [Geom.loc["xp","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy(),Geom.loc["xp","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy(),\
            Geom.loc["xp","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy()+Geom.loc["L","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy(),\
                Geom.loc["xp","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy()+Geom.loc["L","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy()]
    zplot = [Geom.loc["zp","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy(),\
            Geom.loc["H","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy()+Geom.loc["zp","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy(),\
                Geom.loc["H","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy()+Geom.loc["zp","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy(),\
                    Geom.loc["zp","1 F0":f"{FeatCount+1} F{FeatCount}"].to_numpy()]
    xstack = [StackMat.loc["xp","S1":f"S{StackCount}"].to_numpy(),StackMat.loc["xp","S1":f"S{StackCount}"].to_numpy()]
    for n in range(RecCount):
    #    zstack = [StackMat.loc["zp","S1":f"S{StackCount}"].to_numpy(),StackMat.loc["zp","S1":f"S{StackCount}"].to_numpy()+Stack.loc[f"R{n+1} hs","S1":f"S{StackCount}"].to_numpy()]
        zstack = [StackMat.loc["zp","S1":f"S{StackCount}"].to_numpy(),Stack.loc[f"hsr","S1":f"S{StackCount}"].to_numpy()]
    # hsr is accurate in a v technical sense. It is 1/5 slope away from the peak of the recirc zones, but it doesn't account for geom
    xrecircplot = [Geom.loc["xp","1 F0":f"{n+1} F{n}"].to_numpy(),\
                Geom.loc["xp","1 F0":f"{n+1} F{n}"].to_numpy()+Recirc.loc["Xc","1 F0":f"{n+1} F{n}"].to_numpy(),\
                Geom.loc["xp","1 F0":f"{n+1} F{n}"].to_numpy()+Recirc.loc["Lc","1 F0":f"{n+1} F{n}"].to_numpy(),\
                Geom.loc["xp","1 F0":f"{n+1} F{n}"].to_numpy()+Geom.loc["L","1 F0":f"{n+1} F{n}"].to_numpy(),\
                Geom.loc["xp","1 F0":f"{n+1} F{n}"].to_numpy()+Geom.loc["L","1 F0":f"{n+1} F{n}"].to_numpy()+Recirc.loc["R","1 F0":f"{n+1} F{n}"].to_numpy(),\
                Geom.loc["xp","1 F0":f"{n+1} F{n}"].to_numpy()+Geom.loc["L","1 F0":f"{n+1} F{n}"].to_numpy()+Recirc.loc["R","1 F0":f"{n+1} F{n}"].to_numpy()]
    zrecircplot = [Geom.loc["zp","1 F0":f"{n+1} F{n}"].to_numpy()+Geom.loc["H","1 F0":f"{n+1} F{n}"].to_numpy(),\
                Geom.loc["zp","1 F0":f"{n+1} F{n}"].to_numpy()+Geom.loc["H","1 F0":f"{n+1} F{n}"].to_numpy()+Recirc.loc["Hc","1 F0":f"{n+1} F{n}"].to_numpy(),\
                Geom.loc["zp","1 F0":f"{n+1} F{n}"].to_numpy()+Geom.loc["H","1 F0":f"{n+1} F{n}"].to_numpy(),\
                Geom.loc["zp","1 F0":f"{n+1} F{n}"].to_numpy()+Geom.loc["H","1 F0":f"{n+1} F{n}"].to_numpy(),\
                Geom.loc["zp","1 F0":f"{n+1} F{n}"].to_numpy()+Geom.loc["H","1 F0":f"{n+1} F{n}"].to_numpy(),\
                Geom.loc["zp","1 F0":f"{n+1} F{n}"].to_numpy()]

    # %% 2D Plotting Executed
    print(f"recirc\n{xrecircplot}\n{zrecircplot}\n")
    print(f"feat\n{xplot}\n{zplot}\n")
    print(f'receptors\n{RecMat.loc["xp","R1":f"R{RecCount}"].to_numpy()}\n{RecMat.loc["zp","R1":f"R{RecCount}"].to_numpy()}\n')
    print(f"stacks\n{xstack}\n{zstack}\n")
    plt.title('Building Model')
    plt.xlabel('Length')
    plt.ylabel('Height')
    plt.plot(xrecircplot, zrecircplot, label = 'Feature Recirculation Zones',linewidth = 2)
    plt.plot(xplot, zplot, label = 'Features',linewidth = 3)
    plt.plot(xstack, zstack, label = 'Stacks',linewidth = 3)
    plt.scatter(RecMat.loc["xp","R1":f"R{RecCount}"].to_numpy(),RecMat.loc["zp","R1":f"R{RecCount}"].to_numpy(), label = 'Receptors')
    plt.legend(loc=3, prop={'size': 5.5})
    plt.grid()
    plt.show()

def threeD(Stack, Geom, StackMat, FeatCount, StackCount):
    for n in range(FeatCount+1):
        feature = vp.box(pos=vector(Geom.at["xp",f"{n+1} F{n}"]+(Geom.at["L",f"{n+1} F{n}"]/2),Geom.at["zp",f"{n+1} F{n}"]+(Geom.at["H",f"{n+1} F{n}"]/2),0)\
            ,color=color.cyan,length=Geom.at["L",f"{n+1} F{n}"],height=Geom.at["H",f"{n+1} F{n}"],width=Geom.at["B",f"{n+1} F{n}"])
        frecirc = vp.box(pos=vector(Geom.at["xp",f"{n+1} F{n}"]+(Geom.at["L",f"{n+1} F{n}"]/2),Geom.at["zp",f"{n+1} F{n}"]+(Geom.at["H",f"{n+1} F{n}"]/2),0)\
            ,color=color.cyan,length=Geom.at["L",f"{n+1} F{n}"],height=Geom.at["H",f"{n+1} F{n}"],width=Geom.at["B",f"{n+1} F{n}"])
    for n in range(StackCount):
        stack = vp.cylinder(pos=vector(StackMat.at["xp",f"S{n+1}"],StackMat.at["zp",f"S{n+1}"]+(Stack.at[f"hsr",f"S{n+1}"]),0),up=vector(1,0,0)\
            ,color=color.red,radius=1,length=Stack.at[f"hsr",f"S{n+1}"])
    sleep(10)