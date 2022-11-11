#############################
#Program Tic-Tac-Toe        #
#Norbert Horváth, I. ročník #
#Zimný semester 2021/2022   #
#Programování 1, NPRG030    #
#############################
from tkinter import *
from tkinter import messagebox

def gameobrazovka():  #okno hry
    menu.destroy() #zničí menu

    #urobím zo všetkého globálne premennú, tak môžem použit všetkých
    global tabula, AI, botcounter, tiecounter, playercounter 
    
    #spočítá koľko krát kto vyhral
    botcounter = 0 #spočíta počet výher počítaču
    tiecounter= 0  #ak je remíza
    playercounter = 0 #spočíta počet výher hráča - vždy bude 0
    
    #tabuľa
    tabula = [None] * 9

    AI = False  #definuje kto začína, ak AI = False tak hráč.
    
    def ai():
        global AI 
        
        #prvý ťah, ktorý urobí program, bude vždy v rohu, lebo to je najlepší ťah, ktorý môže urobiť, urýchly program
        tabula[0] = 'X'
        kresli()
        AI = True

    #vráti všetky volné štverce
    def dostupne_pohyby(seznam):
        tahy = []
        for x in range(9):
            if None == seznam[x]:
                tahy.append(x)
        return tahy

    #kontroluje či hra už sa skončil
    def skoncit(seznam):
        full = True #full je True ak celá tabuľa je plný  
        for x in range(9):
            if seznam[x] == None:
                full = False #ak existuje volný štverec
        if full: 
            return True
        
        if vyherca(seznam) != None:
            return True

        return False
    
    #seznam výherných kombinací
    kombinace = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    # 0 1 2 \
    # 3 4 5  |- tabuľa
    # 6 7 8 /

    #vráti výťaza, None ak vyhral počítač
    def vyherca(seznam):
        for hrac in ['X', 'O']:
            pozicia_hraca = pozice(hrac, seznam)
            for komb in kombinace:
                vyhra = True  
                for poz in komb: #kontroluje všetky kombinácie
                    if poz not in pozicia_hraca: #ak kombinace výherných pozicí neni v hráčových kombinací, tak vráti False
                        vyhra = False
                if vyhra: 
                    return hrac #ak hráč má výherné kombinace
        return None #ak počítač vyhral

    #vráti všetky pozície, v ktorej má hráč X alebo O
    def pozice(hrac, seznam):
        stvorec = []
        for x in range(9):          
            if seznam[x] == hrac:
                stvorec.append(x)
        return stvorec

    #nahrádza volný štverec s X alebo O 
    def tah(position, hrac, seznam):
        seznam[position] = hrac

    #minimax algoritmus
    def minimax(seznam, maxhrac):
        global AI
    
        #ak hra sa skončila, vráti -1 ak prehral počítač, 1 ak vyhral, 0 ak remíza, a tabuľu
        if skoncit(seznam):
            if AI == False:  #kontroluje, kto je na rade
                if vyherca(seznam) == 'O': 
                    return 1, seznam #ak vyhrá AI vráti 1 
                elif vyherca(seznam) == 'X':
                    return -1, seznam #ak prehrá AI vráti -1
                return 0, seznam #ak remíza
            elif AI == True: #kontroluje, kto je na rade
                if vyherca(seznam) == 'X':
                    return 1, seznam
                elif vyherca(seznam) == 'O':
                    return -1, seznam
                return 0, seznam
    
        #ak máme to najlepšiu koňečný výsledek, tak iniciliazuje
        if maxhrac:
            best = -1 #urobím najlepšiu -1 čo je menej než 0
            besttah = None 
        
            #prejde každým synom
            for tahy in dostupne_pohyby(seznam):
                if AI == False:
                    tah(tahy, 'O', seznam) 
                elif AI == True:
                    tah(tahy, 'X', seznam)
                
                val, choice = minimax(seznam, False)
                tah(tahy, None, seznam)
                
                #ak mame lepsi vysledek, tak besttah bude ten, ktory bol vyherny
                if val >= best:
                    besttah = tahy
                    best = val
            
            #vráti najlepší krok
            return best, besttah
        
        else:
            #to je presne opak, tento algoritmus minimalizuje hráčov výhru
            best = 1
            besttah = None
            for tahy in dostupne_pohyby(seznam):
                if AI == False:
                    tah(tahy, 'X', seznam)
                elif AI == True:
                    tah(tahy, 'O', seznam)
                val, choice = minimax(seznam, True)
                tah(tahy, None, seznam)
                if val <= best:
                    besttah = tahy
                    best = val
            return best, besttah

    #funkce na aktualizáciu obrazovky
    def update(event):
        global tabula
    
        #ak AI ide ako prvý
        if AI:
            
            #zabezpečenie rovnakých políčok(že hráč nemá viac ťahov ako AI)
            if len(pozice('X', tabula)) != len(pozice('O', tabula)) + 1:
                return
        else:
            
            #uistí sa, že množstvo ťahov pre každého hráča je rovnaké
            if len(pozice('O', tabula)) != len(pozice('X', tabula)):
                return
    
        #dostane koordináty políčok, a aktualizuje obrazovku
        if event.x in range(1, 99) and event.y in range(1, 99): #tabuľa[0]
            if tabula[0] == None: #ak tabuľa[0] je prázdný
                if AI == False:
                    tabula[0] = 'X'
                elif AI == True:
                    tabula[0] = 'O'
            else: #ak neni kliknutý
                return
    
        elif event.x in range(100, 199) and event.y in range(1, 99): #tabuľa[1]
            if tabula[1] == None:
                if AI == False:
                    tabula[1] = 'X'
                elif AI == True:
                    tabula[1] = 'O'
            else:
                return
    
        elif event.x in range(200, 299) and event.y in range(1, 99): #tabuľa[2]
            if tabula[2] == None:
                if AI == False:
                    tabula[2] = 'X'
                elif AI == True:
                    tabula[2] = 'O'
            else:
                return
    
        elif event.x in range(10, 99) and event.y in range(100, 199): #tabuľa[3]
            if tabula[3] == None:
                if AI == False:
                    tabula[3] = 'X'
                elif AI == True:
                    tabula[3] = 'O'
            else:
                return
    
        elif event.x in range(100, 199) and event.y in range(100, 199): #tabuľa[4]
            if tabula[4] == None:
                if AI == False:
                    tabula[4] = 'X'
                elif AI == True:
                    tabula[4] = 'O'
            else:
                return
    
        elif event.x in range(200, 299) and event.y in range(100, 199): #tabuľa[5]
            if tabula[5] == None:
                if AI == False:
                    tabula[5] = 'X'
                elif AI == True:
                    tabula[5] = 'O'
            else:
                return
    
        elif event.x in range(1, 99) and event.y in range(200, 299): #tabuľa[6]
            if tabula[6] == None:
                if AI == False:
                    tabula[6] = 'X'
                elif AI == True:
                    tabula[6] = 'O'
            else:
                return
    
        elif event.x in range(100, 199) and event.y in range(200, 299): #tabuľa[7]
            if tabula[7] == None:
                if AI == False:
                    tabula[7] = 'X'
                elif AI == True:
                    tabula[7] = 'O'
            else:
                return
    
        elif event.x in range(200, 299) and event.y in range(200, 299): #tabuľa[8]
            if tabula[8] == None:
                if AI == False:
                    tabula[8] = 'X'
                elif AI == True:
                    tabula[8] = 'O'
            else:
                return

        kresli()
    
        #ak hra sa skončila, tak zavolá endgame()
        if skoncit(tabula):
            endgame()
            return 
    
        outcome, besttah = minimax(tabula, True)
        
        #počítačov ťah
        if AI == False:
            tabula[besttah] = 'O'
        elif AI == True:
            tabula[besttah] = 'X'
        kresli()
    
        #kontrolujem ešte raz, či už skončila hra, ak ano, tak zavolám endgame()
        if skoncit(tabula):
            endgame()
            return

    def kresli():
    
        #aktualizuje obrazovku pomocí Tkinter
        global tabula
        count = 0
        for x in range(54, 255, 100):
            for y in range(48, 249, 100):
                if tabula[count] == None:
                    symbol = ' '
                else:
                    symbol = tabula[count]
                if symbol == 'O':
                    tictactoegrid.create_text((y, x), font = ('Franklin Gothic Medium', 90), text = symbol, fill = 'red', tag='Del')
                else:
                    tictactoegrid.create_text((y, x), font = ('Franklin Gothic Medium', 90), text = symbol, fill = 'blue', tag='Del')
                count += 1
        game_screen.update()

    def endgame():
        #ukáže výhercov
        global tabula, botcounter, playercounter, tiecounter
        if vyherca(tabula) == 'O':
            if AI == False:
                messagebox.showinfo(':(', 'You lost!')
                botcounter += 1
                botwins2.config(text=str(botcounter))
            elif AI == True:
                messagebox.showinfo(':)', 'You are good') #Nikdy nevyhrá hráč, ale just in case
                playercounter += 1
                playerwins2,config(text=str(playercounter))
        elif vyherca(tabula) == 'X':
            if AI == False:
                messagebox.showinfo(':)', 'HOW?') #Nikdy
                playercounter += 1
                playerwins2,config(text=str(playercounter))
            if AI == True:
                messagebox.showinfo(':(', 'You lost :(')
                botcounter += 1
                botwins2.config(text=str(botcounter))
        else:
            messagebox.showinfo('TIE', 'It was a tie!') #pre remízu
            tiecounter += 1
            tie2.config(text=str(tiecounter))

    def restart():
        
        #restartuje celú hru, každé políčko zase dostane None
        global tabula, AI

        tabula = [None] * 9

        tictactoegrid.delete('Del') #odstráni všetky políčka

        if AI == False:
            ai() #zavolám ai() v ktorej predám začiatok počítačovi
        elif AI == True:
            AI = False
            kresli()

    #setup pre Tkinter
    game_screen = Tk()
    game_screen.configure(background='#1E7B86')
    game_screen.title('TicTacToe')
    game_screen.geometry('400x420')

    reset = Button(game_screen, text='Next round', command=restart, background='#FF6666', font = ('System', 10), activebackground="#00FF00") #the next round button
    reset.place(x = 114, y = 67)

    exit = Button(game_screen, text='Exit', command=game_screen.destroy, background='#FF6666', font = ('System', 10), activebackground="#00FF00")
    exit.place(x = 235, y = 67)
    
    #spočíta koľko krát vyhral počítač
    botwins1 = Label(game_screen, text='botwins: ', background='#1E7B86', font = ('System', 10)) 
    botwins2 = Label(game_screen, text=str(botcounter), background='#1E7B86', font = ('System', 10)) 
    
    #spočíta koľko krát vyhral hráč
    playerwins1 = Label(game_screen, text='playerwins: ', background='#1E7B86', font = ('System', 10))
    playerwins2 = Label(game_screen, text=str(playercounter), background='#1E7B86', font = ('System', 10))

    #spočíta remíz
    tie1 = Label(game_screen, text='ties: ', background='#1E7B86', font = ('System', 10))
    tie2 = Label(game_screen, text=str(tiecounter), background='#1E7B86', font = ('System', 10)) 

    #miesto Labelov
    botwins1.place(x = 80, y = 10)
    botwins2.place(x = 95, y = 40)
    playerwins1.place(x = 170, y = 10)
    playerwins2.place(x = 195, y = 40)
    tie1.place(x = 290, y = 10)
    tie2.place(x = 295, y = 40)

    #na canvas ide obrazovka Tic-Tac-Toe
    tictactoegrid = Canvas(game_screen, width=300, height=300, background='#FFFF66')
    tictactoegrid.bind('<Button-1>', update)
    tictactoegrid.create_line(0, 100, 300, 100, width = 1)
    tictactoegrid.create_line(0, 200, 300, 200, width = 1)
    tictactoegrid.create_line(100, 0, 100, 300, width = 1)
    tictactoegrid.create_line(200, 0, 200, 300, width = 1)

    tictactoegrid.place(x = 50, y = 100)
    game_screen.mainloop()

menu = Tk()
menu.title('MENU')
menu.geometry('400x420')
menu.configure(background = '#1E7B86')
credit = Label(menu, text='Made by Horváth Norbert', background='#1E7B86', font = ('Sy stem', 2))
button = Button(menu, text='Play', command = gameobrazovka, background='#FF6666', foreground = '#000033', font = ('System', 30), activebackground="#00FF00")
buttonexit = Button(menu, text='Exit', command = menu.destroy, background='#FF6666', foreground = '#000033', font = ('System', 30), activebackground="#00FF00")

credit.place(x = 230, y = 400)
button.place(x = 135, y = 50)
buttonexit.place(x = 140, y = 190)
mainloop()

