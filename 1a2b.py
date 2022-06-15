import tkinter as tk
import random
from tkinter import messagebox


class Windows(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('終極密碼')
        self.geometry('500x400+300+200')
        self.resizable(0, 0)

        self.guess_count = 0  # 猜的次數累計

        # ----- 建立左邊Frame START-----
        self.LeftFrame = tk.Frame(self, bg='pink')

        self.scrollbar = tk.Scrollbar(self.LeftFrame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ----- 紀錄猜的次數、以及猜的結果 -----
        self.listbox = tk.Listbox(self.LeftFrame, bg='pink', width=25, height=20, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview_moveto(1))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.LeftFrame.pack(side=tk.LEFT, padx=5, pady=5)
        # ----- 建立左邊Frame END-----


        # ----- 建立右邊Frame START-----
        self.RightFrame = tk.Frame(self, bg='lightgray')

        # ----- 輸入及顯示要猜的數字 -----
        self.Frame1 = tk.Frame(self.RightFrame, bg='lightgray')
        self.TitleLabel = tk.Label(self.Frame1, text='請輸入要猜的4位數字', bg='lightgray', font=('arial', 14), fg='blue')
        self.TitleLabel.grid(row=0, column=0, padx=10, pady=5)

        self.numEntry = tk.Entry(self.Frame1, justify='center', font=('arial', 16))
        self.numEntry.grid(row=1, column=0, padx=8, sticky='e')
        self.Frame1.pack(padx=10, pady=10)

        # ----- 功能按鈕設置(開始、送出) -----
        self.Frame2 = tk.Frame(self.RightFrame, bg='lightgray')
        self.startButton = tk.Button(self.Frame2, text='開始', width=7, font=('arial', 16), command=self.GoalNum)
        self.startButton.grid(row=0, column=0, pady=10)

        self.updateButton = tk.Button(self.Frame2, text='送出', width=7, font=('arial', 16), command=self.Check, state='disable')
        self.updateButton.grid(row=0, column=1, padx=5, pady=10)
        self.Frame2.pack(padx=10, pady=10)

        # ----- 功能按鈕設置(結束、提示) -----
        self.Frame3 = tk.Frame(self.RightFrame, bg='lightgray')
        self.endButton = tk.Button(self.Frame3, text='結束', width=7, font=('arial', 16), command=self.GameOver)
        self.endButton.grid(row=0, column=0, pady=10)

        self.tipButton = tk.Button(self.Frame3, text='提示', width=7, font=('arial', 16), command=self.Tips)
        self.tipButton.grid(row=0, column=1, padx=5, pady=10)
        self.Frame3.pack()

        # ----- 規則說明欄 -----
        self.Frame4 = tk.Frame(self.RightFrame)
        self.text = '1.按下開始鍵，即會自動出題 \n\n2.按下送出，即可開始猜測，結果會顯示在左邊 \n\n3.按下提示，可知道其中一個數字(只能用一次)\n\n4.按下結束，可知道答案並選擇是否重來'
        self.textlabel = tk.Label(self.Frame4, text=self.text, bg='lightyellow', justify='left')
        self.textlabel.pack()
        self.Frame4.pack(pady=20)

        self.RightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        # ----- 建立右邊Frame END-----

    # ----- 函式區 START -----
    def GoalNum(self):  # 謎底數字設置
        self.listbox.delete(0, 'end')
        self.tipButton.config(state='normal')
        self.updateButton.config(state='normal')
        self.startButton.config(text='開始')
        self.listbox.insert('end', '請輸入數字後，按下送出開始')
        self.guess_count = 0
        self.listbox.insert('end', f'目前已猜 {self.guess_count} 次')
        self.numEntry.delete(0, 'end')
        self.Numlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.Numset = random.sample(self.Numlist, 4)

    def Check(self):  # 輸入的數字與謎底數字比對，並輸出結果

        self.A_count = 0
        self.B_count = 0
        self.numEntrylist = []

        if self.numEntry.get() != '' and self.numEntry.get().isdigit() is True:
            if len(self.numEntry.get()) != 4:
                messagebox.showwarning('結果', '請確認是否輸入4個數字')
                return
            else:
                for i in range(4):
                    self.numEntrylist.append(int(self.numEntry.get()[i]))
                    self.startButton.config(state='disable')
        else:
            messagebox.showwarning('結果', '請確認是否有輸入非數字文字')
            return

        if self.Numset == self.numEntrylist:
            self.guess_count += 1
            self.listbox.delete(1)
            self.listbox.insert(1, f'目前已猜 {self.guess_count} 次')
            self.listbox.insert('end', f'{self.numEntry.get()}        --->        4A0B')
            self.listbox.insert('end', '如果要繼續遊戲，請按刷新')
            messagebox.showinfo('遊戲結束', '恭喜您答對了')
            self.startButton.config(state='normal')
            self.startButton.config(text='刷新')
            self.updateButton.config(state='disable')
        else:
            self.guess_count += 1
            for i in range(4):
                if self.numEntrylist[i] in self.Numset:
                    if self.numEntrylist[i] == self.Numset[i]:
                        self.A_count += 1
                    else:
                        self.B_count += 1
            self.listbox.insert('end', f'{self.numEntry.get()}        --->        {self.A_count}A{self.B_count}B')

        self.listbox.delete(1)
        self.listbox.insert(1, f'目前已猜 {self.guess_count} 次')
        self.numEntry.delete(0, 'end')

    def GameOver(self):  # 按下結束按鈕後的動作判定
        message = messagebox.askyesno('是否放棄', '真的不想努力了嗎?')
        if message is True:
            try:
                self.num = ''
                for number in self.Numset:
                    self.num += '%s' %(number)
                self.listbox.insert('end', f'遊戲結束，終極密碼是 {self.num}')
                self.listbox.insert('end', '如果要繼續遊戲，請按刷新')
            except:
                messagebox.showerror('結果', '要先按「開始」指定一組終極密碼喔!')
                return

            self.tipButton.config(state='normal')
            self.startButton.config(state='normal')
            self.updateButton.config(state='disable')
            self.guess_count = 0

            try:
                if self.Numset is not None:
                    self.startButton.config(text='刷新')
            except:
                return
        else:
            return

    def Tips(self):  # 按下提示按鈕的動作
        try:
            messagebox.showinfo('提示', f'其中一個數字為 {random.choice(self.Numset)}')
            self.tipButton.config(state='disable')
        except:
            messagebox.showerror('結果', '要先按「開始」指定一組終極密碼喔!')

    # ----- 函式區 END -----

if __name__ == '__main__':
    window = Windows()
    window.mainloop()