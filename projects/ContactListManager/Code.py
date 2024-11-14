import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


class Contact:
    def _init_(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def _str_(self):
        return f'Name: {self.name}, Phone: {self.phone}, Email: {self.email}'


class ContactListManager:
    def _init_(self):
        self.contacts = {}
        self.load_contacts()

    def add_contact(self, name, phone, email):
        if name in self.contacts:
            messagebox.showerror("Error", "Contact already exists.")
        else:
            self.contacts[name] = Contact(name, phone, email)
            messagebox.showinfo("Success", "Contact added successfully.")
            self.save_contacts()

    def view_contacts(self):
        if not self.contacts:
            messagebox.showinfo("Info", "No contacts found.")
        else:
            contacts_str = "\n".join(str(contact) for contact in self.contacts.values())
            messagebox.showinfo("Contacts", contacts_str)

    def search_contact(self, name):
        contact = self.contacts.get(name)
        if contact:
            messagebox.showinfo("Contact Found", str(contact))
        else:
            messagebox.showerror("Error", "Contact not found.")

    def update_contact(self, name, phone=None, email=None):
        contact = self.contacts.get(name)
        if contact:
            if phone:
                contact.phone = phone
            if email:
                contact.email = email
            messagebox.showinfo("Success", "Contact updated successfully.")
            self.save_contacts()
        else:
            messagebox.showerror("Error", "Contact not found.")

    def delete_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            messagebox.showinfo("Success", "Contact deleted successfully.")
            self.save_contacts()
        else:
            messagebox.showerror("Error", "Contact not found.")

    def save_contacts(self):
        with open('contacts.json', 'w') as f:
            json.dump({name: vars(contact) for name, contact in self.contacts.items()}, f)

    def load_contacts(self):
        if os.path.exists('contacts.json'):
            with open('contacts.json', 'r') as f:
                contacts_data = json.load(f)
                self.contacts = {name: Contact(**data) for name, data in contacts_data.items()}


class App:
    def _init_(self, master):
        self.manager = ContactListManager()
        self.master = master
        self.master.title("Contact List Manager")

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        self.add_button = tk.Button(self.frame, text="Add Contact", command=self.add_contact)
        self.add_button.pack(fill=tk.X)

        self.view_button = tk.Button(self.frame, text="View Contacts", command=self.manager.view_contacts)
        self.view_button.pack(fill=tk.X)

        self.search_button = tk.Button(self.frame, text="Search Contact", command=self.search_contact)
        self.search_button.pack(fill=tk.X)

        self.update_button = tk.Button(self.frame, text="Update Contact", command=self.update_contact)
        self.update_button.pack(fill=tk.X)

        self.delete_button = tk.Button(self.frame, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack(fill=tk.X)

        self.exit_button = tk.Button(self.frame, text="Exit", command=self.master.quit)
        self.exit_button.pack(fill=tk.X)

    def add_contact(self):
        name = simpledialog.askstring("Input", "Enter name:")
        phone = simpledialog.askstring("Input", "Enter phone:")
        email = simpledialog.askstring("Input", "Enter email:")
        if name and phone and email:
            self.manager.add_contact(name, phone, email)

    def search_contact(self):
        name = simpledialog.askstring("Input", "Enter name to search:")
        if name:
            self.manager.search_contact(name)

    def update_contact(self):
        name = simpledialog.askstring("Input", "Enter name to update:")
        phone = simpledialog.askstring("Input", "Enter new phone (leave blank to skip):")
        email = simpledialog.askstring("Input", "Enter new email (leave blank to skip):")
        if name:
            self.manager.update_contact(name, phone if phone else None, email if email else None)

    def delete_contact(self):
        name = simpledialog.askstring("Input", "Enter name to delete:")
        if name:
            self.manager.delete_contact(name)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()