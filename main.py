import requests
import json
from datetime import datetime, timedelta
from gtts import gTTS
import os
import pygame
from kivy.app import App
from kivy.uix.button import Button

def get_next_match():
    url = "https://cricbuzz-cricket.p.rapidapi.com/teams/v1/97/schedule"
    headers = {
        "x-rapidapi-key": "a3e85cb9ffmshf6035815f299412p121fa1jsn00c8749e99c7",  # Replace with your actual API key
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        today = datetime.utcnow()  
        today_date = today.date()
        next_match = None

        if 'teamMatchesData' in data and len(data['teamMatchesData']) > 0:
            for match_group in data['teamMatchesData']:
                if 'matchDetailsMap' in match_group:
                    match_details_map = match_group['matchDetailsMap']
                    
                    if 'match' in match_details_map:
                        for match_detail in match_details_map['match']:
                            match_info = match_detail['matchInfo']
                            match_start_timestamp = int(match_info['startDate']) // 1000
                            match_start_datetime = datetime.utcfromtimestamp(match_start_timestamp)
                            match_start_ist = match_start_datetime + timedelta(hours=5, minutes=30)

                            if match_start_ist.date() >= today_date:
                                team1 = match_info['team1']['teamName']
                                team2 = match_info['team2']['teamName']
                                match_time_ist = match_start_ist.strftime('%Y-%m-%d %H:%M:%S IST')
                                
                                if next_match is None or match_start_ist < next_match['date']:
                                    next_match = {
                                        'team1': team1,
                                        'team2': team2,
                                        'time': match_time_ist,
                                        'date': match_start_ist
                                    }

        if next_match:
            return f"Hello Ajaybhai, the next match of India is between {next_match['team2']} and it starts on {next_match['time']}."
    
    return "No upcoming match found for India."

def speak_in_malayalam(text):
    tts = gTTS(text=text, lang='ml')
    tts.save("next_match.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("next_match.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        continue
    
    os.remove("next_match.mp3")

class MyApp(App):
    def build(self):
        button = Button(text='Fetch Next Match', on_press=self.fetch_next_match)
        return button

    def fetch_next_match(self, instance):
        result = get_next_match()
        print(result)
        speak_in_malayalam(result)

if __name__ == '__main__':
    MyApp().run()
