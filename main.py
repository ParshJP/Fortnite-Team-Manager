# Jonah Dabu, Parshva Parikh
# 2020/11/4
# ICS 4U
# Fortnite Tournament team and player generator

import operator         #import necessary modules
import os
import random
from tkinter import Tk, ttk, Frame, PhotoImage, Label, LabelFrame, Text, Button, Toplevel, Scrollbar, \
    filedialog, messagebox, END, simpledialog
from Player import Player       #import Player class

players = []  # list of player objects
pData = []      #list of player data
f = ''      #txt file var

def getPlayers():       #if user clicks get players button, get a text file to read from
    global pData, players, f
    #warn player that a new file will be read from if user has made previous changes
    answer = messagebox.askyesno('Get Players',
                                 "This will select a new file to read from.\nMake sure you 'Save Teams' before continuing IF you made any PREVIOUS changes.\nWould you like to get a new player list?")
    if answer:      #if they choose yes, use a filedialog to get the text file they select
        pData, players = [], []     #reset player data lists
        f = filedialog.askopenfilename(initialdir=os.getcwd(),
                                       filetypes=(("Text files (*.txt)", "*.txt"), ("All files (*.*)", "*.*")))
        try:
            with open(f, "r") as file:      #read the file and take the info of each line into a list
                line = file.readline()
                pData.append(line.split(","))
                while line != "":
                    line = file.readline()
                    if line != "":
                        pData.append(line.split(","))
            players = [0] * len(pData)      #set the player object list length

            for index in range(len(pData)):     #set the values for the player object
                players[index] = Player()
                players[index].setLast(pData[index][0])
                players[index].setFirst(pData[index][1])
                players[index].setFull(pData[index][1], pData[index][0])
                players[index].setRating(pData[index][2])
                players[index].setTier(pData[index][3].strip("\n"))
                btnView.config(state='normal')      #change button configs
                btnGenerate.config(state='normal')
        except Exception as errMessage:     #error message if the file doesn't work
            messagebox.showerror("Get Players", "Selected file is incompatible.\n\n" + str(errMessage))


def close_topview():        #when user clicks out of the toplevel window
    top_level.withdraw()
    root.update()
    root.deiconify()
    btnGenerate.config(state='normal'), btnSave.config(state = 'disabled')      #change button configs


def view_players():     #When user clicks to view the players, switch to top window and set all the players in the treeview
    root.withdraw()
    top_level.update()
    top_level.deiconify()
    for i in tview.get_children():
        tview.delete(i)
    for x in range(len(players)):
        tview.insert("", END, values=(players[x].getLast(), players[x].getFirst(),
                                      players[x].getRating(), players[x].getTier()))


def close_program():        #if user clicks to exit the program, resave the text file with the manipulated data
    answer = messagebox.askyesno('Fortnite Team Tournament', 'Are you sure you want to exit?')
    if answer:
        messagebox.showinfo('Fortnite Team Tournament', 'Thank you!')
        if f != '':
            with open(f, 'wt') as writer:       #resave if a file has been selected
                for player in players:
                    writer.write(player.getLast() + ',' + player.getFirst() + ',' + str(player.getRating()) + ',' + player.getTier())
                    writer.write('\n')
        top_level.destroy()
        root.destroy()
        exit()


def remove_player():    #remove a player on the treeview
    try:
        iid = tview.selection()     #get selection and store its values in a list
        idvalues = tview.item(iid)['values']
        #ask user to confirm the removal
        answer = messagebox.askyesno("Remove Player",
                                     "Are you sure you want to remove " + idvalues[1] + " " + idvalues[0] + "?")
        if answer:
            tview.delete(iid)   #delete the selection and update the player list
            update_players()
    except:
        messagebox.showerror('Remove Player', 'Please select a player to remove.')  #error if nothing is selected


