import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.fernet import Fernet
import os

class FuadFileEncryptorDecryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("Fuad File Encryptor & Decryptor")
        self.root.geometry("400x250")
        
        # Set custom logo/icon
        self.set_icon("ikon.png")  # Replace with your logo file path

        self.encrypted_extension = ".fuadencrypted"

        self.label = tk.Label(root, text="Fuad File Encryptor & Decryptor", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.encrypt_button = tk.Button(root, text="Encrypt File", command=self.encrypt)
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = tk.Button(root, text="Decrypt File", command=self.decrypt)
        self.decrypt_button.pack(pady=5)

        self.customize_button = tk.Button(root, text="Customize Encrypted Extension", command=self.customize_extension)
        self.customize_button.pack(pady=5)
        
        self.create_key_button = tk.Button(root, text="Create Key", command=self.create_key)
        self.create_key_button.pack(pady=5)

    def set_icon(self, icon_path):
        try:
            icon = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(False, icon)
        except Exception as e:
            print(f"Error setting icon: {e}")

    def customize_extension(self):
        new_extension = simpledialog.askstring("Input", "Enter new encrypted file extension (e.g., .encrypted):", parent=self.root)
        if new_extension:
            if not new_extension.startswith('.'):
                new_extension = '.' + new_extension
            self.encrypted_extension = new_extension
            messagebox.showinfo("Success", f"Encrypted file extension set to: {new_extension}")

    def create_key(self):
        key_path = filedialog.asksaveasfilename(title="Save Key As", defaultextension=".key", filetypes=[("Key files", "*.key")])
        if key_path:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
            messagebox.showinfo("Success", "Key Saved! Don't lose it!")

    def encrypt_file(self, file_path, key_path):
        with open(key_path, 'rb') as key_file:
            key = key_file.read()

        cipher_suite = Fernet(key)

        with open(file_path, 'rb') as file:
            file_data = file.read()

        encrypted_data = cipher_suite.encrypt(file_data)

        encrypted_file_path = file_path + self.encrypted_extension
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)

        os.remove(file_path)
        messagebox.showinfo("Success", f"File encrypted and saved as {encrypted_file_path}")

    def decrypt_file(self, file_path, key_path):
        with open(key_path, 'rb') as key_file:
            key = key_file.read()

        cipher_suite = Fernet(key)

        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        try:
            decrypted_data = cipher_suite.decrypt(encrypted_data)
        except Exception as e:
            messagebox.showerror("Error", "Failed to decrypt file")
            return

        decrypted_file_path = file_path.replace(self.encrypted_extension, '')
        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_data)

        os.remove(file_path)
        messagebox.showinfo("Success", f"File decrypted and saved as {decrypted_file_path}")

    def encrypt(self):
        file_path = filedialog.askopenfilename(title="Select a file to encrypt")
        if not file_path:
            return

        key_path = filedialog.askopenfilename(title="Select Key File", filetypes=[("Key files", "*.key")])
        if not key_path:
            return

        self.encrypt_file(file_path, key_path)

    def decrypt(self):
        file_path = filedialog.askopenfilename(title="Select an encrypted file", filetypes=[("Encrypted files", "*" + self.encrypted_extension)])
        if not file_path:
            return

        key_path = filedialog.askopenfilename(title="Select Key File", filetypes=[("Key files", "*.key")])
        if not key_path:
            return

        self.decrypt_file(file_path, key_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = FuadFileEncryptorDecryptor(root)
    root.mainloop()
