import tkinter as tk
from tkinter import messagebox, Toplevel, scrolledtext
import sqlite3
import datetime
import os

class PatoPoaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pato Poa System")
        self.root.geometry("400x900")
        self.root.configure(bg="#90EE90")
        
        self.init_db()
        
        self.btn_atm = tk.Button(root, text="ATM\nLIPA HAPA", command=self.fungua_ukurasa_malipo, 
                                 bg="blue", fg="white", font=("Arial", 16, "bold"), height=3, width=15)
        self.btn_atm.pack(pady=10)
        
        self.hatua = ["SAJILI MADENI", "Namba ya Simu", "Anwani ya Makazi", "Namba ya Nyumba", "Namba ya Simu ya Mdhamini", "Namba ya ID", "Tarehe ya Usajili", "Kiasi cha Mkopo"]
        self.index = 0
        self.data_zilizokusanywa = {}
        
        self.label_maelekezo = tk.Label(root, text=self.hatua[0], bg="#90EE90", font=("Arial", 14, "bold"))
        self.label_maelekezo.pack(pady=5)
        
        self.entry = tk.Entry(root, width=25, font=("Arial", 14)) 
        self.entry.pack(pady=5)
        
        tk.Label(root, text="Tafuta Mteja:", bg="#90EE90", font=("Arial", 9, "bold")).pack()
        self.entry_search = tk.Entry(root, width=25)
        self.entry_search.pack(pady=2)
        self.entry_search.bind("<KeyRelease>", self.tafuta_mteja)
        
        self.frame_btns = tk.Frame(root, bg="#90EE90")
        self.frame_btns.pack(pady=10)
        
        tk.Button(self.frame_btns, text="RUDI", command=self.rudi_nyuma, bg="orange", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_btns, text="ENDELEA", command=self.thibitisha_hatua, bg="blue", fg="white", width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Label(root, text="Orodha ya Wateja:", bg="#90EE90", font=("Arial", 10, "bold")).pack(pady=5)
        self.listbox_wateja = tk.Listbox(root, font=("Arial", 10), height=8, width=45)
        self.listbox_wateja.pack(pady=5, padx=10)
        
        tk.Button(root, text="ONYEHA KUMBUKUMBU ZOTE", command=self.onyesha_kumbukumbu_dirisha, bg="purple", fg="white", width=30).pack(pady=5)
        
        self.frame_chini = tk.Frame(root, bg="#90EE90")
        self.frame_chini.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=20)
        
        tk.Button(self.frame_chini, text="TOKA", command=root.quit, bg="red", fg="white", width=10).pack(side=tk.LEFT)
        tk.Button(self.frame_chini, text="FUTA", command=self.futa_data, bg="gray", fg="white", width=10).pack(side=tk.RIGHT)
        
        self.onyesha_data()

    def init_db(self):
        with sqlite3.connect("patopoa.db") as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS wateja (id INTEGER PRIMARY KEY AUTOINCREMENT, jina TEXT, simu TEXT, anwani TEXT, nyumba TEXT, mdhamini TEXT, id_namba TEXT, tarehe TEXT, kiasi REAL)''')
            c.execute('''CREATE TABLE IF NOT EXISTS malipo (id INTEGER PRIMARY KEY AUTOINCREMENT, jina_mteja TEXT, kiasi REAL, tarehe TEXT)''')
            conn.commit()

    def onyesha_kumbukumbu_dirisha(self):
        win = Toplevel(self.root)
        win.title("Kumbukumbu")
        win.geometry("400x550")
        win.configure(bg="#90EE90")
        
        txt = scrolledtext.ScrolledText(win, width=45, height=20)
        txt.pack(pady=10)
        
        if os.path.exists("kumbukumbu_zote.txt"):
            with open("kumbukumbu_zote.txt", "r", encoding='utf-8') as f:
                txt.insert(tk.INSERT, f.read())
        
        txt.config(state='disabled')
        
        def futa_kumbukumbu():
            if messagebox.askyesno("Tahadhari", "Je, unataka kufuta kumbukumbu zote?"):
                if os.path.exists("kumbukumbu_zote.txt"):
                    os.remove("kumbukumbu_zote.txt")
                    txt.config(state='normal')
                    txt.delete('1.0', tk.END)
                    txt.insert(tk.INSERT, "Kumbukumbu imefutwa.")
                    txt.config(state='disabled')
                    messagebox.showinfo("Safi", "Kumbukumbu zote zimefutwa.")

        tk.Button(win, text="FUTA KUMBUKUMBU ZOTE", command=futa_kumbukumbu, bg="red", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
        tk.Button(win, text="FUNGA", command=win.destroy, bg="gray", fg="white").pack(pady=5)

    # Kazi mpya ya kutuma ujumbe
    def tuma_ujumbe_wa_karibu(self, namba_ya_simu, jina):
        ujumbe = f"Habari {jina}, karibu katika Pato Poa! Sisi ni washindi. Deni lako limepokelewa."
        print(f"Inatuma SMS kwenda {namba_ya_simu}: {ujumbe}")
        # Hapa ndipo utaunganisha API yako ya SMS siku zijazo

    def maliza_usajili(self):
        with sqlite3.connect("patopoa.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO wateja (jina, simu, anwani, nyumba, mdhamini, id_namba, tarehe, kiasi) VALUES (?,?,?,?,?,?,?,?)", list(self.data_zilizokusanywa.values()))
            conn.commit()
        
        jina = self.data_zilizokusanywa.get("SAJILI MADENI")
        simu = self.data_zilizokusanywa.get("Namba ya Simu")
        
        if simu:
            self.tuma_ujumbe_wa_karibu(simu, jina)
            
        messagebox.showinfo("Imefanikiwa", f"Mteja {jina} amesajiliwa na ujumbe wa karibu umetayarishwa!")
        
        self.index = 0
        self.data_zilizokusanywa = {}
        self.label_maelekezo.config(text=self.hatua[0])
        self.onyesha_data()

    def futa_data(self):
        selection = self.listbox_wateja.curselection()
        if not selection:
            messagebox.showwarning("Tahadhari", "Chagua mteja kwenye orodha!")
            return
        
        jina_la_mteja = self.listbox_wateja.get(selection).split(" - ")[0]
        
        msg_box = messagebox.askyesnocancel("Chagua Hatua", 
                                            f"Mteja: {jina_la_mteja}\n\n"
                                            "- Yes (SAVE): Hifadhi kwenye kumbukumbu na uondoe.\n"
                                            "- No (DELETE): Futa kabisa (Delete).\n"
                                            "- Cancel: Acha.")
        
        if msg_box is None: return
            
        with sqlite3.connect("patopoa.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM wateja WHERE jina = ?", (jina_la_mteja,))
            mteja = c.fetchone()
            
            if msg_box == True:
                if mteja:
                    with open("kumbukumbu_zote.txt", "a", encoding='utf-8') as f:
                        f.write(f"KUMBUKUMBU: {datetime.datetime.now()} | {mteja}\n")
                messagebox.showinfo("Imefanikiwa", "Taarifa zimehifadhiwa.")
            elif msg_box == False:
                messagebox.showinfo("Imefanikiwa", "Taarifa zimefutwa kabisa.")
            
            c.execute("DELETE FROM wateja WHERE jina = ?", (jina_la_mteja,))
            conn.commit()
            
        self.onyesha_data()

    def fungua_ukurasa_malipo(self):
        win = Toplevel(self.root)
        win.title("ATM - Pato Poa")
        win.geometry("350x450")
        win.configure(bg="#90EE90")
        tk.Label(win, text="REKODI MALIPO", font=("Arial", 14, "bold"), bg="#90EE90").pack(pady=10)
        entry_jina = tk.Entry(win, width=30)
        entry_jina.pack(pady=5)
        entry_kiasi = tk.Entry(win, width=30)
        entry_kiasi.pack(pady=5)
        tk.Button(win, text="HIFADHI MALIPO", command=lambda: self.process_malipo(entry_jina, entry_kiasi, win), bg="blue", fg="white", width=20).pack(pady=10)
        tk.Button(win, text="KUMBUKUMBU", command=self.onyesha_kumbukumbu_dirisha, bg="purple", fg="white", width=20).pack(pady=5)
        tk.Button(win, text="FUNGA", command=win.destroy, bg="red", fg="white", width=20).pack(pady=5)

    def process_malipo(self, entry_jina, entry_kiasi, win):
        try:
            jina, kiasi = entry_jina.get().strip(), float(entry_kiasi.get().strip())
            with sqlite3.connect("patopoa.db") as conn:
                c = conn.cursor()
                c.execute("UPDATE wateja SET kiasi = kiasi - ? WHERE jina = ?", (kiasi, jina))
                conn.commit()
            messagebox.showinfo("Safi", "Malipo yamehifadhiwa!")
            self.onyesha_data()
            win.destroy()
        except:
            messagebox.showerror("Kosa", "Ingiza taarifa sahihi!")

    def onyesha_data(self):
        self.listbox_wateja.delete(0, tk.END)
        with sqlite3.connect("patopoa.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM wateja")
            for row in c.fetchall():
                self.listbox_wateja.insert(tk.END, f"{row[1]} - Deni: Tsh {row[8]}")

    def tafuta_mteja(self, event):
        self.listbox_wateja.delete(0, tk.END)
        with sqlite3.connect("patopoa.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM wateja WHERE jina LIKE ?", ('%'+self.entry_search.get()+'%',))
            for row in c.fetchall():
                self.listbox_wateja.insert(tk.END, f"{row[1]} - Deni: Tsh {row[8]}")

    def thibitisha_hatua(self):
        val = self.entry.get()
        if not val: return
        self.data_zilizokusanywa[self.hatua[self.index]] = val
        self.entry.delete(0, tk.END)
        self.index += 1
        if self.index < len(self.hatua):
            self.label_maelekezo.config(text=self.hatua[self.index])
        else:
            self.maliza_usajili()

    def rudi_nyuma(self):
        if self.index > 0:
            self.index -= 1
            self.label_maelekezo.config(text=self.hatua[self.index])

root = tk.Tk()
app = PatoPoaApp(root)
root.mainloop()
#