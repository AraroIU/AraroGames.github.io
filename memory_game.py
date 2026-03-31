import tkinter as tk
from tkinter import messagebox
import random
import time

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("เกมส์ฝึกความจำ")
        self.root.geometry("600x700")
        self.root.configure(bg="#2c3e50")
        
        self.game_mode = None
        self.score = 0
        self.best_score = 0
        self.game_active = False
        
        self.show_main_menu()
    
    def show_main_menu(self):
        """เมนูหลัก"""
        self.clear_frame()
        
        title = tk.Label(
            self.root,
            text="🧠 เกมส์ฝึกความจำ",
            font=("Arial", 28, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        title.pack(pady=30)
        
        subtitle = tk.Label(
            self.root,
            text="เลือกเกมส์ที่คุณต้องการ",
            font=("Arial", 14),
            fg="#bdc3c7",
            bg="#2c3e50"
        )
        subtitle.pack(pady=10)
        
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(pady=20)
        
        btn_sequence = tk.Button(
            button_frame,
            text="1. จำลำดับตัวเลข",
            command=lambda: self.start_sequence_game(),
            width=25,
            height=2,
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2"
        )
        btn_sequence.pack(pady=10)
        
        btn_matching = tk.Button(
            button_frame,
            text="2. จับคู่ตัวเลข",
            command=lambda: self.start_matching_game(),
            width=25,
            height=2,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2"
        )
        btn_matching.pack(pady=10)
        
        btn_color = tk.Button(
            button_frame,
            text="3. จำสี",
            command=lambda: self.start_color_game(),
            width=25,
            height=2,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2"
        )
        btn_color.pack(pady=10)
        
        info_label = tk.Label(
            self.root,
            text=f"สูงสุด: {self.best_score}",
            font=("Arial", 12),
            fg="#f39c12",
            bg="#2c3e50"
        )
        info_label.pack(pady=20)
    
    def clear_frame(self):
        """ล้างหน้าจอ"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ============ เกมส์ที่ 1: จำลำดับตัวเลข ============
    def start_sequence_game(self):
        """เริ่มเกมส์ลำดับตัวเลข"""
        self.clear_frame()
        self.game_mode = "sequence"
        self.sequence = []
        self.player_sequence = []
        self.round_num = 0
        self.show_sequence_game()
    
    def show_sequence_game(self):
        """แสดงหน้าจอเกมส์ลำดับ"""
        title = tk.Label(
            self.root,
            text="จำลำดับตัวเลข",
            font=("Arial", 24, "bold"),
            fg="#3498db",
            bg="#2c3e50"
        )
        title.pack(pady=20)
        
        info = tk.Label(
            self.root,
            text=f"รอบที่: {self.round_num} | คะแนน: {self.score}",
            font=("Arial", 14),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        info.pack()
        
        self.display_label = tk.Label(
            self.root,
            text="กำลังโหลด...",
            font=("Arial", 32, "bold"),
            fg="#2ecc71",
            bg="#34495e",
            width=15,
            height=3
        )
        self.display_label.pack(pady=20)
        
        instructions = tk.Label(
            self.root,
            text="จำลำดับตัวเลขที่ปรากฏ แล้วกดปุ่มเดียวกัน",
            font=("Arial", 11),
            fg="#bdc3c7",
            bg="#2c3e50"
        )
        instructions.pack()
        
        # ปุ่มตัวเลข
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(pady=30)
        
        self.sequence_buttons = {}
        buttons = [
            (1, "#e74c3c", 0, 0), (2, "#f39c12", 0, 1),
            (3, "#2ecc71", 1, 0), (4, "#3498db", 1, 1)
        ]
        
        for num, color, row, col in buttons:
            btn = tk.Button(
                button_frame,
                text=str(num),
                font=("Arial", 18, "bold"),
                width=8,
                height=3,
                bg=color,
                fg="white",
                command=lambda n=num: self.player_press_sequence(n),
                cursor="hand2"
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.sequence_buttons[num] = btn
        
        start_btn = tk.Button(
            self.root,
            text="เริ่มเกมส์",
            width=20,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.next_sequence_round,
            cursor="hand2"
        )
        start_btn.pack(pady=20)
        
        back_btn = tk.Button(
            self.root,
            text="กลับหน้าแรก",
            width=20,
            bg="#7f8c8d",
            fg="white",
            font=("Arial", 10),
            command=self.show_main_menu,
            cursor="hand2"
        )
        back_btn.pack()
    
    def next_sequence_round(self):
        """เพิ่มตัวเลขใหม่ลงในลำดับ"""
        self.round_num += 1
        self.player_sequence = []
        self.sequence.append(random.randint(1, 4))
        self.show_sequence()
    
    def show_sequence(self):
        """แสดงลำดับตัวเลข"""
        for btn in self.sequence_buttons.values():
            btn.config(state="disabled")
        
        self.display_label.config(text="ดูลำดับ")
        self.root.after(1000, self.animate_sequence, 0)
    
    def animate_sequence(self, index):
        """ทำให้ลำดับเรียงกัน"""
        if index < len(self.sequence):
            num = self.sequence[index]
            btn = self.sequence_buttons[num]
            btn.config(bg="white")
            self.display_label.config(text=str(num))
            self.root.after(400, lambda: btn.config(bg=self.get_button_color(num)))
            self.root.after(600, lambda: self.animate_sequence(index + 1))
        else:
            self.display_label.config(text="ถึงเทิร์นของคุณ!")
            for btn in self.sequence_buttons.values():
                btn.config(state="normal")
    
    def get_button_color(self, num):
        """ได้สีของปุ่ม"""
        colors = {1: "#e74c3c", 2: "#f39c12", 3: "#2ecc71", 4: "#3498db"}
        return colors[num]
    
    def player_press_sequence(self, num):
        """ผู้เล่นกดปุ่ม"""
        self.player_sequence.append(num)
        
        # ตรวจสอบระดับ
        if self.player_sequence[-1] != self.sequence[len(self.player_sequence) - 1]:
            self.game_over_sequence()
            return
        
        # ครบตามลำดับแล้ว
        if len(self.player_sequence) == len(self.sequence):
            self.score += self.round_num * 10
            self.display_label.config(text="✓ ถูกต้อง!")
            for btn in self.sequence_buttons.values():
                btn.config(state="disabled")
            self.root.after(1500, self.next_sequence_round)
    
    def game_over_sequence(self):
        """จบเกมส์ลำดับ"""
        if self.score > self.best_score:
            self.best_score = self.score
        
        messagebox.showinfo(
            "เสร็จสิ้น",
            f"เกมส์จบ!\n\nรอบ: {self.round_num}\nคะแนน: {self.score}\nสูงสุด: {self.best_score}"
        )
        self.score = 0
        self.show_main_menu()
    
    # ============ เกมส์ที่ 2: จับคู่ตัวเลข ============
    def start_matching_game(self):
        """เริ่มเกมส์จับคู่"""
        self.clear_frame()
        self.game_mode = "matching"
        self.cards = []
        self.flipped = [None, None]
        self.matched = 0
        self.attempts = 0
        
        numbers = list(range(1, 9)) * 2
        random.shuffle(numbers)
        self.cards = numbers
        
        self.show_matching_game()
    
    def show_matching_game(self):
        """แสดงเกมส์จับคู่"""
        title = tk.Label(
            self.root,
            text="จับคู่ตัวเลข",
            font=("Arial", 24, "bold"),
            fg="#9b59b6",
            bg="#2c3e50"
        )
        title.pack(pady=20)
        
        info = tk.Label(
            self.root,
            text=f"จับคู่: {self.matched}/8 | พยายาม: {self.attempts}",
            font=("Arial", 14),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        info.pack()
        
        card_frame = tk.Frame(self.root, bg="#2c3e50")
        card_frame.pack(pady=20)
        
        self.card_buttons = {}
        for i in range(16):
            btn = tk.Button(
                card_frame,
                text="?",
                font=("Arial", 16, "bold"),
                width=6,
                height=3,
                bg="#34495e",
                fg="white",
                command=lambda idx=i: self.flip_card(idx),
                cursor="hand2"
            )
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.card_buttons[i] = {"btn": btn, "flipped": False}
        
        back_btn = tk.Button(
            self.root,
            text="กลับหน้าแรก",
            width=20,
            bg="#7f8c8d",
            fg="white",
            font=("Arial", 10),
            command=self.show_main_menu,
            cursor="hand2"
        )
        back_btn.pack(pady=20)
    
    def flip_card(self, index):
        """พลิกการ์ด"""
        if self.card_buttons[index]["flipped"]:
            return
        
        btn = self.card_buttons[index]["btn"]
        btn.config(text=str(self.cards[index]), bg="#3498db")
        self.card_buttons[index]["flipped"] = True
        
        if self.flipped[0] is None:
            self.flipped[0] = index
        elif self.flipped[1] is None:
            self.flipped[1] = index
            self.attempts += 1
            
            if self.cards[self.flipped[0]] == self.cards[self.flipped[1]]:
                self.matched += 1
                self.flipped = [None, None]
                
                if self.matched == 8:
                    messagebox.showinfo(
                        "ชนะ!",
                        f"ยินดีด้วย!\n\nพยายาม: {self.attempts}\nคะแนน: {(100 - self.attempts * 5)}"
                    )
                    self.show_main_menu()
            else:
                self.root.after(1000, self.unflip_cards)
    
    def unflip_cards(self):
        """พลิกการ์ดกลับ"""
        if self.flipped[0] is not None:
            self.card_buttons[self.flipped[0]]["btn"].config(text="?", bg="#34495e")
            self.card_buttons[self.flipped[0]]["flipped"] = False
        
        if self.flipped[1] is not None:
            self.card_buttons[self.flipped[1]]["btn"].config(text="?", bg="#34495e")
            self.card_buttons[self.flipped[1]]["flipped"] = False
        
        self.flipped = [None, None]
    
    # ============ เกมส์ที่ 3: จำสี ============
    def start_color_game(self):
        """เริ่มเกมส์จำสี"""
        self.clear_frame()
        self.game_mode = "color"
        self.color_sequence = []
        self.player_color_sequence = []
        self.round_num = 0
        self.show_color_game()
    
    def show_color_game(self):
        """แสดงเกมส์จำสี"""
        title = tk.Label(
            self.root,
            text="จำสี",
            font=("Arial", 24, "bold"),
            fg="#e74c3c",
            bg="#2c3e50"
        )
        title.pack(pady=20)
        
        info = tk.Label(
            self.root,
            text=f"รอบที่: {self.round_num} | คะแนน: {self.score}",
            font=("Arial", 14),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        info.pack()
        
        self.color_display = tk.Label(
            self.root,
            text="สีแสดง",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#95a5a6",
            width=15,
            height=4
        )
        self.color_display.pack(pady=20)
        
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(pady=20)
        
        colors = [
            ("แดง", "#e74c3c"), ("เหลือง", "#f39c12"),
            ("เขียว", "#2ecc71"), ("ฟ้า", "#3498db")
        ]
        
        self.color_buttons = {}
        for i, (name, color) in enumerate(colors):
            btn = tk.Button(
                button_frame,
                text=name,
                font=("Arial", 14, "bold"),
                width=10,
                bg=color,
                fg="white",
                command=lambda c=color: self.player_choose_color(c),
                cursor="hand2"
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
            self.color_buttons[color] = btn
        
        start_btn = tk.Button(
            self.root,
            text="เริ่มเกมส์",
            width=20,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.next_color_round,
            cursor="hand2"
        )
        start_btn.pack(pady=20)
        
        back_btn = tk.Button(
            self.root,
            text="กลับหน้าแรก",
            width=20,
            bg="#7f8c8d",
            fg="white",
            font=("Arial", 10),
            command=self.show_main_menu,
            cursor="hand2"
        )
        back_btn.pack()
    
    def next_color_round(self):
        """รอบสีใหม่"""
        self.round_num += 1
        self.player_color_sequence = []
        colors = ["#e74c3c", "#f39c12", "#2ecc71", "#3498db"]
        self.color_sequence.append(random.choice(colors))
        self.show_color_sequence()
    
    def show_color_sequence(self):
        """แสดงลำดับสี"""
        for btn in self.color_buttons.values():
            btn.config(state="disabled")
        
        self.root.after(1000, self.animate_color_sequence, 0)
    
    def animate_color_sequence(self, index):
        """ทำให้ลำดับสีเรียงกัน"""
        if index < len(self.color_sequence):
            color = self.color_sequence[index]
            self.color_display.config(bg=color)
            self.root.after(600, lambda: self.color_display.config(bg="#95a5a6"))
            self.root.after(800, lambda: self.animate_color_sequence(index + 1))
        else:
            for btn in self.color_buttons.values():
                btn.config(state="normal")
    
    def player_choose_color(self, color):
        """ผู้เล่นเลือกสี"""
        self.player_color_sequence.append(color)
        self.color_display.config(bg=color)
        
        if self.player_color_sequence[-1] != self.color_sequence[len(self.player_color_sequence) - 1]:
            self.color_display.config(bg="#c0392b")
            self.game_over_color()
            return
        
        if len(self.player_color_sequence) == len(self.color_sequence):
            self.score += self.round_num * 15
            self.color_display.config(bg="#27ae60")
            for btn in self.color_buttons.values():
                btn.config(state="disabled")
            self.root.after(1500, self.next_color_round)
    
    def game_over_color(self):
        """จบเกมส์สี"""
        if self.score > self.best_score:
            self.best_score = self.score
        
        messagebox.showinfo(
            "เสร็จสิ้น",
            f"เกมส์จบ!\n\nรอบ: {self.round_num}\nคะแนน: {self.score}\nสูงสุด: {self.best_score}"
        )
        self.score = 0
        self.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
