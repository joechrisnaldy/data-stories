"""Build club_country.csv: map each club in the data to the country of the league
it plays in (league-country rule, so Monaco->France, Swansea->England,
Auckland FC->Australia). Names are normalized on both sides (accents, punctuation,
Nordic letters) so the join is robust; anything unmatched is reported, never dropped
silently."""
import re
import unicodedata
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent

GROUPS = {
    "England": ["Arsenal", "Aston Villa", "Birmingham City", "Bournemouth", "Brentford",
                "Brighton", "Burnley", "Charlton Athletic", "Chelsea", "Crystal Palace",
                "Everton", "Fulham", "Hull City", "Ipswich Town", "Leeds United",
                "Leicester City", "Liverpool", "Manchester City", "Manchester Utd",
                "Middlesbrough", "Millwall", "Newcastle", "Norwich City", "Nottingham",
                "Sheffield United", "Sunderland", "Swansea City", "Tottenham", "Watford",
                "West Ham", "Wolves", "Wrexham"],
    "Spain": ["Athletic Club", "Atletico Madrid", "Barcelona", "Cultural Leonesa", "Girona",
              "Granada", "Mallorca", "Oviedo", "Rayo Vallecano", "Real Betis", "Real Madrid",
              "Real Sociedad", "Sevilla", "Villarreal"],
    "Italy": ["Atalanta", "Bologna", "Como", "Cremonese", "Genoa", "Hellas Verona", "Inter",
              "Juventus", "Milan", "Napoli", "Parma", "Pisa", "Roma", "Sassuolo", "Torino",
              "Udinese", "Venezia"],
    "Germany": ["Augsburg", "Bayern Munich", "Dortmund", "Frankfurt", "Freiburg", "Gladbach",
                "Hamburger SV", "Hannover 96", "Hoffenheim", "Holstein Kiel", "Karlsruher",
                "Leverkusen", "Mainz 05", "RB Leipzig", "Schalke 04", "St Pauli", "Stuttgart",
                "Union Berlin", "Werder Bremen", "Wolfsburg"],
    "France": ["Angers", "Auxerre", "Bastia", "Lens", "Lille", "Lorient", "Lyon", "Marseille",
               "Monaco", "Nancy", "Nice", "PSG", "Reims", "Rennes", "Saint-Etienne",
               "Strasbourg"],
    "Netherlands": ["Ajax", "Almere City", "Feyenoord", "NEC Nijmegen", "PSV", "Twente",
                    "Utrecht", "Volendam", "Zwolle"],
    "Belgium": ["Beveren", "Club Brugge", "Genk", "Sint-Truiden", "Union SG"],
    "Portugal": ["Benfica", "Braga", "Casa Pia", "Estrela", "Gil Vicente FC", "Porto",
                 "Sporting CP", "Tondela", "Vit. Guimaraes"],
    "Turkey": ["Basaksehir", "Besiktas", "Fenerbahce", "Galatasaray", "Konyaspor", "Rizespor",
               "Trabzonspor"],
    "Saudi Arabia": ["Al-Ahli", "Al-Ettifaq", "Al-Hilal", "Al-Ittihad", "Al-Najma", "Al-Nassr",
                     "Al-Qadsiah", "Al-Shabab", "Al-Ula", "Neom"],
    "USA": ["Atlanta Utd", "Charlotte", "Chicago Fire", "Columbus Crew", "FC Dallas",
            "Inter Miami", "LAFC", "Miami FC", "Minnesota Utd", "Nashville SC", "NYCFC",
            "Orlando City", "Philadelphia", "Portland Timbers"],
    "Canada": ["Toronto FC", "Vancouver"],
    "Mexico": ["America", "Atletico San Luis", "Cruz Azul", "Guadalajara", "Pachuca",
               "Tijuana", "Toluca", "UNAM"],
    "Brazil": ["Atletico Mineiro", "Botafogo-RJ", "Corinthians", "Flamengo", "Fluminense",
               "Palmeiras", "Sao Paulo"],
    "Argentina": ["Huracan", "Ind. Rivadavia", "River Plate", "San Lorenzo"],
    "Paraguay": ["Cerro Porteno"],
    "Ecuador": ["LDU Quito"],
    "Austria": ["Austria Wien", "Grazer AK", "LASK", "RB Salzburg"],
    "Switzerland": ["Lugano", "Young Boys", "Zurich"],
    "Scotland": ["Celtic", "Hearts", "Hibernian", "Kilmarnock", "Motherwell", "Rangers"],
    "Ireland": ["Shamrock"],
    "Norway": ["Bodo/Glimt", "Viking"],
    "Sweden": ["AIK Stockholm", "Mjallby"],
    "Denmark": ["Brondby", "FC Copenhagen", "Midtjylland", "Nordsjaelland", "Silkeborg"],
    "Greece": ["AE Kifisia", "Olympiacos"],
    "Czechia": ["Slavia Prague", "Sparta Prague", "Viktoria Plzen"],
    "Hungary": ["Ferencvaros", "Puskas Akad."],
    "Poland": ["Cracovia", "Pogon Szczecin"],
    "Romania": ["FCSB", "Univ. Cluj"],
    "Bulgaria": ["Ludogorets"],
    "Serbia": ["Red Star"],
    "Russia": ["Dynamo Moskva", "Krasnodar", "Loko Moscow", "Rostov", "Zenit"],
    "Iran": ["Foolad", "Persepolis", "Sepahan", "Tractor"],
    "South Korea": ["FC Seoul", "Gangwon FC", "Jeonbuk"],
    "Japan": ["FC Tokyo", "Machida Zelvia"],
    "China": ["Zhejiang"],
    "South Africa": ["Orlando Pirates", "Sundowns"],
    "Australia": ["Auckland FC", "Melb City", "Melb. Victory", "Sydney FC", "Wellington"],
}