def add_player():       #add player if user chooses to on treeview
    exists, firstName, lastName = False, '', ''     #set vars
    if len(players) < 64:       #only add a player if there is space (max of 64)
        while firstName == '':      #for first and last name, unless user presses cancel, loop until user enters a valid value
            firstName = simpledialog.askstring("Add Player", "Enter player's first name:")
            if firstName == '':
                messagebox.showerror("Add Player", "First name cannot be blank!")
            elif firstName is None:
                break
            else:
                while lastName == '':
                    lastName = simpledialog.askstring("Add Player", "Enter player's last name:")
                    if lastName == "":
                        messagebox.showerror("Add Player", "Last name cannot be blank!")
                    elif lastName is None:
                        break
                    else:
                        full = firstName + ' ' + lastName       #check if player being added already exists by looping through the player list and comparing
                        for index, x in enumerate(tview.get_children()):
                            if tview.item(x)['values'][1].lower() + ' ' + tview.item(x)['values'][0].lower() == full.lower():
                                exists = True
                                messagebox.showerror('Add Player', players[index].getFull() + ' already exists!')
                                tview.selection_set(x)      #select the existing player
                                tview.see(x)
                        while not exists:           #if the player doesn't exist, ask user for rating (same type of loop as names)
                            rating = simpledialog.askinteger('Add Player', "Enter player's rating (1-100):")
                            if rating is None:
                                break
                            elif rating < 0 or rating > 100:
                                messagebox.showerror("Add Player", "Rating must be from 1 - 100!")      #rating must be 1-100
                            else:
                                if rating < 50:
                                    tier = "Scout"
                                elif 50 <= rating <= 59:
                                    tier = "Ranger"                 #determine player's tier off of the rating
                                elif 60 <= rating <= 69:
                                    tier = "Agent"
                                elif 70 <= rating <= 79:
                                    tier = "Epic"
                                else:
                                    tier = "Legend"
                                iid = tview.insert("", END, values=(lastName, firstName, rating, tier))     #insert the player and select them
                                tview.selection_set(iid)
                                tview.see(iid)
                                update_players()        #update the player list
                                break
    else:
        messagebox.showwarning('Add Player', 'No more players can be added.\nThe tournament has reached its capacity of 64 competitors.')       #if the tourny is full, warn user


def edit_player():      #edit player if user chooses to in treeview
    try:
        iid = tview.selection()     #get the selected player and store values in a list
        idvalues = tview.item(iid)['values']
        for player in players:      #ask user to change the player rating
            if player.getFirst() == idvalues[1] and player.getLast() == idvalues[0]:
                rating = simpledialog.askinteger('Edit Player', "Enter " + player.getFull() + " rating (1-100):")
                if rating is None:
                    break
                elif rating < 0 or rating > 100:
                    messagebox.showerror("Edit Player", "Rating must be from 1 - 100!")     #rating must be 1-100
                else:
                    if rating < 50:
                        tier = "Scout"      #set the player tier according to rating
                    elif 50 <= rating <= 59:
                        tier = "Ranger"
                    elif 60 <= rating <= 69:
                        tier = "Agent"
                    elif 70 <= rating <= 79:
                        tier = "Epic"
                    else:
                        tier = "Legend"
                    tview.selection_set(iid)        #select the edited player and update the player list
                    tview.see(iid)
                    tview.item(iid, values = (player.getLast(), player.getFirst(), rating, tier))
                    update_players()
                    break
    except:
        messagebox.showerror('Edit Player', 'Please select a player to edit.')      #error if no player is selected


def search_player():        #search for a player if the user chooses too
    found = False
    name = simpledialog.askstring("Search Player", "Enter player's name (FirstName LastName):")     #ask for player full name
    if name == '':
        messagebox.showerror("Search Player", "Name cannot be blank!")      #error is user leaves it blank
    elif name is None:
        pass
    else:
        for x in tview.get_children():      #cycle through the players to find the searched name and select if found
            if tview.item(x)['values'][1].lower() + ' ' + tview.item(x)['values'][0].lower() == name.lower():
                found, iid = True, x
                break
        if found:
            tview.selection_set(iid)
            tview.see(iid)
        else:
            messagebox.showerror("Search Player", name + " is not entered in the tournament!")      #if not found, output error to user


def sort_columns(colnum):       #sort the columns by certain orders when selected
    global players
    if colnum == 1:     #sort name columns by ascending
        players.sort(key = lambda x: operator.attrgetter('last')(x).lower())
    elif colnum == 2:
        players.sort(key = lambda x: operator.attrgetter('first')(x).lower())
    elif colnum == 3:       #sort rating by descending and then name by ascending
        players = sorted(sorted(players,key = lambda x: operator.attrgetter('last')(x).lower()),
                         key=lambda x: operator.attrgetter('rating')(x), reverse=True)
    else:       #sort tier by ascending, rating by descending and name by descending
        players = sorted(sorted(sorted(players, key=lambda x: operator.attrgetter('last')(x).lower()),
                                key=lambda x: operator.attrgetter('rating')(x), reverse=True),
                         key=lambda x: operator.attrgetter('tier')(x).lower())
    view_players()     #update the treeview


