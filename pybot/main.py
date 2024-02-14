import tkinter as tk
from tkinter import scrolledtext
from get_bot_response import *
from tkinter import ttk

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.chat_log = [
            {"role":"system", "content":"You are a financial assistant specialised in giving advice on how to allocate a portfolio with minimum risk and providing information about various stocks."}
        ]
        
        self.style = ttk.Style(root)
        self.style.theme_use('alt')

        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_history.pack(padx=10, pady=10)
        self.chat_history.config(state=tk.DISABLED)
        
        self.user_input = tk.Entry(root, width=40)
        self.user_input.pack(padx=10, pady=10)
        
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack()
            
    def display_bot_response(self, sender, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"{sender}: {message}\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)
    
    def send_message(self):
        user_message = self.user_input.get()
        self.display_bot_response("You", user_message)
        self.user_input.delete(0, tk.END)
        
        bot_response = self.get_bot_response(user_message)
        self.display_bot_response("Bot", bot_response)
    
    def get_bot_response(self, user_message):
        self.chat_log.append({"role" : "user", "content":user_message})
        if "search" in user_message.split(" "):
            bot_response = get_news_sentiment(self.chat_log, user_message.split(" ")[-1])
        else:
            bot_response = get_bot_response(self.chat_log)
        self.chat_log.append({"role" : "assistant", "content":bot_response})
        return bot_response

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    root.mainloop()
