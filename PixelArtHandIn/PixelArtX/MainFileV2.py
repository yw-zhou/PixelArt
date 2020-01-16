# --------------------------------------------------------------------
# Program: Pixel Art Assignment - OOP Implementation 
# Author: Yi Wei Zhou
# Date: 26/11/2018
# Description: Allows the user to draw using the pixel Art and some
# other functions. ***The undo button has not been created***
# --------------------------------------------------------------------


from ClassesV2 import *
screen = pygame.display.set_mode((1422,800))

#define variables, load images, create instances of class eg. input and buttons
black,gray,white,lightgray = (0,0,0),(100,100,100),(255,255,255),(210,210,210)
colouroptions = [gray,(0, 153, 0),(51, 102, 255),(153, 102, 255),(255, 204, 0),(255, 102, 0),(204, 0, 0),(255, 230, 204),(102, 51, 0),white,black,(0, 153, 0)]
#black,green,blue,purple,yellow, orange,red,peach,brown
fillicon = pygame.image.load('fillicon.png')
clearicon = pygame.image.load('clearicon.png')
painticon = pygame.image.load('paintbrush.png')
undoicon =pygame.image.load('undo.png')
saveicon =pygame.image.load('save.png')
eraseicon =pygame.image.load('eraser.png')
menuicon = pygame.image.load('menubtn.png')
cwheelicon = pygame.image.load('color.png')
colourpickertxt = pygame.image.load('colourpickertxt.png')
colourpickertxt = pygame.transform.scale(colourpickertxt,(400,32))
font = pygame.font.Font(None, 52)
rgbtext = [font.render('R',True,black),font.render('G',True,black),font.render('B',True,black)]
imagelist = [painticon,cwheelicon, saveicon,clearicon, undoicon, eraseicon, menuicon,fillicon]
rinptbx = InputBox(800, 300, 80, 50,[white,black],font)
ginptbx = InputBox(800, 400, 80, 50,[white,black],font)
binptbx = InputBox(800, 500, 80, 50,[white,black],font)
rgbinpt = [rinptbx,ginptbx,binptbx]
filenameinpt = InputBox(530, 380, 230, 50,[white,black],font)
savebtntxt = pygame.image.load('savebtntxt.png')

saveastxt = pygame.image.load('saveastxt.png')
saveastxt = pygame.transform.scale(saveastxt,(300,42))

savebtn = Button(133,30,None, savebtntxt, (500,500))
exitbtn = Button(35,35,None,clearicon,(500,500))
clock = pygame.time.Clock()
    