def update_players():       #function that updates the players list by cycling through each list and resetting the values
    global players, pData
    players, pData = [], []
    for x in tview.get_children():
        info = tview.item(x)['values']
        pData.append(info)
    players = [0] * len(pData)
    for index in range(len(pData)):
        players[index] = Player()
        players[index].setLast(pData[index][0])
        players[index].setFirst(pData[index][1])
        players[index].setFull(pData[index][1], pData[index][0])
        players[index].setRating(pData[index][2])
        players[index].setTier(pData[index][3])


def generate_teams():       #randomize the teams based off the number of players, teams cannot have less then 3 players and more then 4
    global lblFrames, txtTeams
    btnClear.config(state = 'normal'), btnSave.config(state = 'normal'), btnGenerate.config(state = 'disabled') #config buttons
    random.shuffle(players)     #randomize the players
    x, index = len(players) % 4, 0      #get the outliers and set a index values

    if x == 0:          #if there are full teams of 4, cycle through the player lists and frames to add 4 players (name, rank) to each
        for t in range(len(lblFrames)):
            txtTeams[t].pack_forget()
            txtTeams[t] = Text(lblFrames[t], width=25, height=6, font=('Consolas', 8), relief='flat', bg='white')
            txtTeams[t].pack(padx=5, pady=5)
            trating = 0
            if index >= len(players):
                break
            for num in range(4):
                txtTeams[t].insert(END, "{0:<22s}{1:>3d}\n".format(players[index].getFull(), players[index].getRating()))
                trating += players[index].getRating()
                index += 1
                if num == 3:
                    trating /= 4
                    txtTeams[t].insert(END, "\n{0:<22s}{1:>3d}".format('TEAM RATING: ', round(trating)))        #output the team avg
            txtTeams[t].config(state = 'disabled')

    elif x == 3:        #if there are full teams of 4 and 3 players outlying, cycle through the player lists and frames to add 4 players (name, rank) to each, but 3 for the last one
        for t in range(len(lblFrames)):
            txtTeams[t].pack_forget()
            txtTeams[t] = Text(lblFrames[t], width=25, height=6, font=('Consolas', 8), relief='flat', bg='white')
            txtTeams[t].pack(padx=5, pady=5)
            trating = 0
            if index >= len(players)-3:
                break
            for num in range(4):
                txtTeams[t].insert(END, "{0:<22s}{1:>3d}\n".format(players[index].getFull(), players[index].getRating()))
                trating += players[index].getRating()
                index += 1
                if num == 3:
                    trating /= 4
                    txtTeams[t].insert(END, "\n{0:<22s}{1:>3d}".format('TEAM RATING: ', round(trating)))    #output the team avg
            txtTeams[t].config(state='disabled')
        txtTeams[t].pack_forget()           #team with one less player
        txtTeams[t] = Text(lblFrames[t], width=25, height=6, font=('Consolas', 8), relief='flat', bg='white')
        txtTeams[t].pack(padx=5, pady=5)
        trating = 0
        for num in range(index, index+3):
            txtTeams[t].insert(END, "{0:<22s}{1:>3d}\n".format(players[num].getFull(), players[num].getRating()))
            trating += players[num].getRating()
            if num == index + 2:
                trating /= 3
                txtTeams[t].insert(END, "\n{0:<22s}{1:>3d}".format('TEAM RATING: ', round(trating)))        #output the team avg
        txtTeams[t].config(state='disabled')

    elif x == 2:            #if there are full teams of 4 and 2 players outlying, cycle through the player lists and frames to add 4 players (name, rank) to each, but 3 for the last two
        for t in range(len(lblFrames)):
            txtTeams[t].pack_forget()
            txtTeams[t] = Text(lblFrames[t], width=25, height=6, font=('Consolas', 8), relief='flat', bg='white')
            txtTeams[t].pack(padx=5, pady=5)
            trating = 0
            if index >= len(players)-6:
                break
            for num in range(4):
                txtTeams[t].insert(END, "{0:<22s}{1:>3d}\n".format(players[index].getFull(), players[index].getRating()))
                trating += players[index].getRating()
                index += 1
                if num == 3:
                    trating /= 4
                    txtTeams[t].insert(END, "\n{0:<22s}{1:>3d}".format('TEAM RATING: ', round(trating)))        #output the team avg
            txtTeams[t].config(state='disabled')
        for a in range(t, t+2):     #2 teams with one less player
            txtTeams[a].pack_forget()
            txtTeams[a] = Text(lblFrames[a], width=25, height=6, font=('Consolas', 8), relief='flat', bg='white')
            txtTeams[a].pack(padx=5, pady=5)
            trating = 0
            for num in range(3):
                txtTeams[a].insert(END, "{0:<22s}{1:>3d}\n".format(players[index].getFull(), players[index].getRating()))
                trating += players[index].getRating()
                index += 1
                if num == 2:
                    trating /= 3
                    txtTeams[a].insert(END, "\n{0:<22s}{1:>3d}".format('TEAM RATING: ', round(trating)))        #output the team avg
            txtTeams[a].config(state='disabled')

    elif x == 1:        #if there are full teams of 4 and 1 player outlying, cycle through the player lists and frames to add 4 players (name, rank) to each, but 3 for the last three
        for t in range(len(lblFrames)):
            txtTeams[t].pack_forget()
            txtTeams[t] = Text(lblFrames[t], width=25, height=6, font=('Consolas', 8), relief='flat', bg='white')
            txtTeams[t].pack(padx=5, pady=5)
            trating = 0
            if index >= len(players)-9:
                break
            for num in range(4):
                txtTeams[t].insert(END, "{0:<22s}{1:>3d}\n".format(players[index].getFull(), players[index].getRating()))
                trating += players[index].getRating()
                index += 1
                if num == 3:
                    trating /= 4
                    txtTeams[t].insert(END, "\n{0:<22s}{1:>3d}".format('TEAM RATING: ', round(trating)))        #output the team avg
            txtTeams[t].config(state='disabled')
        for a in range(t, t+3):         #3 teams with 1 less player
            txtTeams[a].pack_forget()
            txtTeams[a] = Text(lblFrames[a], width=25, height=6, font=('Consolas', 8), relief='flat', bg='white')
            txtTeams[a].pack(padx=5, pady=5)
            trating = 0
            for num in range(3):
                txtTeams[a].insert(END, "{0:<22s}{1:>3d}\n".format(players[index].getFull(), players[index].getRating()))
                trating += players[index].getRating()
                index += 1
                if num == 2:
                    trating /= 3
                    txtTeams[a].insert(END, "\n{0:<22s}{1:>3d}".format('TEAM RATING: ', round(trating)))        #output the team avg
            txtTeams[a].config(state='disabled')


