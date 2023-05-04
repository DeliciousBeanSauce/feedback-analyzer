import random
from faker import Faker
from datetime import datetime, timedelta
import csv

fake = Faker()

ratings = list(range(11))
comments = [
    "Great website! User-friendly and clean design.",
    "The website is very informative, and the layout is well-organized.",
    "Easy navigation, but the color scheme could be improved.",
    "Fantastic user experience! The website is fast and responsive.",
    "The website has interesting content, but it's difficult to read on a mobile device.",
    "The website loads slowly, and some images are broken.",
    "Nice design, but I encountered a few broken links.",
    "The website is mobile-friendly, but the content seems outdated.",
    "Amazing customer support! They were very helpful.",
    "The website has a wide variety of products, but the search functionality needs improvement.",
    "The fonts are too small and hard to read.",
    "The website has a great color scheme and overall design.",
    "I like the website's layout, but the navigation could be better.",
    "The content is engaging and well-structured.",
    "Some of the website's features don't work well on my device."
]

log_entries = []

for _ in range(50):
    date_time = fake.date_time_this_year()
    rating = random.choice(ratings)
    comment = random.choice(comments)
    log_entries.append((date_time.strftime('%Y-%m-%d@%H:%M'), rating, comment))

with open('feedback.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for entry in log_entries:
        writer.writerow(entry)
