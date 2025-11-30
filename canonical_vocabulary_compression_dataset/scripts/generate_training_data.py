#!/usr/bin/env python3
"""
Generate comprehensive training dataset for CVC
Creates diverse sentences with varied synonym usage
"""

import random
import json

# Load synonym mappings
with open('../mappings/synonym_to_canonical.json', 'r') as f:
    mappings = json.load(f)

# Sentence templates with synonym slots
sentence_templates = [
    # Size descriptions
    "The {size_big} building dominated the city skyline.",
    "She lived in a {size_small} apartment near the park.",
    "They discovered a {size_big} cave in the mountains.",
    "The {size_small} details made all the difference.",

    # Emotional states
    "He felt {emotion_happy} about the recent developments.",
    "The {emotion_sad} news spread quickly through the community.",
    "Her {emotion_angry} response surprised everyone.",
    "They were {emotion_happy} to announce the results.",

    # Intelligence and ability
    "The {intelligence} student solved the problem quickly.",
    "It was a {intelligence} decision to invest early.",
    "Her {intelligence} analysis impressed the committee.",

    # Speed and motion
    "The {speed_fast} response prevented further damage.",
    "Progress was {speed_slow} but steady.",
    "They moved at a {speed_fast} pace through the project.",
    "The {speed_slow} recovery took months.",

    # Actions and verbs
    "She {verb_say} her concerns clearly.",
    "They {verb_walk} through the historic district.",
    "He {verb_run} to catch the departing train.",
    "The team {verb_make} significant progress.",
    "They {verb_help} local communities in need.",
    "The company {verb_show} impressive quarterly results.",

    # Quality descriptions
    "The {quality_good} performance exceeded expectations.",
    "That was a {quality_bad} decision in retrospect.",
    "They delivered {quality_good} results consistently.",

    # Beauty and aesthetics
    "The {beauty} sunset painted the sky.",
    "It was a {beauty} ceremony attended by hundreds.",
    "The {beauty} landscape attracted many visitors.",

    # Difficulty
    "The {difficulty_hard} challenge tested their skills.",
    "It was an {difficulty_easy} solution to implement.",
    "They faced {difficulty_hard} obstacles along the way.",

    # Importance
    "This is an {importance} milestone for the organization.",
    "The {importance} findings will be published soon.",
    "They discussed {importance} policy changes.",

    # Temperature
    "The {temp_hot} summer day drove people indoors.",
    "The {temp_cold} winter lasted for months.",

    # Quantity
    "There were {quantity_many} applicants for the position.",
    "Only a {quantity_few} candidates were selected.",
    "{quantity_many} people attended the conference.",

    # Complex sentences with multiple synonyms
    "The {intelligence} researcher {verb_show} {quality_good} results from the {size_big} study.",
    "After a {difficulty_hard} journey, they felt {emotion_happy} to arrive at the {beauty} destination.",
    "The {size_small} team {verb_make} {quality_good} progress despite {quantity_few} resources.",
    "Her {intelligence} approach {verb_help} solve the {difficulty_hard} problem {speed_fast}.",
    "The {size_big} corporation {verb_give} {importance} support to {quantity_many} communities.",
]

# Synonym groups for templates
synonym_groups = {
    'size_big': ['enormous', 'huge', 'massive', 'immense', 'colossal', 'gigantic', 'vast', 'large', 'substantial'],
    'size_small': ['tiny', 'minute', 'minuscule', 'petite', 'compact', 'little', 'miniature'],
    'emotion_happy': ['elated', 'joyful', 'cheerful', 'delighted', 'pleased', 'glad', 'jubilant', 'content'],
    'emotion_sad': ['sorrowful', 'melancholy', 'dejected', 'gloomy', 'downcast', 'depressed', 'unhappy'],
    'emotion_angry': ['furious', 'irate', 'enraged', 'livid', 'wrathful', 'incensed', 'mad'],
    'intelligence': ['intelligent', 'clever', 'bright', 'brilliant', 'wise', 'astute', 'sharp', 'smart'],
    'speed_fast': ['rapid', 'swift', 'quick', 'speedy', 'hasty', 'brisk', 'fast'],
    'speed_slow': ['sluggish', 'leisurely', 'gradual', 'unhurried', 'slow'],
    'verb_say': ['stated', 'declared', 'mentioned', 'remarked', 'expressed', 'articulated', 'uttered'],
    'verb_walk': ['strolled', 'sauntered', 'ambled', 'wandered', 'strode', 'walked'],
    'verb_run': ['sprinted', 'dashed', 'raced', 'bolted', 'rushed', 'ran'],
    'verb_make': ['created', 'built', 'constructed', 'fabricated', 'produced', 'made'],
    'verb_help': ['assisted', 'aided', 'supported', 'facilitated', 'helped'],
    'verb_show': ['displayed', 'exhibited', 'demonstrated', 'presented', 'revealed', 'showed'],
    'verb_give': ['provided', 'supplied', 'offered', 'granted', 'bestowed', 'donated', 'gave'],
    'quality_good': ['excellent', 'great', 'superb', 'wonderful', 'outstanding', 'fine', 'good'],
    'quality_bad': ['poor', 'terrible', 'awful', 'dreadful', 'inferior', 'bad'],
    'beauty': ['gorgeous', 'stunning', 'lovely', 'attractive', 'elegant', 'pretty', 'beautiful'],
    'difficulty_hard': ['difficult', 'challenging', 'tough', 'arduous', 'demanding', 'hard'],
    'difficulty_easy': ['simple', 'straightforward', 'effortless', 'uncomplicated', 'easy'],
    'importance': ['significant', 'crucial', 'vital', 'essential', 'critical', 'important', 'key'],
    'temp_hot': ['warm', 'heated', 'scorching', 'burning', 'hot'],
    'temp_cold': ['chilly', 'cool', 'freezing', 'frigid', 'icy', 'cold'],
    'quantity_many': ['numerous', 'multiple', 'several', 'various', 'many'],
    'quantity_few': ['scarce', 'rare', 'limited', 'few'],
}

def generate_sentence(template):
    """Generate a sentence from a template by filling in synonyms."""
    sentence = template
    # Find all placeholders in the template
    for key in synonym_groups:
        if '{' + key + '}' in sentence:
            synonym = random.choice(synonym_groups[key])
            sentence = sentence.replace('{' + key + '}', synonym, 1)
    return sentence

# Generate training data
random.seed(42)  # For reproducibility
sentences = []

# Generate 2500 sentences
for _ in range(2500):
    template = random.choice(sentence_templates)
    sentence = generate_sentence(template)
    sentences.append(sentence)

# Write to file
with open('../data/training_data_original.txt', 'w') as f:
    for sentence in sentences:
        f.write(sentence + '\n')

print(f"Generated {len(sentences)} training sentences")
print(f"Saved to: ../data/training_data_original.txt")