def save_teams():       #when user saves file, write the generated teams to a word doc
    filename = filedialog.asksaveasfilename(initialdir=os.getcwd(), filetypes=[("Word Document (*.doc)", "*.doc")])     #use file dialouge so user can save
    with open (filename, 'w') as writer:
        for i in range(len(txtTeams)):      #cycle through each text widget and append the info
            writer.write('TEAM ' + str(i+1))
            writer.write('\n\n')
            writer.write(txtTeams[i].get(1.0, 'end-1c'))
            writer.write('\n\n\n')


def clear_teams():          #clear the generated team and configure buttons
    for t in range(len(lblFrames)):
        txtTeams[t].pack_forget()
        txtTeams[t] = Text(lblFrames[t], width=25, height=6, font=('Consolas', 8), state = 'disabled', relief='flat', bg='white')
        txtTeams[t].pack(padx=5, pady=5)
        btnClear.config(state = 'disabled'), btnSave.config(state = 'disabled'), btnGenerate.config(state = 'normal')


root = Tk()     # create thw window
root.title('Fortnite Team Tournament')
root.protocol('WM_DELETE_WINDOW', close_program)
root.geometry('%dx%d+%d+%d' % (912, 740, root.winfo_screenwidth() // 2 - 912 // 2,
                               root.winfo_screenheight() // 2 - 740 // 2))
root.resizable(False, False)

frame = Frame(root, padx=10, pady=10, bg='white')       #create frame holding the widgets
frame.pack()

imgBanner = PhotoImage(file='images/fortnite_banner.png')       #create the banner image
lblBanner = Label(frame, image=imgBanner, padx=10, pady=10, borderwidth=0)
lblBanner.grid(row=0, column=0, columnspan=5, pady=5)

lblFrames = [0] * 16    #create a list holding the label frames and another holding the textboxes in them
txtTeams = [0] * 16
rownum, colnum = 1, 0
                            #create them with a loop
for i in range(len(lblFrames)):
    lblFrames[i] = LabelFrame(frame, text='TEAM ' + str(i + 1), bg='white', font=('Consolas', 11, 'bold'))
    txtTeams[i] = Text(lblFrames[i], width=25, height=6, font=('Consolas', 8), state='disabled', relief='flat',
                       bg='white')
    txtTeams[i].pack(padx=5, pady=5)

    lblFrames[i].grid(row=rownum, column=colnum, padx=5, pady=5)
    if (i + 1) % 4 == 0:
        rownum += 1
        colnum = 0          #4x4 lblframe grid
    else:
        colnum += 1

buttonFrame = Frame(frame, padx=10, pady=10, bg='white')        #frame holding the buttons
buttonFrame.grid(row=1, column=4, rowspan=4)
        #create all the buttons on the main window to manipulate files and teams and windows
btnPlayers = Button(buttonFrame, text='GET PLAYERS', width=15, height=2, command=getPlayers)
btnPlayers.pack(side='top', padx=5, pady=5)
btnView = Button(buttonFrame, text='VIEW PLAYERS', width=15, height=2, state = 'disabled', command=view_players)
btnView.pack(side='top', padx=5, pady=5)
btnGenerate = Button(buttonFrame, text='GENERATE', width=15, height=2, state='disabled', command=generate_teams)
btnGenerate.pack(side='top', padx=5, pady=5)
btnSave = Button(buttonFrame, text='SAVE TEAMS', width=15, height=2, state='disabled', command = save_teams)
btnSave.pack(side='top', padx=5, pady=5)
btnClear = Button(buttonFrame, text='CLEAR', width=15, height=2, state = 'disabled', command=clear_teams)
btnClear.pack(side='top', padx=5, pady=5)
btnExit = Button(buttonFrame, text='EXIT', width=15, height=2, command=close_program)
btnExit.pack(side='top', padx=5, pady=5)

imgLogo = PhotoImage(file='images/fortnite_logo.png')   #image for the bottom logo
lblLogo = Label(buttonFrame, image=imgLogo, borderwidth=0, bg='white').pack(side='top', padx=5, pady=5)

'''
This is the window that lets you view, add, and remove players
'''

top_level = Toplevel(padx=10, pady=10, bg='white')      #create top level window
top_level.title('Player List')
top_level.resizable(False, False)
top_level.protocol('WM_DELETE_WINDOW', close_topview)
top_level.geometry(
    '%dx%d+%d+%d' % (490, 635, root.winfo_screenwidth() // 2 - 490 // 2, root.winfo_screenheight() // 2 - 635 // 2))
top_level.withdraw()

img = PhotoImage(file='images/fortnite.png')        #banner image on top_level
lblImg = Label(top_level, image=img, bg='white')
lblImg.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

style = ttk.Style() #set the font and style for the top view
style.configure('mystyle.Treeview.Heading', foreground='gold', font=('Consolas', 11, 'bold'))

tview = ttk.Treeview(top_level, selectmode='browse', columns=('1', '2', '3', '4'), show='headings', height=20,
                     style='mystyle.Treeview')  #set the treeview widget
tview.grid(row=1, column=0, pady=5)

headingtext = ('LAST NAME', 'FIRST NAME', 'RATING', 'TIER')     #column headers and widths
columnwidths = [150, 150, 75, 75]

for i in range(4):      #create the columns
    tview.column(str(i + 1), width=columnwidths[i], anchor='w')
    tview.heading(str(i + 1), text=headingtext[i], anchor='w', command = lambda columnid=i+1: sort_columns(columnid))

vscroll = Scrollbar(top_level, orient='vertical', command=tview.yview)  #create scroll bar
vscroll.grid(row=1, column=1, sticky='ns')

bottomFrame = Frame(top_level, padx=5, pady=5, bg='white')      #button frame
bottomFrame.grid(row=2, column=0, columnspan=2)
    #buttons to manipulate players
btnRemove = Button(bottomFrame, text='REMOVE', width=10, pady=5, command=remove_player)
btnRemove.pack(side='left', padx=5, pady=5)
btnAdd = Button(bottomFrame, text='ADD', width=10, pady=5, command=add_player)
btnAdd.pack(side='left', padx=5, pady=5)
btnEdit = Button(bottomFrame, text='EDIT', width=10, pady=5, command=edit_player)
btnEdit.pack(side='left', padx=5, pady=5)
btnSearch = Button(bottomFrame, text='SEARCH', width=10, pady=5, command=search_player)
btnSearch.pack(side='left', padx=5, pady=5)

root.mainloop()     #loop the interface