def mainlevel(info,load = False):
    #more instances of menus
    cmboard = Menu(2,6,150,430,[8,8],(8,8),colouroptions)
    optsboard = Menu(2,4,150,290,[8,8],(8,480),None,imagelist)
    cmboard.clchosen = black
    w,h = screen.get_size()
    w-= 180
    #if the user loaded an image, the saved file would open it and display the
    #placements of colour accordingly. Otherwise if its a new image it will
    #load all white with the number of cells given
    if load:
        colourlst = []
        fi = open(info[0], 'r')
        r,c,w,h = map(int,fi.readline().strip().split())
        for x in range(r*c):
            colourlst.append(eval(fi.readline().strip()))
        pixelart = PixelArt(r,c,w,h,(180,0),colourlst)
    elif len(info) == 1:
        pixelart = PixelArt(w//info[0],h//info[0],w-w%info[0],h-h%info[0],(180,0))
    elif len(info) == 2:
        cellsize = min(w//info[0],h//info[1])
        pixelart = PixelArt(info[0],info[1],info[0]*cellsize,info[1]*cellsize,(180,0))

    #mouse/drawing states
    pixelart.canfill = False
    mousedown,colourpick,erase,saveas = False,False,False,False
    side = None
    templist = [cmboard.cellclicked((45,520)),optsboard.cellclicked((45,520))]
    if load:
        filenameinpt.text = info[0][:-4]
        filenameinpt.txt_surface = filenameinpt.font.render(filenameinpt.text, True, white)

    while True:
        #drawing everything
        screen.fill(white)
        pixelart.draw(screen)
        pygame.draw.rect(screen,lightgray,(0,0,180,800))
        cmboard.draw(screen)
        optsboard.draw(screen)
        
        for event in pygame.event.get():
            mousepos = pygame.mouse.get_pos()
            if colourpick:
                #the page to test if RGB was clicked so users can input values
                #for each RGB value
                for c in rgbinpt:c.handle_event(event,True,3)
            if saveas:
                #if the user wanted to save, open the main file names and save if
                # the name does not already exist. Then create a new file or open
                # the existing one under the same name and save current colour order
                filenameinpt.handle_event(event,False, 10)
                if savebtn.handle_event(event):
                    filename,intxt = open('filenames.txt','a'),open('filenames.txt','r')
                    new,namelst = True,readfile()
                    print(filenameinpt.text + '.txt',namelst)
                    if filenameinpt.text + '.txt' not in namelst:
                        filename.write('\n'+filenameinpt.text + '.txt')
                    tempsavefile = open(filenameinpt.text + '.txt','w+')
                    filename.close()
                    intxt.close()
                    tempsavefile.write(str(pixelart.rows) +' '+ str(pixelart.col)+' ' + str(pixelart.swidth) +' '+ str(pixelart.sheight)+'\n')
                    for row in pixelart.pixels:
                        for pixel in row:
                            tempsavefile.write(str(pixel.colour)+'\n')
                    tempsavefile.close()
                    saveas = 'Maybe'
            if exitbtn.handle_event(event):
                #go out of the draw page back to the start
                colourpick = 'Maybe'
                saveas = 'Maybe'
                templist = [cmboard.cellclicked((45,520)),optsboard.cellclicked((45,520))]
            if event.type == pygame.MOUSEBUTTONDOWN:
                #only fills if paint bucket tool is still selected.
                if optsboard.buttons[1][3].lcolour == black: pixelart.canfill = True
                else:
                    pixelart.canfill = False
                    mousedown = True

                #tests for if user clicked the palette or the tools and which one they
                    #clicked
                templist = [cmboard.cellclicked(mousepos),optsboard.cellclicked(mousepos)]
                for i, temp in enumerate(templist):
                    if temp!= None:
                        if i == 0:
                            #if palette is clicked make the drawing colour that colour, but if
                            #colour pick windowis already open load that colour into the palette
                            if colourpick:
                                cmboard.buttons[temp[1]][temp[0]].colour = tempcolour
                                colouroptions[temp[0]*cmboard.rows + temp[1]] = tempcolour
                            if erase: holdcolour = colouroptions[temp[0]*cmboard.rows + temp[1]]
                            else:
                                cmboard.clchosen = colouroptions[temp[0]*cmboard.rows + temp[1]]
                                holdcolour = cmboard.clchosen

                        else:
                            #depending on which tool is selected, make the mouse that mode
                            erase = False
                            if temp[0]*optsboard.rows + temp[1]==3:
                                for row in pixelart.pixels:
                                    for cell in row:cell.colour = white
                                templist = [cmboard.cellclicked((45,520)),optsboard.cellclicked((45,520))]
                            elif temp[0]*optsboard.rows + temp[1]==7:
                                pixelart.canfill = True
                            elif temp[0]*optsboard.rows + temp[1] == 6:
                                return
                            elif temp[0]*optsboard.rows + temp[1] == 1:
                                colourpick = True
                                saveas = False
                            elif temp[0]*optsboard.rows + temp[1] == 5:
                                holdcolour= cmboard.clchosen
                                erase = True
                                cmboard.clchosen = white
                            elif temp[0]*optsboard.rows + temp[1] == 0:
                                cmboard.clchosen = holdcolour
                            elif temp[0]*optsboard.rows + temp[1] == 2:
                                colourpick = False
                                saveas = True
                                templist = [cmboard.cellclicked((45,520)),optsboard.cellclicked((45,520))]    
                if colourpick == False and saveas == False: pixelart.cellclicked(pygame.mouse.get_pos(),cmboard.clchosen)
            if event.type == pygame.MOUSEBUTTONUP:
                if colourpick == 'Maybe': colourpick = False
                if saveas == 'Maybe': saveas = False
                mousedown = False
            pressed = pygame.key.get_pressed()
            #allow the use of keyboard movements to paint
            if pressed[pygame.K_LEFT]:side = 'left'
            elif pressed[pygame.K_RIGHT]: side = 'right'
            elif pressed[pygame.K_UP]: side = 'up'
            elif pressed[pygame.K_DOWN]:side = 'down'
            else: side = None
        if side!= None:pixelart.keystrokes(side,cmboard.clchosen)
        if mousedown:
            #allows for drag
            mousepos = pygame.mouse.get_pos()
            same = False
            if not colourpick and not saveas: pixelart.cellclicked(mousepos,cmboard.clchosen)
            if optsboard.buttons[1][3].lcolour != black: pixelart.canfill = False
        if saveas and not colourpick:
            #during the save option open a new window and draw needed items
            
            saveasopts = pygame.draw.rect(screen,lightgray,((screen.get_size()[0] - 400)//2, 300, 400, 150))
            screen.blit(saveastxt,(saveasopts.x + 45, saveasopts.y + 20))
            exitbtn.draw(screen, (saveasopts.x+350,saveasopts.y+5))
            savebtn.draw(screen, (saveasopts.x + 260, saveasopts.y + 90))
            filenameinpt.draw(screen)
            
        if colourpick and not saveas:
            #if user pressed colourpick, open a new window and draw the input boxes
            #as well as the current colour inputed
            colouropts = pygame.draw.rect(screen,lightgray,((screen.get_size()[0] - 500)//2, 200, 500, 400))
            screen.blit(colourpickertxt,(colouropts.x+45, colouropts.y+20))
            exitbtn.draw(screen, (colouropts.x+450,colouropts.y+10))
            tempcolour = []
            for c in rgbinpt:
                c.draw(screen)
                if c.text == '':tempcolour.append(0)
                elif int(c.text)>255: tempcolour.append(255)
                else: tempcolour.append(int(c.text))
            pygame.draw.rect(screen,tempcolour,(colouropts.x+30, colouropts.y+100, 250,250))
            
            
            for i,x in enumerate(rgbtext):
                screen.blit(x,(760, 310+i*100))
        pygame.display.update()
        if side!= None:clock.tick(20)

#mainlevel([30])
        


