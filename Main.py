import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3
import random
import pyttsx3  
from datetime import datetime

class HotelAG:
    def __init__(self, root):
        self.root = root
        self.root.title("HOTEL AG MANAGEMENT SYSTEM")
        self.root.geometry("900x700")
        
        # Speech Setup
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        
        self.engine.setProperty('voice', voices[0].id) 
        self.engine.setProperty('rate', 150) 
        
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
        tk.Label(self.root, text="WELCOME TO HOTEL AG", font=("times new roman", 30, "bold"), pady=40).pack()

        buttons = [
            ("1 Booking", self.Booking_UI),
            ("2 Rooms Info", self.Rooms_Info_UI),
            ("3 Room Service (Menu Card)", self.Restaurant_UI),
            ("4 Payment & Bill", self.Payment_UI),
            ("5 Record (Database)", self.Record_UI),
            ("0 Exit", self.root.quit)
        ]

        for text, command in buttons:
            tk.Button(self.root, text=text, font=("times new roman", 12,"bold"), bd=10,width=35, height=2, command=command).pack(pady=10)

    # --- UPDATED BOOKING WITH ROOM DETAILS ---
    def Booking_UI(self):
        win = tk.Toplevel(self.root); win.geometry("560x800")
        win.title("Room Booking")
        
        # Room Details Map
        self.room_info_map = {
            "Standard Non-AC": (5000, "1 Double Bed, Television, Telephone,Double-Door Cupboard, 1 Coffee table with 2 sofa, Balcony and an attached washroom with hot/cold water.\n"),
            "Standard AC": (8000, "1 Double Bed, Television, Telephone, Double-Door Cupboard, 1 Coffee table with 2 sofa, Balcony and an attached washroom with hot/cold water + Window/Split AC.\n"),
            "3-Bed Non-AC": (11000, "1 Double Bed + 1 Single Bed, Television, Telephone, a Triple-Door Cupboard, 1 Coffee table with 2 sofa, 1 Side table, Balcony with an Accent table with 2 Chair and an attached washroom with hot/cold water.\n"),
            "3-Bed AC": (14000, "1 Double Bed + 1 Single Bed, Television, Telephone, a Triple-Door Cupboard, 1 Coffee table with 2 sofa, 1 Side table, Balcony with an Accent table with 2 Chair and an attached washroom with hot/cold water + Window/Split AC.\n")
        }

        tk.Label(win, text="Name:").pack(); e_n = tk.Entry(win, width=40); e_n.pack()
        tk.Label(win, text="Phone:").pack(); e_p = tk.Entry(win, width=40); e_p.pack()
        tk.Label(win, text="Address:").pack(); e_a = tk.Entry(win, width=40); e_a.pack()
        tk.Label(win, text="Check-In:").pack(); ci = DateEntry(win, width=37, date_pattern='dd/mm/yyyy'); ci.pack()
        tk.Label(win, text="Check-Out:").pack(); co = DateEntry(win, width=37, date_pattern='dd/mm/yyyy'); co.pack()
        
        tk.Label(win, text="Select Room Type:").pack(pady=5)
        rt = ttk.Combobox(win, values=list(self.room_info_map.keys()), width=37); rt.pack()
        
        
        # Live Room Details Label
        details_label = tk.Label(win, text="", fg="blue", wraplength=400, font=("times new roman", 9, "italic","bold"))
        details_label.pack(pady=10)

        def on_room_change(event):
            selection = rt.get()
            price, info = self.room_info_map[selection]
            details_label.config(text=f"Amenities: {info}\nPrice: Rs. {price}")

        rt.bind("<<ComboboxSelected>>", on_room_change)

        def save():
            if not rt.get(): messagebox.showwarning("Warning", "Select Room Type"); return
            cid, rn = random.randint(100, 999), random.randint(300, 399)
            price = self.room_info_map[rt.get()][0]
            conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
            c.execute("INSERT INTO guests (cust_id, name, phno, address, checkin, checkout, room_type, room_no, room_price, restaurant_bill, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (cid, e_n.get(), e_p.get(), e_a.get(), ci.get(), co.get(), rt.get(), rn, price, 0, "Unpaid"))
            conn.commit(); conn.close()
            messagebox.showinfo("Success", f"Booked Successfully!\nID: {cid}\nRoom: {rn}")
            self.speak("Happy stay in A G Hotel"); 
            win.destroy()

        tk.Button(win, text="Confirm Booking",font=("times new roman", 15,"bold"), bg="red", fg="white",bd=10, command=save, width=20).pack(pady=20)
        

    # --- RESTAURANT  ---
    def Restaurant_UI(self):
        win = tk.Toplevel(self.root); win.state('zoomed')
        canvas = tk.Canvas(win); sb = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        sf = ttk.Frame(canvas); sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((win.winfo_screenwidth()//2, 0), window=sf, anchor="n")
        
        tk.Label(sf, text="MENU CARD", font=("times new roman", 30, "bold"), fg="red", pady=20).pack()
        tk.Label(sf, text="Enter Cust ID:").pack(); cid_e = tk.Entry(sf, font=("times new roman", 14,"bold")); cid_e.pack(pady=10)

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
            tk.Label(sf, text=cat, font=("times new roman", 16, "bold"), fg="blue", pady=10).pack(anchor="w")
            for itm, prc in items.items():
                fr = tk.Frame(sf); fr.pack(fill="x", padx=50)
                v, q = tk.IntVar(), tk.IntVar(value=1)
                tk.Checkbutton(fr, text=f"{itm} - Rs.{prc}", variable=v, font=("times new roman", 12)).pack(side="left")
                tk.Spinbox(fr, from_=1, to=10, width=5, textvariable=q).pack(side="left", padx=10)
                vars[itm] = (v, q, prc)

        def order():
            tot = sum(v.get() * q.get() * p for v, q, p in vars.values())
            conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
            c.execute("UPDATE guests SET restaurant_bill = restaurant_bill + ? WHERE cust_id = ?", (tot, cid_e.get()))
            conn.commit(); conn.close(); win.destroy()
        tk.Button(sf, text="Confirm Order", font=("times new roman", 14,"bold"),bd=10, bg="blue", fg="white", command=order).pack(pady=30)
        canvas.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

    # --- UPDATED RECORD WITH SEARCH, EDIT, DELETE ---
    def Record_UI(self):
        win = tk.Toplevel(self.root); win.geometry("1100x700")
        win.title("Hotel Database")

        # Search Frame
        search_fr = tk.Frame(win); search_fr.pack(pady=10)
        tk.Label(search_fr, text="Search (Name/Phone/ID): ").pack(side="left")
        search_ent = tk.Entry(search_fr, width=30); search_ent.pack(side="left", padx=10)

        cols = ("Cust ID", "Name", "Phone", "CheckIn", "CheckOut", "Room", "RoomNo", "Bill", "Status")
        tree = ttk.Treeview(win, columns=cols, show='headings')
        for col in cols: tree.heading(col, text=col); tree.column(col, width=110, anchor="center")
        tree.pack(expand=True, fill='both')

        def load_data(query=""):
            for item in tree.get_children(): tree.delete(item)
            conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
            if query:
                c.execute("SELECT cust_id, name, phno, checkin, checkout, room_type, room_no, (room_price + restaurant_bill), status FROM guests WHERE name LIKE ? OR phno LIKE ? OR cust_id LIKE ?", (f'%{query}%', f'%{query}%', f'%{query}%'))
            else:
                c.execute("SELECT cust_id, name, phno, checkin, checkout, room_type, room_no, (room_price + restaurant_bill), status FROM guests")
            for row in c.fetchall(): tree.insert("", tk.END, values=row)
            conn.close()

        search_ent.bind("<KeyRelease>", lambda e: load_data(search_ent.get()))
        
        def delete_rec():
            selected = tree.selection()
            if not selected: return
            if messagebox.askyesno("Confirm", "Delete this record?"):
                cid = tree.item(selected[0])['values'][0]
                conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
                c.execute("DELETE FROM guests WHERE cust_id=?", (cid,))
                conn.commit(); conn.close(); load_data()

        def edit_rec():
            selected = tree.selection()
            if not selected: return
            cid = tree.item(selected[0])['values'][0]
            edit_win = tk.Toplevel(win); edit_win.geometry("300x300")
            
            conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
            c.execute("SELECT name, phno, address FROM guests WHERE cust_id=?", (cid,))
            row = c.fetchone()
            
            tk.Label(edit_win, text="Edit Name:").pack()
            e_n = tk.Entry(edit_win); e_n.insert(0, row[0]); e_n.pack()
            tk.Label(edit_win, text="Edit Phone:").pack()
            e_p = tk.Entry(edit_win); e_p.insert(0, row[1]); e_p.pack()

            def update():
                c.execute("UPDATE guests SET name=?, phno=? WHERE cust_id=?", (e_n.get(), e_p.get(), cid))
                conn.commit(); conn.close(); edit_win.destroy(); load_data()
            tk.Button(edit_win, text="Update", command=update).pack(pady=10)

        btn_fr = tk.Frame(win); btn_fr.pack(pady=10)
        tk.Button(btn_fr, text="Edit Selected", font=("times new roman", 12,"bold"), command=edit_rec,bd=10, bg="blue", fg="white").pack(side="left", padx=10)
        tk.Button(btn_fr, text="Delete Selected",font=("times new roman", 12,"bold"),  command=delete_rec,bd=10, bg="red", fg="white").pack(side="left", padx=10)
        load_data()

    # --- PAYMENT WITH YES/NO RECEIPT ---
    def Payment_UI(self):
        win = tk.Toplevel(self.root); win.geometry("300x200")
        tk.Label(win, text="Enter Phone Number:").pack(pady=10)
        e = tk.Entry(win); e.pack()

        def pay():
            conn = sqlite3.connect('hotel_records.db'); c = conn.cursor()
            c.execute("SELECT name, room_price, restaurant_bill, cust_id, room_no, room_type, checkin, checkout, phno FROM guests WHERE phno=? AND status='Unpaid'", (e.get(),))
            res = c.fetchone()
            if res:
                total = res[1] + res[2]
                if messagebox.askyesno("Confirm", f"Name: {res[0]}\nTotal: Rs.{total}\nProceed with Payment?"):
                    c.execute("UPDATE guests SET status='Paid' WHERE phno=?", (e.get(),))
                    conn.commit()
                    self.speak("Thanks! Visit Again")
                    
                    # (1) YES/NO OPTION FOR RECEIPT
                    if messagebox.askyesno("Payment Successful", "Do you want to see the receipt?"):
                        self.show_receipt_on_screen({'name':res[0],'room_price':res[1],'food_price':res[2],'cust_id':res[3],'room_no':res[4],'room_type':res[5],'checkin':res[6],'checkout':res[7],'phone':res[8]})
                    win.destroy()
            else: messagebox.showerror("Error", "No unpaid records found")
            conn.close()

        tk.Button(win, text="Pay Bill", font=("times new roman", 12,"bold"), command=pay,bd=10, bg="blue", fg="white").pack(pady=20)

    def show_receipt_on_screen(self, data):
        bill_win = tk.Toplevel(self.root)
        bill_win.title("Receipt")
        bill_win.geometry("400x600"); bill_win.configure(bg="white")
        total = data['room_price'] + data['food_price']
        tk.Label(bill_win, text="HOTEL AG RECEIPT", font=("times new roman", 20, "bold"), bg="white").pack(pady=10)
        content = f"Cust ID: {data['cust_id']}\nName: {data['name']}\nPhone: {data['phone']}\nRoom No: {data['room_no']}\nType: {data['room_type']}\n\nCheck-In: {data['checkin']}\nCheck-Out: {data['checkout']}\n\nRoom Rent: Rs. {data['room_price']}\nFood Bill: Rs. {data['food_price']}\n\nTOTAL: Rs. {total}\nStatus: PAID"
        tk.Label(bill_win, text=content, font=("times new roman", 12,"bold"), bg="white", justify="left").pack(pady=10)
        tk.Button(bill_win, text="Close", command=bill_win.destroy).pack(pady=20)

    def Rooms_Info_UI(self):
        messagebox.showinfo("Info", "Standard AC: 8000\nStandard Non-AC: 5000\n3-Bed AC: 14000\n3-Bed Non-AC: 11000")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelAG(root)
    root.mainloop()