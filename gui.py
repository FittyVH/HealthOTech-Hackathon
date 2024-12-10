import tkinter as tk
from tkinter import scrolledtext
from mistralai import Mistral

def run_mistral_chat(api_key, user_message, model="mistral-large-latest"):
    client = Mistral(api_key=api_key)
    system_message = {
        "role": "system",
        "content": "You are an AI assistant specialized in providing information about medical schemes and medical rights available in india. Do not answer questions unrelated to medical schemes."
    }
    user_message = {"role": "user", "content": user_message}
    
    chat_response = client.chat.complete(
        model=model,
        messages=[system_message, user_message]
    )
    
    return chat_response.choices[0].message.content

class MedicalChatBotApp:
    def __init__(self, root, api_key):
        self.api_key = api_key
        self.root = root
        self.root.title("Medical Schemes Chatbot")

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=70, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.chat_display.tag_config("user_bold", font=("Arial", 10, "bold"))

        # Input area
        self.input_label = tk.Label(root, text="Enter your query about medical schemes:")
        self.input_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.user_input = tk.Entry(root, width=50)
        self.user_input.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Buttons
        self.send_button = tk.Button(root, text="Send", command=self.get_response)
        self.send_button.grid(row=2, column=1, padx=10, pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=3, column=1, padx=10, pady=5)

    def get_response(self):
        user_message = self.user_input.get().strip()
        if not user_message:
            return  
    
        self.update_chat(f"User: {user_message}", is_user=True)

        try:
            response = run_mistral_chat(self.api_key, user_message)
            self.update_chat(f"Bot: {response}")
        except Exception as e:
            self.update_chat(f"Error: {str(e)}")
    
        self.user_input.delete(0, tk.END)

    def update_chat(self, message, is_user = False):
        self.chat_display.config(state='normal')
    
        if is_user:
            self.chat_display.insert(tk.END, message + "\n", "user_bold")
        else:
            self.chat_display.insert(tk.END, message + "\n")
    
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def exit_app(self):
        self.root.quit()

if __name__ == "__main__":
    api_key = "paste your own mistral api key here:)"  # mistral ai api key

    root = tk.Tk()
    app = MedicalChatBotApp(root, api_key)
    root.mainloop()