_SPECIAL = {"ø": "o", "Ø": "o", "æ": "ae", "Æ": "ae", "đ": "d", "ð": "d", "ł": "l", "ß": "ss"}


def norm(s):
    s = str(s)
    for k, v in _SPECIAL.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


# Build normalized lookup; detect collisions in my own list
lookup = {}
collisions = []
for country, clubs in GROUPS.items():
    for c in clubs:
        k = norm(c)
        if k in lookup:
            collisions.append((c, lookup[k], country))
        lookup[k] = country
print("GROUPS clubs:", sum(len(v) for v in GROUPS.values()), "| unique normalized:", len(lookup))
if collisions:
    print("!! COLLISIONS in GROUPS:", collisions)

# Map the actual data clubs
p = pd.read_csv(BASE / "data" / "players.csv")
played = p[p.games.fillna(0) > 0]
data_clubs = sorted(played.club.dropna().unique())
rows, unmapped = [], []
for club in data_clubs:
    country = lookup.get(norm(club))
    if country is None:
        unmapped.append(club)
    else:
        rows.append({"club": club, "country": country})

pd.DataFrame(rows).to_csv(BASE / "club_country.csv", index=False)
print(f"\ndata clubs: {len(data_clubs)} | mapped: {len(rows)} | UNMAPPED: {len(unmapped)}")
if unmapped:
    print("UNMAPPED (fix these):", unmapped)

# GROUPS entries that never matched a data club (my typos / extras)
data_keys = {norm(c) for c in data_clubs}
never = sorted([c for cs in GROUPS.values() for c in cs if norm(c) not in data_keys])
if never:
    print("GROUPS entries not in data (typo/extra):", never)

# Diagnostics for ambiguous clubs: which national teams employ them
for amb in ["Red Star", "Miami FC", "Neom", "Auckland FC", "Wellington"]:
    sub = played[played.club == amb]
    if len(sub):
        print(f"  [{amb}] -> nations:", sorted(sub.team.unique()))
