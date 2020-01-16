# --------------------------------------------------------------------
# Program: Pixel Art Assignment - OOP Implementation 
# Author: Yi Wei Zhou
# Date: 26/11/2018
# Description: Introduction menu/page to program. Allows readers to load
# possible files or input the parameters for a new file. 
# --------------------------------------------------------------------

import pygame
pygame.init()
screen = pygame.display.set_mode((1422,800))

loading = pygame.image.load('Loading0.png')
loading = pygame.transform.scale(loading,(300,37))
screen.blit(loading,(300,300))
pygame.display.update()

from ClassesV2 import InputBox,Button,Menu,readfile,stagecentre, Group

swidth,sheight = screen.get_size()



#variable definitions, the creation of buttons, images and text           
black,white= (0,0,0),(255,255,255)
bgreen = (37,108,140)
titletxt = pygame.image.load('pixelart.png')
titletxt = pygame.transform.scale(titletxt,(650,319))
starttxt = pygame.image.load('starttxt.png')
startbtn = Button(250,55,bgreen,starttxt,(600,480))
startbtn.pos = (stagecentre('btn',startbtn,screen),startbtn.pos[1])
optionsbrd = pygame.image.load('txtbox.png')
optionsbrd = pygame.transform.scale(optionsbrd,(300,250))
rowstxt = pygame.image.load('rowstxt.png')
rowstxt = pygame.transform.scale(rowstxt,(61,13))
coltxt = pygame.image.load('columnstxt.png')
coltxt = pygame.transform.scale(coltxt,(90,13))
ortxt = pygame.image.load('ortxt.png')
ortxt = pygame.transform.scale(ortxt,(300,19))
sizetxt = pygame.image.load('sizetxt.png')
sizetxt = pygame.transform.scale(sizetxt,(112,13))
submittxt = pygame.image.load('submittxt.png')
submitbtn = Button(150,35,bgreen,submittxt,(680,575))
loadtxt = pygame.image.load('loadtxt.png')
loadbtn = Button(150,35,bgreen,loadtxt,(640,550))
backtxt = pygame.image.load('backtxt.png')
backbtn = Button(150,35,bgreen,backtxt,(640,730))
arrowrimg = pygame.image.load('arrowr.png')
arrowlimg = pygame.image.load('arrowl.png')
xbtn = pygame.image.load('clearicon.png')
rightbtn = Button(50,50,None, arrowrimg, (820,720))
leftbtn = Button(50,50,None, arrowlimg, (560,720))
color = [black,bgreen]
rowinptbx = InputBox(280, 460, 100, 32,color)
colinptbx = InputBox(410, 460, 100, 32,color)
sizeinptbx = InputBox(410, 530, 100, 32,color)

#boolean definition for modes
done,options,loadstate,isload,goto = False,False,False,False,False

font = pygame.font.Font(None, 16)
play= 125
bggif = []

#If screen taking too long to load uncomment below and comment the for loop below
#temp = pygame.image.load('titlebg_0000_Layer-128.png')
#bggif = [pygame.transform.scale(temp,(1422,800))]

for x in range(128):#load images for the splash screen at the beginning
    temp = pygame.image.load('titlebg_'+"%04d"%(x)+'_Layer-'+str(128-x)+'.png')
    bggif.append(pygame.transform.scale(temp,(1422,800)))
guidedisplay = font.render(" ",True, white)

#creating groups
optsgroup = Group((stagecentre('img',optionsbrd,screen),460),
                  [['img',optionsbrd,0,0],['img',ortxt,0,105],['img',rowstxt,50,40],
                   ['img',coltxt,170,40],['inpt',rowinptbx,30,60],['inpt',colinptbx,160,60],
                   ['inpt',sizeinptbx,160,130],['btn',submitbtn, 80,170],['img',sizetxt,30,140],
                   ['img',guidedisplay,30,5] ])
