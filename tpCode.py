from cmu_112_graphics import *
import random
import tkinter as tk
from datetime import date,datetime,timedelta
import time, random, string, math, calendar,ast

##########################################
# Main Weekly Calendar mode
##########################################
def appStarted(app):
    app.margin = 100 
    app.userProfile=None
    app.user=''
    app.categories=4
    app.cats=["to do:","events:","notes:",'highlights: ']
    app.days=['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    app.sun= [ ([]) for cat in range(app.categories) ]
    app.mon=[ ([]) for cat in range(app.categories) ]
    app.tues=[ ([]) for cat in range(app.categories) ]
    app.wed=[ ([]) for cat in range(app.categories) ]
    app.thurs=[ ([]) for cat in range(app.categories) ]
    app.fri=[ ([]) for cat in range(app.categories) ]
    app.sat=[ ([]) for cat in range(app.categories) ]
    app.weeklyCalendar={'sunday':app.sun,'monday':app.mon,'tuesday':app.tues,'wednesday':app.wed,'thursday':app.thurs,'friday':app.fri,'saturday':app.sat}
    app.weeklyCalendarUnd={'sunday':app.sun,'monday':app.mon,'tuesday':app.tues,'wednesday':app.wed,'thursday':app.thurs,'friday':app.fri,'saturday':app.sat}
    app.pointX=None
    app.pointY=None
    app.rows = app.categories
    app.cols = len(app.weeklyCalendar)
    app.underlined=''
    app.daySelected=False
    app.selected=0
    app.input=''
    app.underlined=''
    app.notesInput=''
    today=date.today().strftime("%m/%d/%Y")  #from datetime link below
    dt = datetime.strptime(today, '%m/%d/%Y') 
    app.start = dt - timedelta(days = (dt.weekday() + 1) % 7)
    app.today=date.today().strftime("%m/%d")
    app.day=date.today().strftime("%d")
    app.weekDates=getWeek(app)
    app.monthDates=''
    app.delete=False
    app.check=False
    app.notesOn=False
    app.waiting=True
    app.notes='Notes:'
    app.font='Iniya 15'
    app.alterMode=False
    app.image = None
    app.monthMode=False
    app.monthlyCalendar={'sunday':app.sun,'monday':app.mon,'tuesday':app.tues,'wednesday':app.wed,'thursday':app.thurs,'friday':app.fri,'saturday':app.sat}

def getUser(app): #gets content from user text file
    result = dict()
    with open(f'users/{app.user}.txt') as content:
        for line in content:
            dicti=ast.literal_eval(line)  #from https://www.kite.com/python/docs/ast.literal_eval
            result.update(dicti)
    return result

def getFont(app): #gets content from user text file
    result = dict()
    with open(f'users/{app.user}_font.txt') as content:
        for line in content:
            dicti=ast.literal_eval(line) #from https://www.kite.com/python/docs/ast.literal_eval
            result.update(dicti)
    return result

def getNotes(app): #gets previously stored notes
    content=open(f'users/{app.user}_Notes.txt','r+')
    lines=content.read()
    return lines

def makeUserProfile(app): #creates user file/adds new data
    f = open(f'users/{app.user}.txt', "a")
    f.write(f'{app.weeklyCalendar}\n')
    f.close()
    return f'users/{app.user}.txt'

def makeUserFont(app): #creates user file/adds new data
    f = open(f'users/{app.user}_font.txt', "a")
    f.write(f'{app.weeklyCalendarUnd}\n')
    f.close()
    return f'users/{app.user}_font.txt'

def makeNotes(app): #creates user notes file/adds new data
    f = open(f'users/{app.user}_Notes.txt', "a")
    f.write(f'{app.notesInput}; ')
    f.close()
    return f'users/{app.user}_Notes.txt'
def getWeek(app):  #gets dates for current week; learned from https://docs.python.org/3/library/datetime.html
    weekDates=[]
    lastDay=app.start+timedelta(days=6)
    n=0
    while n<=6:
        lastDay=app.start+timedelta(days=n)
        weekDates.append(lastDay.strftime('%m/%d'))
        n+=1
    return weekDates
def getWeekAlt(app,start):
    weekDates=[]
    lastDay=start+timedelta(days=6)
    n=0
    while n<=6:
        lastDay=start+timedelta(days=n)
        weekDates.append(lastDay.strftime('%m/%d'))
        n+=1
    return weekDates

def getMonth(app):
    monthDates=[]
    monthEvents=[]
    s=app.start
    u=app.user
    today=date.today()
    wIndex=today.isocalendar()[1] - today.replace(day=1).isocalendar()[1]   #https://www.mytecbits.com/internet/python/week-number-of-month
    if wIndex==1:
        i=wIndex
        monthDates.insert(wIndex,app.weekDates)
        while i<=4:
            s=s + timedelta(days=7)
            result=getWeekAlt(app,s)
            monthDates.insert(wIndex,result)
            monthEvents.insert(wIndex,getNextWeeksEvents(app))
            i+=1
    if wIndex==4:
        i=wIndex
        while i>1:
            s=s + timedelta(days=7)
            user=str(u)+' next'
            result=getWeekAlt(app,s)
            monthDates.insert(wIndex,result)
            monthEvents.insert(wIndex,getWeeksEvents(app,user))
            i+=1
        monthDates.insert(wIndex,app.weekDates)
        monthEvents.insert(wIndex,getWeeksEvents(app,app.user))
    if wIndex==2:
        a=app.start
        u=app.user
        a=a-timedelta(days=7)
        u=str(u)+' last'
        result=getWeekAlt(app,a)
        monthDates.insert(wIndex-1,result)
        monthEvents.insert(wIndex-1,getWeeksEvents(app,u))
        monthDates.insert(wIndex,app.weekDates)
        monthEvents.insert(wIndex,getWeeksEvents(app,app.user))
        
        i=wIndex
        a=app.start
        u=app.user
        while i<=4:
            a=a + timedelta(days=7)
            u=str(u)+' next'
            result=getWeekAlt(app,a)
            monthDates.insert(i,result)
            monthEvents.insert(i,getWeeksEvents(app,u))
            i+=1
    if wIndex==3:
        s=s-timedelta(days=7)
        result=getWeekAlt(app,s)
        monthDates.insert(wIndex-2,result)
        s=s-timedelta(days=7)
        result=getWeekAlt(app,s)
        monthDates.insert(wIndex-1,result)
        monthDates.insert(wIndex,app.weekDates)
        i=wIndex
        while i<=4:
            s=s + timedelta(days=7)
            result=getWeekAlt(app,s)
            monthDates.insert(wIndex,result)
            i+=1
    return monthDates,monthEvents
def keyPressed(app,event):
    if (event.key == '|') and app.daySelected==False: #from course notes https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
        app.saveSnapshot()
    if app.userProfile==None and len(str(event.key))==1:
        app.user+=event.key
    if app.userProfile==None and event.key=="Delete":
        app.user=app.user[0:-1]
    if event.key=="Enter" and app.daySelected==False and app.notesOn==False:
        app.userProfile=app.weeklyCalendar
        app.waiting=False
        try:
            app.weeklyCalendar=getUser(app)
        except:
            makeUserProfile(app)
        try:
            app.notes=getNotes(app)
        except:
            makeNotes(app)
        try:
            app.weeklyCalendarUnd=getFont(app)
        except:
            makeUserFont(app)
        a=app.user
        appStarted(app)
        app.user=a
        app.weeklyCalendar=getUser(app)
        app.notes=getNotes(app)
        app.weeklyCalendarUnd=getFont(app)
        app.userProfile=app.weeklyCalendar
        app.waiting=False
    if app.daySelected==True and event.key=='~':
        app.alterMode=True
    if app.alterMode==True and event.key=='-':
        app.alterMode=False
    if app.daySelected==True and event.key!='Enter' and event.key!='~' and event.key!='-':
        if app.alterMode==True:
            if event.key=='Space': 
                app.input=str(app.input)+' '
                app.underlined=str(app.underlined)+' '
            elif event.key=="Delete":
                app.input=app.input[0:-1]
                app.underlined=app.underlined[0:-1]
            else:
                app.input=str(app.input)+str(event.key)  
                app.underlined=str(app.underlined)+str(event.key) 
        else:
            if event.key=='Space':
                app.input=str(app.input)+' '
            elif event.key=="Delete":
                app.input=app.input[0:-1]
            else:
                app.input=str(app.input)+str(event.key) 
    elif app.daySelected==True and app.alterMode==False and event.key=="Enter":
        app.weeklyCalendar[app.days[app.selected[1]]][app.selected[0]].append(app.input)
        app.weeklyCalendarUnd[app.days[app.selected[1]]][app.selected[0]].append(app.underlined)
        app.input=''
        app.underlined=''
        app.alterMode=False
        app.daySelected=False
        makeUserProfile(app)
        makeUserFont(app)
    if event.key=="Escape":
        app.user=''
        app.waiting=True
        app.userProfile=None
        appStarted(app)
    if event.key=="Down":
        app.delete=True
    if event.key=="Up":
        app.delete=False
    if event.key=='+' and app.daySelected==False:
        app.check=True
    elif event.key=='+' and app.check==True:
        app.check=False
    if app.notesOn==True and event.key!='Enter':
        if event.key=='Space':
            app.notesInput=str(app.notesInput)+' '
        elif event.key=="Delete":
            app.notesInput=app.notesInput[0:-1]
        else:
            app.notesInput=str(app.notesInput)+str(event.key)      
    if app.notesOn==True and event.key=="Enter":
        makeNotes(app)
        app.notesInput=''
        app.notes=getNotes(app)
        app.notesOn=False

    if event.key=='Right':
        u=app.user
        s=app.start
        appStarted(app)
        if 'last' in u:
            app.user=u[:-5]
        else:
            app.user=str(u)+' next'
        app.start=s+timedelta(days=7)
        app.weekDates=getWeek(app)
        app.userProfile=app.weeklyCalendar
        try:
            app.weeklyCalendar=getUser(app)
        except:
            makeUserProfile(app)
            app.weeklyCalendar=getUser(app)
        try:
            app.notes=getNotes(app)
        except:
            makeNotes(app)
            app.notes=getNotes(app)
        try:
            app.weeklyCalendarUnd=getFont(app)
        except:
            makeUserFont(app)
            app.weeklyCalendarUnd=getFont(app)
        app.waiting=False
    if event.key=='Left':
        u=app.user
        s=app.start
        appStarted(app)
        if 'next' in u:
            app.user=u[:-5]
        else:
            app.user=str(u)+' last'
        app.start=s - timedelta(days=7)
        app.weekDates=getWeek(app)
        app.userProfile=app.weeklyCalendar
        try:
            app.weeklyCalendar=getUser(app)
        except:
            makeUserProfile(app)
            app.weeklyCalendar=getUser(app)
        try:
            app.notes=getNotes(app)
        except:
            makeNotes(app)
            app.notes=getNotes(app)
        try:
            app.weeklyCalendarUnd=getFont(app)
        except:
            makeUserFont(app)
            app.weeklyCalendarUnd=getFont(app)
        app.waiting=False

def mousePressed(app, event):
    if app.user!='':
        if event.x<85 and event.y<30 and app.monthMode==False:
            app.monthDates,app.monthEvents=getMonth(app)
            app.monthMode=True
        elif event.x<85 and event.y<30 and app.monthMode==True:
            app.monthMode=False
        if (app.width//8)<event.x<(app.width-app.width//8) and (app.height-app.height//8)<event.y<(app.height-app.height//48):
            app.notesOn=True
        if pointInGrid(app,event.x,event.y)==True:
            (row, col) = getCell(app, event.x, event.y)
            app.selected=(row,col)
            app.daySelected=True
            app.pointX,app.pointY=event.x,event.y
        if app.delete==True and pointInGrid(app,event.x,event.y)==True:
            (row, col) = getCell(app, event.x, event.y)
            (x0,y0,x1,y1)=getCellBounds(app,row,col)
            line=int((event.y-y0)//15)
            removeLine(app,row,col,line)
        if app.check==True and pointInGrid(app,event.x,event.y)==True:
            (row, col) = getCell(app, event.x, event.y)
            (x0,y0,x1,y1)=getCellBounds(app,row,col)
            line=int((event.y-y0)//15)
            removeLine(app,row,col,line)
            app.input=str(app.input)+'✓'
            app.check=False

def removeLine(app,row,col,line): #works in delete/edit mode, edits last in list
    words=app.weeklyCalendar[app.days[col]][row]
    app.input=words[line]
    words.pop(line)
    app.weeklyCalendar[app.days[col]][row]=words
    makeUserProfile(app)
    makeUserFont(app)
    app.delete=False

def getWeeksEvents(app,user):
    u=user
    events={'sunday':[],'monday':[],'tuesday':[],'wednesday':[],'thursday':[],'friday':[],'saturday':[]}
    result = dict()
    with open(f'users/{user}.txt') as content:
        for line in content:
            dicti=ast.literal_eval(line)  #from https://www.kite.com/python/docs/ast.literal_eval
            result.update(dicti)
    for col in range(app.cols):
        events[app.days[col]]=result[app.days[col]][1]
    return events

def pointInGrid(app, x, y): #from course; https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))

def getCell(app, x, y):#from course notes; https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    # aka "viewToModel"
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)
    return (row, col)

def getCellBounds(app, row, col): #from course notes; https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    # aka 'modelToView'
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

def drawBoard(app, canvas):
    canvas.create_text(app.width//2,30,text='Weekly Planner',font='Iniya 40 underline',fill='navy')
    for row in range(app.rows):
        (x0, y0, x1, y1) = getCellBounds(app, row, 0)
        canvas.create_text(x0-45, (y0+y1)//2,text=app.cats[row],fill='steel blue',font='Iniya 18')
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            if app.selected!=(row,col):
                canvas.create_rectangle(x0, y0, x1, y1, fill='peach puff')
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill='pale violet red')
    for col in range(app.cols):
        (x0, y0, x1, y1) = getCellBounds(app, 0, col)
        if app.weekDates[col]==app.today: 
            canvas.create_text((x0+x1)//2, y0-25,text=app.weekDates[col],fill='hot pink',font='Iniya 16')
            canvas.create_text((x0+x1)//2, y0-10, text=app.days[col],fill='deep pink',font='Iniya 18') 
            for row in range(app.rows):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill='pink')
        else:
            canvas.create_text((x0+x1)//2, y0-25,text=app.weekDates[col],fill='darkorchid3',font='Iniya 16')
            canvas.create_text((x0+x1)//2, y0-10, text=app.days[col],fill='darkorchid4',font='Iniya 18')
    if app.selected!=0:
        (x0, y0, x1, y1) = getCellBounds(app, app.selected[0], app.selected[1])
        canvas.create_rectangle(x0, y0, x1, y1, fill='pale violet red')
        y=0
        for x in range(len(app.input)):
            y=x
            i=0
            if app.input[x] in app.underlined[i:]:
                canvas.create_text(x0+10+7*y, y1-(y1-y0)//6,text=f'{app.input[x]}',font='Iniya 15 underline',activefill='white')
                i+=1
            else:
                canvas.create_text(x0+10+7*y, y1-(y1-y0)//6,text=f'{app.input[x]}',font='Iniya 15',activefill='white')

def drawEvents(app,canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            words=app.weeklyCalendar[app.days[col]][row]
            font=app.weeklyCalendarUnd[app.days[col]][row]
            dY=0 
            y=0
            for j in range(len(words)):
                y=0
                if app.weekDates[col]<app.today:
                    word=words[j]
                    for x in range(len(word)):
                        if word[x] in font[j]:
                            canvas.create_text(x0+10+y,y0+15+dY,text=f'{word[x]}',font='Iniya 15 underline',activefill='white')
                        else:
                            canvas.create_text(x0+10+y,y0+15+dY,text=f'{word[x]}',font='Iniya 15',activefill='white')
                        y+=7
                    dY+=15
                else:
                    word=words[j]
                    for x in range(len(word)):
                        if word[x] in font[j]:
                            canvas.create_text(x0+10+y,y0+15+dY,text=f'{word[x]}',font='Iniya 15 underline',activefill='white')
                        else:
                            canvas.create_text(x0+10+y,y0+15+dY,text=f'{word[x]}',font='Iniya 15',activefill='white')
                        y+=7
                    dY+=15

def drawWeekNotes(app,canvas):
    canvas.create_rectangle(app.width//8, app.height-app.height//8, app.width-app.width//8, app.height-app.height//48, fill='light sky blue',outline='steel blue')
    canvas.create_text(app.width//2, app.height-app.height//8+15,text=f'{app.notes}',font='Iniya 15',width=app.width-2*app.width//8)
    canvas.create_text(app.width//2, app.height-app.height//48-15,text=f'{app.notesInput}',font='Iniya 15')

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='linen')
    if app.waiting==True:
        canvas.create_text(app.width//2,30,text='Weekly Planner',font='Iniya 40 underline',fill='navy')
        canvas.create_text(app.width//2,app.height//2-60,text=f'User: {app.user}',font='Iniya 30')
        canvas.create_text(app.width//2,app.height//2,text='Enter your username above!',font='Iniya 45',fill='deep pink')
    if app.monthMode==False and app.waiting==False:
        drawBoard(app, canvas)
        drawEvents(app,canvas)
        drawWeekNotes(app,canvas)
        canvas.create_rectangle(4,4,85,30,fill='steel blue')
        canvas.create_text(44,16,text='4 week view',fill='navy',font='Iniya 15')
        canvas.create_text(350, 16, text='Press | to saveSnapshot',font='Iniya 15')
        canvas.create_text(350, 28, text='Press ~/- to toggle underline',font='Iniya 15')
        canvas.create_text(350, 40, text='Press Down/Up to toggle Edit Mode',font='Iniya 15')
        canvas.create_text(350, 52, text='Press + to check off (then select line)',font='Iniya 15')
        canvas.create_text(app.width-app.width//9,20,text=f'User: {app.user}',font='Iniya 18')
    elif app.monthMode==True and app.waiting==False:
        drawMonthBoard(app,canvas)
        canvas.create_rectangle(4,4,85,30,fill='steel blue')
        canvas.create_text(44,16,text='1 week view',fill='navy',font='Iniya 15')
        canvas.create_text(350, 16, text='Press | to saveSnapshot',font='Iniya 15')
        canvas.create_text(app.width-app.width//9,20,text=f'User: {app.user}',font='Iniya 18')
    if (app.image != None): #from course notes; https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
        canvas.create_image(1325, 700, image=ImageTk.PhotoImage(app.image))

def drawMonthBoard(app, canvas):
    canvas.create_text(app.width//2,30,text='Monthly Planner',font='Iniya 40 underline',fill='navy')
    for col in range(app.cols):
        (x0, y0, x1, y1) = getCellBounds(app, 0, col)
        canvas.create_text((x0+x1)//2, y0-10, text=app.days[col],fill='darkorchid4',font='Iniya 18')
    for row in range(app.rows):
        (x0, y0, x1, y1) = getCellBounds(app, row, 0)
        canvas.create_text(x0-45, (y0+y1)//2,text=str(row+1),fill='steel blue',font='Iniya 18')
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill='peach puff')
            if app.monthDates[row][col]==app.today: 
                canvas.create_rectangle(x0, y0, x1, y1, fill='pink')
                canvas.create_text((x0+x1)//2, y0+10, text=app.monthDates[row][col],fill='deep pink',font='Iniya 18 underline')
            else:
                canvas.create_text((x0+x1)//2, y0+10,text=app.monthDates[row][col],font='Iniya 18',fill='deep pink')
            dy=0
            for h in range(len(app.monthEvents[row][app.days[col]])):
                canvas.create_text((x0+x1)//2, (y0+y1)//2+dy,text=app.monthEvents[row][app.days[col]][h],font='Iniya 15')
                dy+=15
runApp(width=1350, height=700)

