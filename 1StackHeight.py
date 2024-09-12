#%% Imports
import ImportSH as imp
import GUISH as g
import MatLatSH as ml
import CalculationSH as c
import PlottingSH as plot

#%% Import data
CondPath,GeomPath,StackPath,RecPath = imp.imp(1)

#%% Counts
Conditions, Geom, StackMat, RecMat = ml.asgn(CondPath, GeomPath, StackPath, RecPath)
FeatCount, StackCount, RecCount = ml.count(Conditions, Geom, StackMat, RecMat)

#%% Defining DataFrames
Recirc = ml.recirc(StackCount, FeatCount)
Cond = ml.cond()
AvgStack,HStack,LStack = ml.stack(RecCount, StackCount)
htopframe = ml.htop(Recirc, RecMat, Geom, FeatCount)

#%% Calculations
Recirc = c.recirc(Recirc, Geom, StackMat, StackCount, FeatCount)
Cond = c.cond(Cond, Conditions, Geom)
htop = c.htop(htopframe)
AvgStack = c.stack(AvgStack, Cond.loc[:,"Avg z0"], Recirc, StackMat, RecMat, htop, StackCount, RecCount, 5)
LStack = c.stack(AvgStack, Cond.loc[:,"L z0"], Recirc, StackMat, RecMat, htop, StackCount, RecCount, 5)
HStack = c.stack(AvgStack, Cond.loc[:,"H z0"], Recirc, StackMat, RecMat, htop, StackCount, RecCount, 5)

#%% Plotting
#plot.twoD(AvgStack, Recirc, Geom, StackMat, RecMat, FeatCount, StackCount, RecCount)
#plot.threeD(AvgStack, Geom, StackMat, FeatCount, StackCount)
g.mixitup(Conditions,CondPath,Geom,GeomPath,StackMat,StackPath,RecMat,RecPath,Recirc,AvgStack,LStack,HStack)

#minDrdf =[""]*RecCount
#Everything above is confirmed, below is functional and looks right, but could be wrong. If numbers are fishy, inspect again
# htop, idk about this one, looks right? maybe?
# If a > 2, will measure distance from top of stack measured by recirc, not base of stack
# If a < 0, will measure distance from base of stack
# If 0 < a < 2, will measur e distance from given stack height 
#minDrdf[n] = [AvgStack.loc[f"R{n+1} Dr"]]
# Plotting DataFrame
# Plotting Assembly
#    zstack = [StackMat.loc["zp","S1":f"S{StackCount}"].to_numpy(),StackMat.loc["zp","S1":f"S{StackCount}"].to_numpy()+AvgStack.loc[f"R{n+1} hs","S1":f"S{StackCount}"].to_numpy()]
# hsr is accurate in a v technical sense. It is 1/5 slope away from the peak of the recirc zones, but it doesn't account for geom