import os, csv, string, re, random, pyperclip, pathlib
import tkinter as tk
from tkinter import filedialog, Text, messagebox
from pathlib import Path

user_dir = str(Path.home())
app_dir = "\\Documents\\PasswordManager"
pathlib.Path(user_dir+app_dir).mkdir(parents=True, exist_ok=True)
os.chdir(user_dir + app_dir)
csv_file_exists = os.path.isfile("password.csv")


def append_to_csvPassword(username, password, url):
    with open ("password.csv", "a", newline="") as csv_file:
        fieldnames = ["username", "password", "url"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not csv_file_exists:
            csv_writer.writeheader()

        csv_writer.writerow({"username": username, "password": password, "url" : url})

        return True

def find_Password(site):
    webRegex = re.compile(r"(www.)?([a-zA-z0-9]+)(.com)?")
    my_site = webRegex.search(site).group(2).lower()
    result_str = "Site not saved"
    with open("password.csv", "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            if not row["url"]:
                continue

            stored_site = webRegex.search(row["url"]).group(2).lower()

            if stored_site == my_site:
                result_str = "Username: {} \nPassword: {} \n".format(row["username"], row["password"])
        return result_str

def random_Password(length, with_digits, with_punc):
    letters_only = string.ascii_letters
    letters_digits = string.ascii_letters + string.digits
    letters_punct = string.ascii_letters + string.punctuation

    letters_digits_punct = string.ascii_letters + string.digits + string.punctuation


    if not with_digits and not with_punc:
        random_pass = "".join(random.choice(letters_only) for i in range(int(length)))
    if with_digits and not with_punc:
        random_pass = "".join(random.choice(letters_digits) for i in range(int(length)))
    if not with_digits and with_punc:
        random_pass = "".join(random.choice(letters_punct) for i in range(int(length)))
    if with_digits and with_punc:
        random_pass = "".join(random.choice(letters_digits_punct) for i in range(int(length)))
    return random_pass


def pass_save_window():

    def get_save_values():
        username = username_entry.get()
        password = password_entry.get()
        url = url_entry.get()
        if append_to_csvPassword(username, password, url):
            saved_label.config(text="Password saved")

    save_window = tk.Toplevel()
    save_window.title("Save Password")

    canvas = tk.Canvas(save_window, height="500", width="500")
    canvas.pack()

    save_frame = tk.Frame(save_window, bg="#80c1ff",)
    save_frame.place(relx=0.1, rely=0.1, relwidth=.8, relheight=.8,)

    username_label = tk.Label(save_frame, text="Username:",)
    username_label.place(relx=0.25, rely= 0.33, relwidth=0.25, relheight=0.05, anchor='n')
    username_entry = tk.Entry(save_frame)
    username_entry.place(relx = 0.75, rely=.33, relwidth = .35, relheight = 0.05, anchor='n')

    password_label = tk.Label(save_frame, text="Password:")
    password_label.place(relx=0.25, rely=0.44, relwidth=0.25, relheight=0.05, anchor='n')
    password_entry = tk.Entry(save_frame, show="*")
    password_entry.place(relx=0.75, rely=.44, relwidth=.35, relheight = 0.05, anchor='n')

    url_label = tk.Label(save_frame, text="Website:")
    url_label.place(relx= 0.25, rely=.55, relwidth=0.25, relheight=0.05, anchor='n')
    url_entry = tk.Entry(save_frame)
    url_entry.place(relx=.75, rely=.55, relwidth=.35, relheight = 0.05, anchor='n')

    save_button = tk.Button(save_frame, text = "Save", command=get_save_values)
    save_button.place(relx = .5, rely = .77, relwidth = .5, relheight = 0.08, anchor='n')

    saved_label = tk.Label(save_frame, text="", font=1)
    saved_label.pack(side='bottom')


def find_pass_window():
    def get_find_values():
        var1 = find_entry.get()
        text= find_Password(var1)
        label.config(text=text)

    find_window = tk.Tk()
    find_window.title("Find Password")

    canvas = tk.Canvas(find_window, height="500", width="500")
    canvas.pack()

    find_frame = tk.Frame(find_window, bg="#80c1ff", bd=5)
    find_frame.place(relx=0.5, rely=0.1, relwidth=.75, relheight=0.1, anchor='n')

    find_entry = tk.Entry(find_frame, font=40)
    find_entry.place(relwidth=0.65, relheight=1)

    find_button = tk.Button(find_frame, text="Find", font=40, command=get_find_values)
    find_button.place(relx=0.7, relheight=1, relwidth=0.3)

    lower_frame = tk.Frame(find_window, bg="#80c1ff", bd=10)
    lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor ='n')

    label = tk.Label(lower_frame, font=('Helvetica', 18), justify="left", anchor="nw")
    label.place(relwidth=1, relheight=1)



def pass_generator_window():

    def get_gen_values():
        var1 = how_long.get()
        var2 = wants_digits.get()
        var3 = wants_digits.get()
        password = random_Password(var1, var2, var3)
        pyperclip.copy(password)
        generate_label.config(text=password)
        clipboard_label.config(text="Password copied to clipboard")

    generate_window = tk.Toplevel()
    generate_window.title("Generate Password")

    how_long = tk.DoubleVar()
    wants_digits = tk.BooleanVar()
    wants_pun = tk.BooleanVar()

    canvas = tk.Canvas(generate_window, height="500", width = "500")
    canvas.pack()

    generate_frame = tk.Frame(generate_window, bg="#80c1ff", bd=5)
    generate_frame.place(relx=0.5, rely=0.75, relwidth=.75, relheight=0.1, anchor='n')

    upper_frame = tk.Frame(generate_window, bg="#80c1ff", bd=10)
    upper_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.6, anchor ='n')

    generate_label = tk.Label(generate_frame, font=1)
    generate_label.place(relwidth=0.65, relheight=1,)
    clipboard_label = tk.Label(generate_window, text="", font=1)
    clipboard_label.pack(side='bottom')

    generate_button = tk.Button(generate_frame, text="Generate", command=get_gen_values)
    generate_button.place(relx=0.7, relheight=1, relwidth=0.3,)

    how_many_char_label = tk.Label(upper_frame, text="Charcaters:", font=1)
    how_many_char_label.place(relx= 0.275, rely=.575, anchor='n')
    how_many_char_scale = tk.Scale(upper_frame, variable=how_long, from_=0, to=26, orient="horizontal")
    how_many_char_scale.place(relx=.725, rely=.55, anchor='n')

    wants_digits_cb = tk.Checkbutton(upper_frame, text="Digits", variable=wants_digits, font=1)
    wants_digits_cb.place(relx = 0.5, rely=.25,  anchor='n')

    want_punmarks_cb = tk.Checkbutton(upper_frame, text="Special characters", onvalue=1, offvalue=0,font=1, variable=wants_pun)
    want_punmarks_cb.place(relx=0.5, rely=.4,  anchor='n')

main_root = tk.Tk()

main_root.title("PasswordManager")

canvas = tk.Canvas(main_root, height="500", width="500")
canvas.pack()


main_frame = tk.Frame(main_root, bg="#80c1ff")
main_frame.place(relx=0.5, rely=0.1, relwidth=.8, relheight=.8, anchor='n')

save_button = tk.Button(main_frame, text="Save Passsword", command=pass_save_window)
save_button.place(relx=0.5,rely=.17, relwidth=.5, relheight=0.08, anchor='n')

find_button = tk.Button(main_frame, text="Find Password", command=find_pass_window)
find_button.place(relx=0.5,rely=.42 ,relwidth=.5, relheight=0.08, anchor='n')

generate_button = tk.Button(main_frame, text="Generate Password", command=pass_generator_window)
generate_button.place(relx=0.5, rely=.67, relwidth=.5, relheight=.08, anchor='n')

main_root.mainloop()
