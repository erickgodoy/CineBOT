import random
import json
import pickle
import numpy as np
import os
import mysql.connector
import nltk

from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from tkinter import *
from PIL import ImageTk, Image

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'cinedb'
    )
    

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))		
classes = pickle.load(open('classes.pkl', 'rb'))	
model = load_model('chatbotmodel.h5')			

def clean_up_sentence(sentence):				
    sentence_words = nltk.word_tokenize(sentence)			
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]		
    return sentence_words	

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)	
    bag = [0] * len(words)						
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:		
                bag[i] = 1		
    return np.array(bag)		


def predict_class(sentence):
    bow = bag_of_words(sentence)		
    res = model.predict(np.array([bow]))[0]		
    ERROR_THRESHOLD = 0.25						
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]		

    results.sort(key=lambda x: x[1], reverse=True)		
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})		
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])		
            break
    return result



BG_GRAY = "#ff6978"
BG_COLOR = "#fffcf9"

#TEXT_COLOR = "#EAECEE"
TEXT_COLOR = "#36413e"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

img_cine = Image.open("./img/logo2.png")


state = 0
respuestas_reserva = []
it = 1


class ChatApplication: 

    def __init__(self):       
        self.window = Tk()
        self._setup_main_window()
     
    def run(self):

        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("CineBOT")
        self.window.iconbitmap('./img/icon.ico')
        self.window.resizable(width=False, height=False)        #Fijar Tamaño
        self.window.configure(width=470, height=550, bg=BG_COLOR)   #Dimensiones de ventana
        
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="CineBOT", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        self.tkimage = ImageTk.PhotoImage(img_cine)
        img_label = Label(self.window,image = self.tkimage)
        img_label.place(x=150, y=0)

 
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # messagebox
        self.msg_entry = Entry(bottom_label, bg="#fffcf9", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # boton enviar
        send_button = Button(bottom_label, text="Enviar", font=FONT_BOLD, width=20, bg="#a5be00", 
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
    
    def reserva(self, n, msg):
        global it
        it = it + 1
        self.msg_entry.delete(0, END)
        if n == 1:
            msg2 = f"Yo: reserva\n\nBOT: Nombres y Apellidos\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg2)
            self.text_widget.configure(state=DISABLED)
            self.text_widget.see(END)
        
        if n == 2:
            msg1 = f"Yo: {msg}\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg1)
            self.text_widget.configure(state=DISABLED)
            respuestas_reserva.append(msg)

            msg2 = f"BOT: Nombre de la Pelicula\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg2)
            self.text_widget.configure(state=DISABLED)

        if n == 3:
            msg1 = f"Yo: {msg}\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg1)
            self.text_widget.configure(state=DISABLED)
            respuestas_reserva.append(msg)

            msg2 = f"BOT: Seleccione un horario\n\n1) 4:30\n\n2) 6:30\n\n3) 8:30\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg2)
            self.text_widget.configure(state=DISABLED)    

        if n == 4:
            horario = int(msg)
            hora = ""

            msg1 = f"Yo: {msg}\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg1)
            self.text_widget.configure(state=DISABLED)

            if horario == 1:
                hora = "4:30"
            elif horario == 2:
                hora = "6:30"
            elif horario == 3:
                hora = "8:30"
            else:
                hora = "0:00"

            respuestas_reserva.append(hora)
            nroSala  = random.randint(1,3)

            msg2 = f"BOT: La sala asignada es N° {nroSala}\n\n BOT: Ingrese el numero del asiento (1-50):\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg2)
            self.text_widget.configure(state=DISABLED)

            respuestas_reserva.append(nroSala)             

        if n == 5:
            msg1 = f"Yo: {msg}\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg1)
            self.text_widget.configure(state=DISABLED)
            respuestas_reserva.append(int(msg))
           

            msg2 = f"RESERVA EXITOSA!\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg2)
            self.text_widget.configure(state=DISABLED)   



            cursor = mydb.cursor()
            cursor.execute("INSERT INTO reserva(nombres, pelicula, hora, sala, asiento) VALUES (%s,%s,%s,%s,%s)",(respuestas_reserva[0],respuestas_reserva[1],respuestas_reserva[2],respuestas_reserva[3],respuestas_reserva[4]))
            mydb.commit()

            respuestas_reserva.clear()
            it = 0

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        msg = msg.lower()
        global state
        if msg == 'reserva':
            state = 1

        if state == 1:
            self.reserva( it, msg)
            if it == 6:
                state = 0
        else:
            self._insert_message(msg, "Yo", "Bot")

    def _insert_message(self, msg, sender, bot_name):
        if not msg:
            return
            
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"{bot_name}: {get_response(predict_class(msg), intents)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)
             
if __name__ == "__main__":
    app = ChatApplication()
    app.run()