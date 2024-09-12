import dearpygui.dearpygui as dpg
import pandas as pd
import numpy as np

#Conditions, Geom, StackMat, RecMat
def s():
    dpg.create_context()

def f():
    dpg.create_viewport(title='Base', width=1000, height=1000)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Base", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

def readme():
    width, height, channels, first_image = dpg.load_image("stackdiagram.png") # Load first image, using "data_A" as the tag so you can individually load the texture. 
    with dpg.texture_registry():
        dpg.add_static_texture(width, height, first_image, tag="texture_A")
    dpg.add_text("\nThis calculates the minimum possible stack height using the geometric method. This assumes:\n\n"
        "The wind is approaching perpendicular to the building, from one wind direction, in a 2D frame.\n"
        "All obstacles on the rooftop are rectangular in form.\n"
        "Any intakes on the up or downwind walls are hidden.\n"
        "An intake exists in every recirculation zone (All recirc zones are accounted for).\n"
        "All features (stacks, obstacles, intakes) are centered on building in depth. \n"
        "All units are compatible. \n")
    with dpg.drawlist(width=800, height=524):
            dpg.draw_image("texture_A", (0, 0),(800, 524))

def tabi(Matr,fp):
    matr = Matr.head(Matr.shape[0]).index.values
    matc = Matr.columns.values
    print(f"{fp}")
    for n in range(len(fp)):
        if fp[n] == "\\":
            title = f"{fp[n+1:len(fp)]}"
        else:
            zero = 0
    with dpg.tab(label=f"{title}"):
        with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                    borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):
            
            dpg.add_table_column(label="")
            for n in range(Matr.shape[1]):
                dpg.add_table_column(label=f"{matc[n]}")
            for i in range(Matr.shape[0]):
                with dpg.table_row():
                    dpg.add_text(f"{matr[i]}")
                    for j in range(Matr.shape[1]):
                        dpg.add_text(f"{Matr.iat[i,j]}")

def inputs(Ma,fa,Mb,fb,Mc,fc,Md,fd):
    with dpg.tab_bar(tag="inptab") as tb:            
            tabi(Ma,fa)
            tabi(Mb,fb)
            tabi(Mc,fc)
            tabi(Md,fd)

def tabo(Matr,name):
    matr = Matr.head(Matr.shape[0]).index.values
    matc = Matr.columns.values
    title = f"{name}"
    with dpg.tab(label=f"{title}"):
        with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                    borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):
            dpg.add_table_column(label="")
            for n in range(Matr.shape[1]):
                dpg.add_table_column(label=f"{matc[n]}")
            for i in range(Matr.shape[0]):
                with dpg.table_row():
                    dpg.add_text(f"{matr[i]}")
                    for j in range(Matr.shape[1]):
                        dpg.add_text(f"{Matr.iat[i,j]}")

def outputs(R,C,A,L,H):
    with dpg.tab_bar(tag="outtab") as tb:            
            tabo(R,"Recirc")
            tabo(C,"Cond")
            tabo(A,"Avg")
            tabo(L,"Low")
            tabo(H,"High")

