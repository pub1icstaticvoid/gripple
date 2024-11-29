"""Death Gripple main program."""
import tkinter as tk
import tkinter.font as tkFont
import json
import random
from PIL import ImageTk, Image

f = open("dg_data.json", encoding="utf-8")
dg_data = json.load(f)
VALUES = list(dg_data["track"].keys())
VALUES.sort()
rand_song = VALUES[random.randrange(0, len(VALUES))]
f.close()

class App:
    """Includes window set up and methods for Death Gripple."""
    def __init__(self, root:tk.Tk):
        #setting title
        self.root = root
        root.title("Death Gripple")
        #setting window size
        width=600
        height=600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times',size=10)
        self.correct_song = rand_song
        self.attempt = 0

        self.search_bar = tk.Entry(root, borderwidth="1px", font=ft,
                                   fg="#333333", justify="center")
        self.search_bar.place(x=130,y=230,width=300,height=30)
        self.search_bar.insert(0, "Enter a Death Grips song here...")
        self.search_bar.config(state="normal", fg="gray")

        self.search_res = tk.Listbox(root, borderwidth="1px", font=ft,
                                     fg="#333333",justify="left", selectmode="single")
        self.search_res.place(x=130,y=260,width=300,height=92)
        self.search_res.config(state="normal")

        self.upper_label = tk.Label(root, font=ft, fg="#333333",
                                    justify="center",text="Death Gripple")
        self.upper_label.place(x=180,y=0,width=211,height=37)

        self.submit = tk.Button(root, bg="#f0f0f0", font=ft,
                                fg="#000000", justify="center",
                                text="Submit", command=self.submit_song)
        self.submit.place(x=450,y=230,width=70,height=25)

        self.album_label = tk.Label(root, font=ft, fg="#333333",
                                    justify="center", text="Album",
                                    borderwidth=1, relief="solid",
                                    bg="white")
        self.album_label.place(x=10, y=380, width=200, height=30)

        self.album_text = tk.Text(root, wrap="word")
        self.album_text.config(state="disabled")
        self.album_text.tag_config("yellow", background="yellow")
        self.album_text.tag_config("green", background="green2")
        self.album_text.place(x=10, y=415, width=200, height=160)

        self.tracknum_label = tk.Label(root, font=ft, fg="#333333",
                                    justify="center", text="Track No.",
                                    borderwidth=1, relief="solid",
                                    bg="white")
        self.tracknum_label.place(x=220, y=380, width=75, height=30)

        self.tracknum_text = tk.Text(root, wrap="word")
        self.tracknum_text.config(state="disabled")
        self.tracknum_text.tag_config("yellow", background="yellow")
        self.tracknum_text.tag_config("green", background="green2")
        self.tracknum_text.place(x=220, y=415, width=75, height=160)

        self.track_label = tk.Label(root, font=ft, fg="#333333",
                                    justify="center", text="Track Title",
                                    borderwidth=1, relief="solid",
                                    bg="white")
        self.track_label.place(x=305, y=380, width=280, height=30)

        self.track_text = tk.Text(root, wrap="word")
        self.track_text.config(state="disabled")
        self.track_text.tag_config("green", background="green2")
        self.track_text.tag_config("yellow", background="yellow")
        self.track_text.place(x=305, y=415, width=280, height=160)

        self.attempt_label = tk.Label(root, font=ft, fg="#333333",
                                    justify="center", text="Attempts",
                                    borderwidth=1, relief="solid",
                                    bg="white")
        self.attempt_label.place(x=30, y=60, width=100, height=30)

        self.attempt_text = tk.Text(root, wrap="word")
        self.attempt_text.place(x=30, y=100, width=100, height=30)
        self.attempt_text.insert("1.0", f"{self.attempt}/6")
        self.attempt_text.config(state="disabled")

        self.ride_jpg = Image.open("mc_ride.jpg")
        self.ride_jpg = self.ride_jpg.resize((200,150))
        self.ride_jpg = ImageTk.PhotoImage(self.ride_jpg)
        self.mc_ride = tk.Label(root, image=self.ride_jpg)
        self.mc_ride.image = self.ride_jpg
        self.mc_ride.place(x=185, y=45, width=200, height=150)

        self.search_bar.bind("<Any-KeyRelease>", self.filter)
        self.search_res.bind("<<ListboxSelect>>", self.song_select)
        self.search_bar.bind("<FocusIn>", self.temp_text)
        self.search_bar.bind("<FocusOut>", self.on_focus_out)

        self.filter()

    def temp_text(self, event=None):
        """Deletes temporary text once user selects search bar."""
        if self.search_bar.get() == "Enter a Death Grips song here...":
            self.search_bar.config(fg="black")
            self.search_bar.delete(0, "end")
            self.search_bar.insert(0, "")

    def on_focus_out(self, event=None):
        """Adds back temporary text once user clicks out."""
        if self.search_bar.get() == "":
            self.search_bar.insert(0, "Enter a Death Grips song here...")
            self.search_bar.config(fg="gray")

    def submit_song(self):
        """Submits song to be compared to correct song."""
        guess_song = self.search_bar.get()
        if guess_song in VALUES:
            self.album_check(dg_data["track"][guess_song]["album"])
            self.track_check(guess_song)
            self.search_bar.delete(0, "end")
            self.set_attempt()
        else:
            self.search_bar.delete(0, "end")

    def filter(self, event=None):
        """Filters out search results."""
        pattern = self.search_bar.get().lower()
        self.search_res.delete(0, "end")
        filtered = [value for value in VALUES if value.lower().startswith(pattern)]
        self.search_res.insert("end", *filtered)

    def song_select(self, event=None):
        """Selects song from list box."""
        song = self.search_res.get("anchor")
        self.search_bar.delete(0, "end")
        self.search_bar.insert(0, song)

    def set_attempt(self):
        """Sets attempt count."""
        self.attempt += 1
        if self.attempt == 7:
            self.no_more_attempts()
        else:
            self.attempt_text.config(state="normal")
            self.attempt_text.delete("1.0", "end")
            self.attempt_text.insert("1.0", f"{self.attempt}/6")
            self.attempt_text.config(state="disabled")

    def album_check(self, album):
        """Sets album name."""
        correct_song_album = dg_data["track"][self.correct_song]["album"]
        correct_album_val = int(dg_data["album"][correct_song_album])
        self.album_text.config(state="normal")
        if album == correct_song_album:
            self.album_text.insert("end", album + "\n\n", "green")
        elif int(dg_data["album"][album]) in range(correct_album_val - 2, correct_album_val + 3):
            arrow = self.arrow_album(album, correct_song_album)
            self.album_text.insert("end", arrow + album + "\n\n", "yellow")
        else:
            arrow = self.arrow_album(album, correct_song_album)
            self.album_text.insert("end", arrow + album + "\n\n")
        self.album_text.config(state="disabled")

    def track_check(self, track):
        """Sets track name and number."""
        tracknum = dg_data["track"][track]["num"]
        correct_tracknum = dg_data["track"][self.correct_song]["num"]
        self.track_text.config(state="normal")
        self.tracknum_text.config(state="normal")
        if track == self.correct_song:
            self.track_text.insert("end", track + "\n\n", "green")
            self.tracknum_text.insert("end", tracknum + "\n\n", "green")
            self.win()
        elif int(tracknum) in range(int(correct_tracknum) - 2, int(correct_tracknum) + 3):
            if tracknum == correct_tracknum:
                arrow = self.arrow_track(tracknum, correct_tracknum)
                self.tracknum_text.insert("end", tracknum + "\n\n", "green")
                if dg_data["track"][track]["album"] == dg_data["track"][self.correct_song]["album"]:
                    self.track_text.insert("end", arrow + track + "\n\n", "yellow")
                else:
                    self.track_text.insert("end", arrow + track + "\n\n")
            else:
                arrow = self.arrow_track(tracknum, correct_tracknum)
                self.track_text.insert("end", arrow + track + "\n\n", "yellow")
                self.tracknum_text.insert("end", arrow + tracknum + "\n\n", "yellow")
        else:
            arrow = self.arrow_track(tracknum, correct_tracknum)
            self.track_text.insert("end", arrow + track + "\n\n")
            self.tracknum_text.insert("end", arrow + tracknum + "\n\n")
        self.track_text.config(state="disabled")
        self.tracknum_text.config(state="disabled")

    def arrow_album(self, album, correct_album):
        """Sets arrow to point up or down for albums."""
        if int(dg_data["album"][album]) < int(dg_data["album"][correct_album]):
            return "| ▲ | "
        return "| ▼ | "

    def arrow_track(self, tracknum, correct_tracknum):
        """Sets arrow to point up or down for albums."""
        if int(tracknum) < int(correct_tracknum):
            return "| ▼ | "
        if int(tracknum) == int(correct_tracknum):
            return ""
        return "| ▲ | "

    def no_more_attempts(self):
        """Window shows up if you are trash."""
        self.search_bar.config(state="disabled")
        self.search_res.config(state="disabled")
        self.submit.config(state="disabled")
        l_window = tk.Toplevel(master=self.root)
        l_window.title("Game Over")
        width=400
        height=400
        screenwidth = l_window.winfo_screenwidth()
        screenheight = l_window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        l_window.geometry(alignstr)
        l_window.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times',size=10)

        l_title = tk.Label(l_window, font=ft, fg="#333333",
                           justify="center", text="Death Gripple: GAME OVER")
        l_title.place(x=110, y=0, width=180, height=25)

        album_title = str(dg_data["track"][self.correct_song]["album"])
        album_title = album_title.replace(" ", "_")
        l_album_art = Image.open(f"{album_title}.jpg")
        l_album_art = l_album_art.resize((150,150))
        l_album_art = ImageTk.PhotoImage(l_album_art)
        l_cover = tk.Label(l_window, image=l_album_art)
        l_cover.image = l_album_art
        l_cover.place(x=120, y=40, width=150, height=150)

        result = f"The correct answer is '{self.correct_song}' from '{dg_data["track"][self.correct_song]["album"]}'"
        l_results = tk.Text(l_window, wrap="word")
        l_results.place(x=60, y=200, width=276, height=60)
        l_results.insert("end", result)
        l_results.config(state="disabled")

        l_again_text = tk.Label(l_window, font=ft, fg="#333333",
                           justify="center", text="Play Again?")
        l_again_text.place(x=110, y=270, width=180, height=30)

        l_yes_btn = tk.Button(l_window, bg="#f0f0f0", font=ft,
                              fg="#000000", justify="center",
                              text="Yes", command=self.play_again)
        l_yes_btn.place(x=70, y=320, width=70, height=25)

        l_no_btn = tk.Button(l_window, bg="#f0f0f0", font=ft,
                              fg="#000000", justify="center",
                              text="No", command=self.quit)
        l_no_btn.place(x=250, y=320, width=70, height=25)

    def quit(self):
        """Quits application."""
        self.root.destroy()

    def play_again(self):
        """Runs the game again."""
        global rand_song
        self.root.destroy()
        rand_song = VALUES[random.randrange(0, len(VALUES))]
        root = tk.Tk()
        thing = App(root)
        root.mainloop()

    def win(self):
        "Window shows up when you get the dub."
        self.search_bar.config(state="disabled")
        self.search_res.config(state="disabled")
        self.submit.config(state="disabled")
        w_window = tk.Toplevel(master=self.root)
        w_window.title("You Win")
        width=400
        height=400
        screenwidth = w_window.winfo_screenwidth()
        screenheight = w_window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        w_window.geometry(alignstr)
        w_window.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times',size=10)

        w_title = tk.Label(w_window, font=ft, fg="#333333",
                           justify="center", text="Death Gripple: YOU WIN")
        w_title.place(x=110, y=0, width=180, height=25)

        album_title = str(dg_data["track"][self.correct_song]["album"])
        album_title = album_title.replace(" ", "_")
        w_album_art = Image.open(f"{album_title}.jpg")
        w_album_art = w_album_art.resize((150,150))
        w_album_art = ImageTk.PhotoImage(w_album_art)
        w_cover = tk.Label(w_window, image=w_album_art)
        w_cover.image = w_album_art
        w_cover.place(x=120, y=40, width=150, height=150)

        result = f"The correct answer is '{self.correct_song}' from '{dg_data["track"][self.correct_song]["album"]}'"
        w_results = tk.Text(w_window, wrap="word")
        w_results.place(x=60, y=200, width=276, height=60)
        w_results.insert("end", result)
        w_results.config(state="disabled")

        w_again_text = tk.Label(w_window, font=ft, fg="#333333",
                           justify="center", text="Play Again?")
        w_again_text.place(x=110, y=270, width=180, height=30)

        w_yes_btn = tk.Button(w_window, bg="#f0f0f0", font=ft,
                              fg="#000000", justify="center",
                              text="Yes", command=self.play_again)
        w_yes_btn.place(x=70, y=320, width=70, height=25)

        w_no_btn = tk.Button(w_window, bg="#f0f0f0", font=ft,
                              fg="#000000", justify="center",
                              text="No", command=self.quit)
        w_no_btn.place(x=250, y=320, width=70, height=25)


if __name__ == "__main__":
    main = tk.Tk()
    app = App(main)
    main.mainloop()
