import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3
import random
import pyttsx3  
import os
from datetime import datetime

class HotelAG:
    def __init__(self, root):
        self.root = root
        self.root.title("HOTEL AG MANAGEMENT SYSTEM")
        self.root.state('zoomed') 
        
        self.engine = pyttsx3.init()
        self.init_db()
        self.main_menu()
        self.speak("Welcome to A G Hotel")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def init_db(self):
        conn = sqlite3.connect('hotel_records.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cust_id INTEGER,
            name TEXT, phno TEXT, address TEXT,
            checkin TEXT, checkout TEXT, room_type TEXT,
            room_no INTEGER, room_price REAL, 
            restaurant_bill REAL, status TEXT)''')
        conn.commit()
        conn.close()

    def main_menu(self):
        for widget in self.root.winfo_children(): widget.destroy()
        m_frame = tk.Frame(self.root)
        m_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(m_frame, text="WELCOME TO HOTEL AG", font=("Arial", 40, "bold"), pady=40).pack()
        btns = [("1 Booking", self.Booking_UI), ("2 Rooms Info", self.Rooms_Info_UI), 
                ("3 Room Service (Menu Card)", self.Restaurant_UI), ("4 Payment & Bill", self.Payment_UI), 
                ("5 Record (Database)", self.Record_UI), ("0 Exit", self.root.quit)]
        for text, command in btns:
            tk.Button(m_frame, text=text, font=("Arial", 16), width=40, height=2, command=command).pack(pady=10)

    def Restaurant_UI(self):
        win = tk.Toplevel(self.root); win.state('zoomed')
        canvas = tk.Canvas(win); sb = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        sf = ttk.Frame(canvas); sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((win.winfo_screenwidth()//2, 0), window=sf, anchor="n")
        
        tk.Label(sf, text="MENU CARD", font=("Arial", 30, "bold"), fg="red", pady=20).pack()
        tk.Label(sf, text="Enter Cust ID:").pack(); cid_e = tk.Entry(sf, font=("Arial", 14)); cid_e.pack(pady=10)

        menu = {
            "BEVERAGES": {"Regular Tea": 80, "Masala Tea": 90, "Coffee": 90, "Cold Drinks": 140, "Bread Butter": 90, "Bread Jam": 80},
            "SOUPS": {"Tomato Soup": 110, "Hot & Sour": 110, "Veg Munchow": 110, "Sweet Corn": 110},
            "MAIN COURSE": {"Shahi Paneer": 450, "Kadai Paneer": 400, "Handi Paneer": 500, "Palak Paneer": 400, "Mix Veg": 350, "Jeera Aloo": 300},
            "ROTI/DAL": {"Dal Fry": 200, "Dal Makhani": 220, "Plain Roti": 20, "Butter Roti": 25, "Butter Naan": 40},
            "SOUTH INDIAN": {"Plain Dosa": 60, "Onion Dosa": 70, "Masala Dosa": 70, "Paneer Dosa": 90, "Rice Idli": 40, "Sambhar Vada": 30},
            "ICE CREAM": {"Vanilla": 60, "Strawberry": 80, "Pineapple": 70, "Butter Scotch": 90}
        }

        vars = {}
        for cat, items in menu.items():
            tk.Label(sf, text=cat, font=("Arial", 15, "bold"), fg="blue", pady=10).pack(anchor="w")
            for itm, prc in items.items():
                fr = tk.Frame(sf); fr.pack(fill="x", padx=50)
                v, q = tk.IntVar(), tk.IntVar(value=1)
                tk.Checkbutton(fr, text=f"{itm} - Rs.{prc}", variable=v, font=("Arial", 12)).pack(side="left")
                tk.Spinbox(fr, from_=1, to=10, width=5, textvariable=q).pack(side="left", padx=10)
                vars[itm] = (v, q, prc)

        def order():
            tot = sum(v.get() * q.get() * p for v, q, p in vars.values())
            conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
            c.execute("UPDATE guests SET restaurant_bill = restaurant_bill + ? WHERE cust_id = ?", (tot, cid_e.get()))
            conn.commit(); conn.close(); win.destroy()
        tk.Button(sf, text="Confirm Order", font=("Arial", 14), bg="blue", fg="white", command=order).pack(pady=30)
        canvas.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

    def Record_UI(self):
        win = tk.Toplevel(self.root); win.state('zoomed')
        sf = tk.Frame(win); sf.pack(pady=10); sv = tk.StringVar()
        tk.Label(sf, text="Search: ").pack(side="left"); tk.Entry(sf, textvariable=sv, width=40).pack(side="left")
        
        cols = ("Cust ID", "Name", "Phone", "CheckIn", "CheckOut", "Room", "RoomNo", "Bill", "Status")
        tree = ttk.Treeview(win, columns=cols, show='headings')
        for col in cols: tree.heading(col, text=col); tree.column(col, anchor="center")
        tree.pack(expand=True, fill='both', padx=20)

        def load(q=""):
            for i in tree.get_children(): tree.delete(i)
            conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
            c.execute("SELECT cust_id, name, phno, checkin, checkout, room_type, room_no, (room_price + restaurant_bill), status FROM guests WHERE name LIKE ? OR phno LIKE ?", (f'%{q}%', f'%{q}%'))
            for r in c.fetchall(): tree.insert("", tk.END, values=r)
            conn.close()
        sv.trace("w", lambda *a: load(sv.get())); load()

        def delete():
            s = tree.selection()
            if s:
                conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
                c.execute("DELETE FROM guests WHERE cust_id=?", (tree.item(s[0])['values'][0],))
                conn.commit(); conn.close(); load()

        def edit():
            s = tree.selection()
            if not s: return
            cid = tree.item(s[0])['values'][0]
            conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
            c.execute("SELECT name, phno FROM guests WHERE cust_id=?", (cid,))
            current = c.fetchone()
            ew = tk.Toplevel(win); ew.title("Edit Record"); ew.geometry("300x250")
            tk.Label(ew, text="New Name:").pack(pady=5)
            en = tk.Entry(ew); en.insert(0, current[0]); en.pack()
            tk.Label(ew, text="New Number:").pack(pady=5)
            ep = tk.Entry(ew); ep.insert(0, current[1]); ep.pack()
            def up():
                c.execute("UPDATE guests SET name=?, phno=? WHERE cust_id=?", (en.get(), ep.get(), cid))
                conn.commit(); conn.close(); ew.destroy(); load()
            tk.Button(ew, text="Update", bg="blue", fg="white", command=up).pack(pady=20)

        bf = tk.Frame(win); bf.pack(pady=10)
        tk.Button(bf, text="Edit Selected", bg="blue", fg="white", command=edit).pack(side="left", padx=10)
        tk.Button(bf, text="Delete Selected", bg="red", fg="white", command=delete).pack(side="left", padx=10)

    # --- IMPROVED PHYSICAL RECEIPT FORMAT ---
    def Payment_UI(self):
        win = tk.Toplevel(self.root); win.state('zoomed')
        f = tk.Frame(win); f.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(f, text="PAYMENT", font=("Arial", 30, "bold")).pack(pady=20)
        e = tk.Entry(f, font=("Arial", 14), width=30); e.pack(pady=10)
        def pay():
            conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
            c.execute("SELECT name, room_price, restaurant_bill, cust_id, room_no, room_type, checkin, checkout, phno FROM guests WHERE phno=? AND status='Unpaid'", (e.get(),))
            res = c.fetchone()
            if res and messagebox.askyesno("Pay", f"Total Amount: Rs. {res[1]+res[2]}"):
                c.execute("UPDATE guests SET status='Paid' WHERE phno=?", (e.get(),))
                conn.commit()
                if messagebox.askyesno("Receipt", "Print Receipt?"):
                    fn = f"Bill_ID_{res[3]}.txt"
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(fn, "w") as f_f:
                        f_f.write(f"==============================\n")
                        f_f.write(f"         HOTEL AG\n")
                        f_f.write(f"==============================\n")
                        f_f.write(f"Date: {now}\n")
                        f_f.write(f"Cust ID: {res[3]}\n")
                        f_f.write(f"Guest  : {res[0]}\n")
                        f_f.write(f"Phone  : {res[8]}\n")
                        f_f.write(f"------------------------------\n")
                        f_f.write(f"Room No: {res[4]} ({res[5]})\n")
                        f_f.write(f"Check-In: {res[6]}\n")
                        f_f.write(f"------------------------------\n")
                        f_f.write(f"Room Rent:   Rs. {res[1]}\n")
                        f_f.write(f"Food Bill:   Rs. {res[2]}\n")
                        f_f.write(f"------------------------------\n")
                        f_f.write(f"TOTAL PAID:  Rs. {res[1]+res[2]}\n")
                        f_f.write(f"==============================\n")
                        f_f.write(f"  Thank you for visiting!\n")
                        f_f.write(f"==============================\n")
                    os.startfile(fn)
                win.destroy()
            conn.close()
        tk.Button(f, text="Pay & Print", font=("Arial", 14), bg="green", fg="white", command=pay).pack(pady=20)

    def Booking_UI(self):
        win = tk.Toplevel(self.root); win.state('zoomed')
        f = tk.Frame(win); f.place(relx=0.5, rely=0.5, anchor="center")
        self.r_d = {"Standard Non-AC": (5000,"Price:5000-> 1 Double Bed, Television, Telephone,Double-Door Cupboard, 1 Coffee table with 2 sofa, Balcony and an attached washroom with hot/cold water.\n"),
                    "Standard AC": (8000,"Price:8000->1 Double Bed, Television, Telephone, Double-Door Cupboard, 1 Coffee table with 2 sofa, Balcony and an attached washroom with hot/cold water + Window/Split AC.\n"),
                    "3-Bed Non-AC": (11000,"Price:11000->1 Double Bed + 1 Single Bed, Television, Telephone, a Triple-Door Cupboard, 1 Coffee table with 2 sofa, 1 Side table, Balcony with an Accent table with 2 Chair and an attached washroom with hot/cold water.\n"), 
                    "3-Bed AC": (14000,"Price:14000->1 Double Bed + 1 Single Bed, Television, Telephone, a Triple-Door Cupboard, 1 Coffee table with 2 sofa, 1 Side table, Balcony with an Accent table with 2 Chair and an attached washroom with hot/cold water + Window/Split AC.\n")}
        tk.Label(f, text="Name:").pack(); e1 = tk.Entry(f, width=40); e1.pack()
        tk.Label(f, text="Phone:").pack(); e2 = tk.Entry(f, width=40); e2.pack()
        tk.Label(f, text="Address:").pack(); e3 = tk.Entry(f, width=40); e3.pack()
        tk.Label(f, text="In:").pack(); ci = DateEntry(f, width=37, date_pattern='dd/mm/yyyy'); ci.pack()
        tk.Label(f, text="Out:").pack(); co = DateEntry(f, width=37, date_pattern='dd/mm/yyyy'); co.pack()
        rt = ttk.Combobox(f, values=list(self.r_d.keys()), width=37); rt.pack(pady=10); d_l = tk.Label(f, text="", fg="blue")
        d_l.pack(); rt.bind("<<ComboboxSelected>>", lambda e: d_l.config(text=f"Amenities: {self.r_d[rt.get()][1]}"))
        def save():
            cid, rn = random.randint(100, 999), random.randint(300, 399)
            conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
            c.execute("INSERT INTO guests (cust_id, name, phno, address, checkin, checkout, room_type, room_no, room_price, restaurant_bill, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (cid, e1.get(), e2.get(), e3.get(), ci.get(), co.get(), rt.get(), rn, self.r_d[rt.get()][0], 0, "Unpaid"))
            conn.commit(); conn.close(); win.destroy()
        tk.Button(f, text="Book", bg="green", fg="white", command=save).pack(pady=10)

    def Rooms_Info_UI(self): messagebox.showinfo("Info", "Prices: 5000 - 14000")

if __name__ == "__main__":
    root = tk.Tk();
    app = HotelAG(root); 
    root.mainloop()