def twoD(Geom,Stack,Rec,Recirc,AvgStack):
    w = int(Geom.iloc[3,:].max()*20)
    h = int(Geom.iloc[5,:].max()*50)
    ho = h-50
    print(f"\n\nh\n\n{h}\n")
    print(f"\n\nw\n\n{w}\n")
    xgw = np.zeros(Geom.shape[1])
    hgn = np.zeros(Geom.shape[1])
    xge = np.zeros(Geom.shape[1])
    hgs = np.zeros(Geom.shape[1])
    xrc = np.zeros(Geom.shape[1])
    hrc = np.zeros(Geom.shape[1])
    xre = np.zeros(Geom.shape[1])
    hre = np.zeros(Geom.shape[1])
    xrl = np.zeros(Geom.shape[1])
    with dpg.drawlist(width=w, height=h):
        for n in range(Geom.shape[1]):
            xgw[n] = Geom.iat[0,n]*10
            hgn[n] = ho-(Geom.iat[2,n]+Geom.iat[5,n])*10
            xge[n] = (Geom.iat[0,n]+Geom.iat[3,n])*10
            hgs[n] = ho-Geom.iat[2,n]*10
            xrc[n] = (Geom.iat[0,n]+Recirc.iat[4,n])*10
            hrc[n] = ho-(Geom.iat[2,n]+Geom.iat[5,n]+Recirc.iat[3,n])*10
            xre[n] = (Geom.iat[0,n]+Recirc.iat[5,n])*10
            hre[n] = ho-(Geom.iat[2,n]+Geom.iat[5,n])*10
            xrl[n] = (Geom.iat[0,n]+Geom.iat[3,n]+Recirc.iat[2,n])*10
            with dpg.draw_layer(label="Buildings"):
                    dpg.draw_rectangle((xgw[n],hgn[n]),(xge[n],hgs[n]),color=(0, 255, 0, 255))
                    print((xgw[n],hgn[n]),(xge[n],hgs[n]))
            with dpg.draw_layer(label="Recirc"):
                 dpg.draw_line((xgw[n],hgn[n]),(xrc[n],hrc[n],),color=(255, 0, 255, 150))
                 dpg.draw_line((xrc[n],hrc[n],),(xre[n],hre[n]),color=(255, 0, 255, 150))
                 dpg.draw_line((xge[n],hgn[n]),(xrl[n],hgn[n]),color=(255, 0, 255, 150))
                 dpg.draw_line((xrl[n],hgn[n]),(xrl[n],hgs[n]),color=(255, 0, 255, 150))
        for n in range(Stack.shape[1]):
            shbot = ho-(Stack.iat[5,n]*10)
            shtop = ho-(AvgStack.iat[0,n]*10)
            with dpg.draw_layer(label="Stacks"):
                 dpg.draw_line(((Stack.iat[3,n]*10),shbot),((Stack.iat[3,n]*10),shtop),color=(255*n, 255, 255, 150))
                 dpg.draw_triangle((Stack.iat[3,n]*10,shtop),\
                                   (Stack.iat[3,n]*100,ho-(shtop+(0.2*Stack.iat[3,n]*100))),\
                                    (Stack.iat[3,n]*100,ho-(shtop+(-0.2*Stack.iat[3,n]*100))),\
                                        color=(255,255,255,255))
                 print(f"\n\nStack{n+1}\n{(Stack.iat[3,n]*10)},{ho-(Stack.iat[5,n]*10)}\n{(Stack.iat[3,n]*10)},{ho-(AvgStack.iat[0,n]*10)}")
                 print(f"\n{(Stack.iat[3,n]*10)},{(Stack.iat[5,n]*10)}\n{(Stack.iat[3,n]*10)},{(AvgStack.iat[0,n]*10)}\nho\n{ho}")
        for n in range(Rec.shape[1]):
             with dpg.draw_layer(label="Receptors"):
                  dpg.draw_circle((Rec.iat[0,n]*10,ho-Rec.iat[2,n]*10),10)
def mixitup(Cond,CondPath,Geom,GeomPath,Stack,StackPath,Rec,RecPath,Recirc,AvgStack,LStack,HStack):
    s()
    with dpg.window(tag="Base",autosize=True):
        with dpg.collapsing_header(label = "Read Me"):
            readme()
        with dpg.collapsing_header(label="Inputs"):
             inputs(Cond,CondPath,Geom,GeomPath,Stack,StackPath,Rec,RecPath)
        with dpg.collapsing_header(label="Outputs"):
             outputs(Recirc,Cond,AvgStack,LStack,HStack)
        with dpg.collapsing_header(label="2D Render"):
             twoD(Geom,Stack,Rec,Recirc,AvgStack)
    f()