#greating menus
loadmenu = Menu(3,2,swidth-50,sheight-50,[250,300],(150,300),[bgreen]*6,None,200,50,30)
deletemenu = Menu(3,2,swidth-50,sheight-50,[400,300],(330,300),[bgreen]*6,[xbtn]*6,50,50)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN: #when button is pressed
            mousepos = pygame.mouse.get_pos()
            if loadstate: #if user already pressed load
                fileclicked = loadmenu.cellclicked(mousepos)
                deleteclicked = deletemenu.cellclicked(mousepos)
                #the file the user clicked will then be loaded into MainFile
                #to run the program
                if fileclicked != None:
                    if len(namelst)>6*pgnum +fileclicked[0]*loadmenu.rows + fileclicked[1]:
                        goto,loadstate,isload = True,False,True
                        info = [namelst[6*pgnum + fileclicked[0]*loadmenu.rows + fileclicked[1]]]
                elif deleteclicked != None:
                    #delete files if clicked
                    if 6*pgnum + deleteclicked[0]*loadmenu.rows + deleteclicked[1] < len(namelst):
                        del namelst[6*pgnum + deleteclicked[0]*loadmenu.rows + deleteclicked[1]]
                        f = open('filenames.txt','w')
                        for name in namelst:
                            f.write(name +'\n')
                        f.close()
                        namelst = readfile()
                        namelst_notxt = [x[:-4] for x in namelst]
                        loadmenu = Menu(3,2,swidth-50,sheight-50,[250,300],(150,300),[bgreen]*6,['text']+namelst_notxt[:6],200,50,30)
                        
        if event.type == pygame.QUIT:
                done = True
        if loadstate:
            #if user pressed load, test if they pressed any other buttons
            #eg. back, turn page right and turn page left,
            namelst_notxt = [x[:-4] for x in namelst]
            if backbtn.handle_event(event): loadstate = False
            #if right or left is pressed turn page number which will load different
            #files into the menu class
            elif rightbtn.handle_event(event):
                if len(namelst) > (pgnum +1) *6:
                    pgnum +=1
                    loadmenu = Menu(3,2,swidth-50,sheight-50,[250,300],(150,300),[bgreen]*6,['text']+namelst_notxt[pgnum*6:pgnum*6+6],200,50,30)
            elif leftbtn.handle_event(event):
                if pgnum > 0:
                    pgnum -= 1
                    loadmenu = Menu(3,2,swidth-50,sheight-50,[250,300],(150,300),[bgreen]*6,['text']+namelst_notxt[pgnum*6:pgnum*6+6],200,50,30)
        else:
            #During the start page if user presses start or load go to those pages
            if startbtn.handle_event(event): options = True
            elif loadbtn.handle_event(event) and not options:
                namelst = readfile()
                namelst_notxt = [x[:-4] for x in namelst]
                pgnum = 0
                loadmenu = Menu(3,2,swidth-50,sheight-50,[250,300],(150,300),[bgreen]*6,['text']+namelst_notxt[:6],200,50,30)
                loadstate = True 
        if options:
            #if in options, handle events to allow input of cell size or
            # of cells in columns and rows. 
            rowinptbx.handle_event(event,True,3)
            colinptbx.handle_event(event,True,3)
            sizeinptbx.handle_event(event,True,3)
            if submitbtn.handle_event(event):
                try:
                    if 5<=int(sizeinptbx.text)<=400:
                        goto,info,isload = True,[int(sizeinptbx.text)],False
                    else:
                        print('rows')
                        guidedisplay = font.render("Cell size must be between 5 and 400",True, white)
                except ValueError:
                    try :
                        if 1<= int(rowinptbx.text)<=350 and 1<= int(colinptbx.text)<=350:
                            goto, info,isload = True,[int(rowinptbx.text),int(colinptbx.text)],False
                        else:
                            print('rows')
                            guidedisplay = font.render("Rows and columns must be between 1 and 350",True, white)
                    except ValueError:guidedisplay = font.render("Please fill required boxes",True, white)

    screen.blit(bggif[play],(0,0)) #display the splash screen
    #screen.blit(bggif[0],(0,0))
    if loadstate:
        #during loading display a preview of each picture and the names which
        # can be clicked to enter and edit
        options = False
        loadmenu.draw(screen)
        deletemenu.draw(screen)
        backbtn.draw(screen)
        cords=[(50,50),(500,50),(950,50), (50,370),(500,370),(900,370)]
        rightbtn.draw(screen)
        leftbtn.draw(screen)
        for ind,name in enumerate(namelst[pgnum*6:pgnum*6+6]):
            tempfile = open(name,'r')
            r,c,w,h = map(int,tempfile.readline().strip().split())
            tempwidth = min(400//r,280//c)
            for row in range(r):
                for col in range(c):
                    pygame.draw.rect(screen,eval(tempfile.readline().strip()),(cords[ind][0]+row*tempwidth,cords[ind][1]+col*tempwidth, tempwidth,tempwidth))
            
    elif goto:
        #load the main file using information from options page or load page
        screen.fill(black)
        screen.blit(loading,(300,300))
        pygame.display.update()
        from MainFileV2 import *
        filenameinpt.text = ''
        mainlevel(info,isload)
        namelst = readfile()
        goto,options,loadstate = False,False,False
    elif options:
        #if on options page, draw all the objects
        optsgroup.draw(screen)
        #guided display is not blitting!!!!
        rowinptbx.draw(screen)
        colinptbx.draw(screen)
        sizeinptbx.draw(screen)
        if rowinptbx.active or colinptbx.active:
            sizeinptbx.text = ''
            sizeinptbx.txt_surface = sizeinptbx.font.render('', True, sizeinptbx.color)
        elif sizeinptbx.active:
            rowinptbx.text,colinptbx.text = '',''
            rowinptbx.txt_surface = rowinptbx.font.render('', True, rowinptbx.color)
            colinptbx.txt_surface = colinptbx.font.render('', True, colinptbx.color)
        submitbtn.draw(screen)
    else:
        #drawing buttons in the opening page
        startbtn.draw(screen)
        loadbtn.draw(screen)    
        screen.blit(titletxt,(stagecentre('img',titletxt,screen),120))
    #change the pictures for animation
    if play <= 0: play = 125
    else:play -= 1
    pygame.display.update()
    pygame.time.Clock().tick(20)
