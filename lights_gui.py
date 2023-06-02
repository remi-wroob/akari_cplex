import tkinter as tk

def create_board(n):
    board = []
    for _ in range(n):
        row = [0] * n
        board.append(row)
    return board

def button_click(row, col):
    if board[row][col] == 0:
        board[row][col] = 1
        buttons[row][col].configure(bg='black', activebackground='gray25')
    elif board[row][col] == 1:
        board[row][col] = '0'
        buttons[row][col].configure(text='0')
    elif board[row][col] == '4':
        board[row][col] = 0
        buttons[row][col].configure(text='', bg='white', activebackground='gray75')
    elif type(board[row][col]) == str:
        temp = str(int(board[row][col])+1)
        board[row][col] = temp
        buttons[row][col].configure(text=temp)

def save_board():
    print("Zapisywanie planszy:")
    for row in board:
        print(row)

    print('\n\n\n')

    eksport(board)

def create_gui(n):
    root = tk.Tk()
    root.title("Plansza z przyciskami")

    global board
    board = create_board(n)

    global buttons
    buttons = []

    for row in range(n):
        button_row = []
        for col in range(n):
            button = tk.Button(root, text='', width=2, height=1, bg='white', activebackground='gray75', fg='white',
                               activeforeground='white', bd=1, command=lambda r=row, c=col: button_click(r, c))
            button.grid(row=row, column=col)
            button_row.append(button)
        buttons.append(button_row)

    save_button = tk.Button(root, text="Zapisz", command=save_board)
    save_button.grid(row=n, columnspan=n)

    root.mainloop()


def list_to_cplex(list):
    t_list = ''
    for i in range(len(list)):
        t_list += '{'
        for j in range(len(list[i])):
            t_list += str(list[i][j])
            if j <= len(list[i]) - 2:
                t_list += ', '
        t_list += '}'
        if i <= len(list) - 2:
            t_list += ', '
    return t_list


def zapisz_do_pliku(zmienna_tekstowa, nazwa_pliku):
    with open(nazwa_pliku, 'w') as plik:
        plik.write(zmienna_tekstowa)


def eksport(board):
    meta_plansza = []
    n = len(board)
    sc = 0
    sc_i = 0
    # kol = 0
    # wie = 0
    rozmiar2 = n ** 2
    ilosc_scian = 0
    for i in board:
        for j in i:
            if j != 0:
                ilosc_scian += 1
    polaczenia = [[0 for _ in range(rozmiar2)] for _ in range(rozmiar2)]
    ogr_sc_war = []
    ogr_sc_idx = []
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                meta_plansza.append(0)
                polaczenia[(i*n)+j][(i*n)+j] = 1
                try:
                    k = 1
                    while board[i][j+k] == 0:
                        polaczenia[(i*n)+j][(i*n)+j+k] = 1
                        k += 1
                except IndexError:
                    pass
                try:
                    k = 1
                    while board[i][j-k] == 0 and j - k >= 0:
                        polaczenia[(i*n)+j][(i*n)+j-k] = 1
                        k += 1
                except IndexError:
                    pass
                try:
                    k = 1
                    while board[i+k][j] == 0:
                        polaczenia[(i*n)+j][((i + k) * n) + j] = 1
                        k += 1
                except IndexError:
                    pass
                try:
                    k = 1
                    while board[i-k][j] == 0 and i - k >= 0:
                        polaczenia[(i*n)+j][((i - k) * n) + j] = 1
                        k += 1
                except IndexError:
                    pass


            else:
                meta_plansza.append('sciana')
                sc += 1
                if board[i][j] != 1:
                    sc_i += 1
                    ogr_sc_war.append(int(board[i][j]))
                    temp = []
                    if i + 1 <= n - 1 and board[i+1][j] == 0:
                        # temp.append(board[i+1][j])
                        temp.append(((i + 1) * n) + j + 1)
                    if j + 1 <= n - 1 and board[i][j+1] == 0:
                        # temp.append(board[i][j+1])
                        temp.append((i * n) + j + 2)
                    if i - 1 >= 0 and board[i-1][j] == 0:
                        # temp.append(board[i-1][j])
                        temp.append(((i - 1) * n) + j + 1)
                    if j - 1 >= 0 and board[i][j-1] == 0:
                        # temp.append(board[i][j-1])
                        temp.append((i * n) + j)

                    ogr_sc_idx.append(temp)


        kolumny = []
        wiersze = []
        for i in range(n):
            temp = []
            for j in range(n):
                if board[i][j] == 0:
                    temp.append((i*n)+j+1)
                else:
                    wiersze.append(temp)
                    temp = []
                if j == n - 1:
                    wiersze.append(temp)
        for j in range(n):
            temp = []
            for i in range(n):
                if board[i][j] == 0:
                    temp.append((i*n)+j+1)
                else:
                    kolumny.append(temp)
                    temp = []
                if i == n - 1:
                    kolumny.append(temp)

        while [] in kolumny:
            kolumny.remove([])

        while [] in wiersze:
            wiersze.remove([])


    # print(polaczenia)
    # print(wiersze)
    # print(kolumny)
    # print(meta_plansza)
    # print(ogr_sc_idx)
    # print(ogr_sc_war)

    t_ogr_sc_idx = list_to_cplex(ogr_sc_idx)
    t_kolumny = list_to_cplex(kolumny)
    t_wiersze = list_to_cplex(wiersze)
    # print(t_ogr_sc_idx)
    # print(t_kolumny)
    # print(t_wiersze)

    cplex = f'range sc = 1..{sc_i};\n{{int}} ogr_sc_idx[sc] = [{t_ogr_sc_idx}];\nint ogr_sc_war[sc] = {ogr_sc_war};\n\n\n\n' \
            f'range kol = 1..{len(kolumny)};\n{{int}} kolumny[kol] = [{t_kolumny}];\nrange wie = 1..{len(wiersze)};\n{{int}} wiersze[wie] = [{t_wiersze}];\n\n\n\n' \
            f'range n2 = 1..{n**2};\nint rozmiar2 = {n**2};\nint ilosc_scian = {sc};\nint polaczenia[n2][n2] = {polaczenia};'
    # print(cplex)

    meta = f'polaczenia = {polaczenia}\nwiersze = {wiersze}\nkolumny = {kolumny}\npusta_plansza = {meta_plansza}\nogr_sc_war = {ogr_sc_war}\nogr_sc_idx = {ogr_sc_idx}'
    #print(meta)


    zapisz_do_pliku(cplex, 'cplex.txt')
    zapisz_do_pliku(meta, 'meta.txt')












n = int(input("Podaj rozmiar planszy: "))
create_gui(n)
