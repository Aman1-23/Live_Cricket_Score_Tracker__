"""
CricScore - Live Cricket Score Tracker
========================================
A desktop GUI application built with Tkinter that scrapes Cricbuzz.com
in real time and displays live match scores, summaries, and status
for all ongoing/upcoming cricket matches.

Author  : Aman Kumar
GitHub  : https://github.com/Aman1-23
LinkedIn: https://linkedin.com/in/aman-kumar-96a28a372

Core Concepts Demonstrated
---------------------------
1. Object-Oriented Programming (OOP)   -> CricketScore class encapsulates state & behavior
2. GUI Development                     -> Tkinter widgets (Label, Combobox, Button, Frame)
3. Web Scraping                        -> BeautifulSoup (bs4) HTML parsing
4. HTTP Requests                       -> requests module to fetch live page content
5. Regex                               -> Extracting team names from raw scraped strings
"""

from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk
from bs4 import BeautifulSoup
import requests
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "cric.jpg")
SOURCE_URL = "https://www.cricbuzz.com/"


class CricketScore:
    """
    Encapsulates the entire GUI + scraping logic for the live
    cricket score tracker application.
    """

    def __init__(self, rootWindow):
        self.rootWindow = rootWindow
        self.rootWindow.title("LIVE CRICKET SCORE")
        self.rootWindow.geometry("800x500")

        # --- Background image ---
        self.bg = ImageTk.PhotoImage(file=BG_IMAGE_PATH)
        Label(self.rootWindow, image=self.bg).place(x=0, y=0)

        # --- Heading ---
        Label(
            self.rootWindow,
            text="Live Matches",
            font=("times new roman", 60),
            compound="center",
        ).pack(padx=100, pady=50)

        # --- Match selector dropdown ---
        self.var = StringVar()
        self.matches = self.match_details()
        self.data = list(self.matches.keys())
        self.cb = Combobox(self.rootWindow, values=self.data, width=50)
        self.cb.place(x=250, y=200)

        # --- Check Score button ---
        Button(
            self.rootWindow,
            text="Check Score",
            font=("times new roman", 15),
            command=self.show_match_details,
        ).place(x=50, y=380)

    def select(self):
        """Returns the currently selected match from the dropdown."""
        return self.cb.get()

    def scrap(self):
        """
        Sends an HTTP GET request to Cricbuzz's homepage and returns
        the list of raw match-card HTML elements.
        """
        page = requests.get(SOURCE_URL, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="match_menu_container")
        return results.find_all("li", class_="cb-match-card") if results else []

    def match_details(self):
        """
        Parses every scraped match card into a clean dictionary keyed
        by "Team A vs Team B" containing summary, header, and score.
        """
        details = self.scrap()
        live_match = {}
        for detail in details:
            summary = self.match_summary(detail)
            if summary is not None:
                match_header = self.match_header(detail).text
                teams = self.teams_name(detail)
                score_card = self.team_score(detail)

                live_match[f"{teams[0]} vs {teams[1]}"] = {
                    "summary": summary.text,
                    "match_header": match_header,
                    "score_card": f"{score_card[0]} :: {score_card[1]}",
                }
        return live_match

    def match_summary(self, detail):
        return detail.find("div", class_="cb-mtch-crd-state")

    def match_header(self, detail):
        return detail.find("div", class_="cb-mtch-crd-hdr")

    def teams_name(self, detail):
        """Extracts clean team names by stripping the trailing score digits."""
        team1_raw = detail.find("div", class_="cb-hmscg-bat-txt").text
        team2_raw = detail.find("div", class_="cb-hmscg-bwl-txt").text

        team1_idx = re.search(r"\d", team1_raw)
        team2_idx = re.search(r"\d", team2_raw)

        team1 = team1_raw[: team1_idx.start()] if team1_idx else team1_raw
        team2 = team2_raw[: team2_idx.start()] if team2_idx else team2_raw
        return [team1, team2]

    def team_score(self, detail):
        team1_raw = detail.find("div", class_="cb-hmscg-bat-txt").text
        team2_raw = detail.find("div", class_="cb-hmscg-bwl-txt").text
        return [team1_raw, team2_raw]

    def show_match_details(self):
        """Renders the score/summary panel for the selected match."""
        self.frame1 = Frame(self.rootWindow, bg="#ADD8E6")
        self.frame1.place(x=180, y=280, width=600, height=200)

        selected = self.select()
        if selected not in self.matches:
            return
        x = self.matches[selected]

        Label(
            self.frame1,
            text=f"{selected} - {x['match_header']}",
            font=("times new roman", 15, "bold"),
            bg="#ADD8E6",
            fg="red",
        ).place(x=150, y=15)

        Label(
            self.frame1,
            text="Score Details : ",
            font=("times new roman", 10, "bold"),
            bg="#ADD8E6",
        ).place(x=10, y=40)
        Label(
            self.frame1,
            text=x["score_card"],
            font=("times new roman", 10, "bold"),
            bg="#ADD8E6",
        ).place(x=20, y=60)

        Label(
            self.frame1,
            text="Summary : ",
            font=("times new roman", 10, "bold"),
            bg="#ADD8E6",
        ).place(x=10, y=100)
        Label(
            self.frame1,
            text=x["summary"],
            font=("times new roman", 10, "bold"),
            bg="#ADD8E6",
        ).place(x=20, y=120)


def main():
    rootWindow = Tk()
    CricketScore(rootWindow)
    rootWindow.mainloop()


if __name__ == "__main__":
    main()
