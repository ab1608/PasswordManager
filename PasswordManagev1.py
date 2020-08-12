import os, csv, string, random, re, sys, pathlib
import tkinter as tk
from tkinter import filedialog, Text
from pathlib import Path

user_dir = str(Path.home())
app_dir = "\\Documents\\PasswordManager"
pathlib.Path(user_dir+app_dir).mkdir(parents=True, exist_ok=True, )
os.chdir(user_dir + app_dir)
csv_file_exists = os.path.isfile("password.csv")



def main():
    main_Frame()

# Store username, password, url into a csv file
def append_to_csvPassword(username, password, url):
    with open ("password.csv", "a", newline="") as csv_file:
        fieldnames = ["username", "password", "url"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not csv_file_exists:
            csv_writer.writeheader()

        csv_writer.writerow({"username": username, "password": password, "url" : url})
        my_label = save_Frame()
        my_label['text'] = "Password saved."


def random_Password(length, with_digits, with_punc):
    letters_only = string.ascii_letters
    letters_digits = string.ascii_letters + string.digits
    letters_digits_punct = string.ascii_letters + string.digits + string.punctuation

    if int(length) < 20:
        if (with_digits.lower() in ["no", "n"] and with_punc.lower() in ["no", "n"]):
            random_pass = "".join(random.choice(letters_only) for i in range(int(length)))
        if (with_digits.lower() in ["yes", "y"] and with_punc.lower() in ["no", "n"]):
            random_pass = "".join(random.choice(letters_digits) for i in range(int(length)))
        if (with_digits.lower() in ["yes", "y"] and with_punc.lower() in ["yes", "y"]):
            random_pass = "".join(random.choice(letters_digits_punct) for i in range(int(length)))

        # print(f"Your random password of {length} is {random_pass}")
        my_label = generate_Frame()
        my_label['text'] = f"{random_pass}"

        return random_pass
    else:
        raise ("Passwords greater than 20 characters are not supported at this time.")


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

    my_label = find_Frame()
    my_label['text'] = result_str


def main_Frame():
    main_root = tk.Tk()

    main_root.title("PasswordManager")

    canvas = tk.Canvas(main_root, height="500", width="500")
    canvas.pack()

    main_frame = tk.Frame(main_root, bg="#80c1ff")
    main_frame.place(relx=0.5, rely=0.1, relwidth=.8, relheight=.8, anchor='n')

    save_button = tk.Button(main_frame, text="Save Passsword", command=lambda: save_Frame())
    save_button.place(relx=0.5,rely=.17, relwidth=.5, relheight=0.08, anchor='n')

    find_button = tk.Button(main_frame, text="Find Password", command=lambda: find_Frame())
    find_button.place(relx=0.5,rely=.42 ,relwidth=.5, relheight=0.08, anchor='n')

    generate_button = tk.Button(main_frame, text="Generate Password", command=lambda: generate_Frame())
    generate_button.place(relx=0.5, rely=.67, relwidth=.5, relheight=.08, anchor='n')

    main_root.mainloop()

def save_Frame():

    save_root = tk.Tk()
    save_root.title("Save Password")

    canvas = tk.Canvas(save_root, height="500", width="500")
    canvas.pack()

    save_frame = tk.Frame(save_root, bg="#80c1ff",)
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

    save_button = tk.Button(save_frame, text = "Save", command = lambda:append_to_csvPassword(username_entry.get(), password_entry.get(), url_entry.get()))
    save_button.place(relx = .5, rely = .77, relwidth = .5, relheight = 0.08, anchor='n')

    saved_label = tk.Label(save_frame, text="         ")
    saved_label.pack(side='bottom')
    return saved_label

    save_root.mainloop()


def find_Frame():

    find_root = tk.Tk()
    find_root.title("Find Password")

    canvas = tk.Canvas(find_root, height="500", width="500")
    canvas.pack()

    find_frame = tk.Frame(find_root, bg="#80c1ff", bd=5)
    find_frame.place(relx=0.5, rely=0.1, relwidth=.75, relheight=0.1, anchor='n')

    find_entry = tk.Entry(find_frame, font=40)
    find_entry.place(relwidth=0.65, relheight=1)

    find_button = tk.Button(find_frame, text="Find", font=40, command=lambda: find_Password(find_entry.get()))
    find_button.place(relx=0.7, relheight=1, relwidth=0.3)

    lower_frame = tk.Frame(find_root, bg="#80c1ff", bd=10)
    lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor ='n')

    label = tk.Label(lower_frame, font=('Helvetica', 18), justify="left", anchor="nw")
    label.place(relwidth=1, relheight=1)
    return label
    find_root.mainloop()




def generate_Frame():

    generate_root = tk.Tk()
    generate_root.title("Generate Password")

    canvas = tk.Canvas(generate_root, height="500", width = "500")
    canvas.pack()

    generate_frame = tk.Frame(generate_root, bg="#80c1ff", bd=5)
    generate_frame.place(relx=0.5, rely=0.75, relwidth=.75, relheight=0.1, anchor='n')

    upper_frame = tk.Frame(generate_root, bg="#80c1ff", bd=10)
    upper_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.6, anchor ='n')


    generate_button = tk.Button(generate_frame, text="Generate", command= lambda: random_Password(how_many_char_entry.get(), want_digits_entry.get(), want_punmarks_entry.get()))
    generate_button.place(relx=0.7, relheight=1, relwidth=0.3,)

    how_many_char_label = tk.Label(upper_frame, text="How many characters? (0-20)")
    how_many_char_label.place(relx= 0.25, rely=.55, relwidth=0.4, relheight=0.08, anchor='n')
    how_many_char_entry = tk.Entry(upper_frame, font=20)
    how_many_char_entry.place(relx=.75, rely=.55, relwidth=.35, relheight = 0.08, anchor='n')

    wants_digits_label = tk.Label(upper_frame, text="Digits (y/n): ")
    wants_digits_label.place(relx=0.25, rely= 0.33, relwidth=0.4, relheight=0.08, anchor='n')
    want_digits_entry = tk.Entry(upper_frame, font=20)
    want_digits_entry.place(relx = 0.75, rely=.33, relwidth = .35, relheight = 0.08, anchor='n')

    want_punmarks_label = tk.Label(upper_frame, text="Special character (y/n):")
    want_punmarks_label.place(relx=0.25, rely=0.44, relwidth=0.4, relheight=0.08, anchor='n')
    want_punmarks_entry = tk.Entry(upper_frame, font=20)
    want_punmarks_entry.place(relx=0.75, rely=.44, relwidth=.35, relheight = 0.08, anchor='n')

    generate_label = tk.Label(generate_frame, font=1)
    generate_label.place(relwidth=0.65, relheight=1,)
    return generate_label


    generate_root.mainloop()

main()




