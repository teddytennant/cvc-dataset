#!/usr/bin/env python3
"""
Expand synonym mappings to create comprehensive coverage
"""

import json

# Create expanded mappings
expanded_mappings = {
    "metadata": {
        "version": "2.0",
        "description": "Comprehensive synonym-to-canonical mappings for CVC dataset",
        "creation_date": "2025-11-30",
        "total_mappings": 550,
        "sources": ["WordNet", "Manual Curation", "Frequency Analysis"]
    },
    "mappings": {
        # SIZE ADJECTIVES
        "size_big": {
            "canonical": "big",
            "synonyms": ["large", "huge", "enormous", "gigantic", "massive", "immense", "colossal", "vast", "substantial", "grand", "great", "sizable", "considerable", "extensive", "voluminous"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "size_small": {
            "canonical": "small",
            "synonyms": ["little", "tiny", "minute", "minuscule", "petite", "compact", "miniature", "diminutive", "microscopic", "slight", "puny", "undersized"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "size_tall": {
            "canonical": "tall",
            "synonyms": ["high", "lofty", "towering", "elevated", "soaring"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "size_short": {
            "canonical": "short",
            "synonyms": ["low", "squat", "stubby", "compact"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "size_wide": {
            "canonical": "wide",
            "synonyms": ["broad", "expansive", "extensive", "spacious", "ample"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "size_narrow": {
            "canonical": "narrow",
            "synonyms": ["thin", "slim", "slender", "tight", "confined"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "size_thick": {
            "canonical": "thick",
            "synonyms": ["dense", "heavy", "substantial", "chunky"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # SPEED ADJECTIVES
        "speed_fast": {
            "canonical": "fast",
            "synonyms": ["quick", "rapid", "swift", "speedy", "hasty", "brisk", "fleet", "expeditious", "prompt"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "speed_slow": {
            "canonical": "slow",
            "synonyms": ["sluggish", "leisurely", "gradual", "unhurried", "plodding", "lagging", "dawdling"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # INTELLIGENCE ADJECTIVES
        "intelligence_smart": {
            "canonical": "smart",
            "synonyms": ["intelligent", "clever", "bright", "brilliant", "wise", "astute", "sharp", "shrewd", "keen", "perceptive", "insightful", "brainy", "gifted", "talented"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "intelligence_dumb": {
            "canonical": "dumb",
            "synonyms": ["stupid", "foolish", "ignorant", "unintelligent", "dense", "dim", "dull"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # BEAUTY ADJECTIVES
        "beauty_beautiful": {
            "canonical": "beautiful",
            "synonyms": ["pretty", "gorgeous", "stunning", "lovely", "attractive", "handsome", "elegant", "exquisite", "graceful", "charming", "appealing", "alluring", "radiant"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "beauty_ugly": {
            "canonical": "ugly",
            "synonyms": ["unattractive", "hideous", "unsightly", "grotesque", "homely"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # EMOTION ADJECTIVES - HAPPY
        "emotion_happy": {
            "canonical": "happy",
            "synonyms": ["joyful", "cheerful", "delighted", "pleased", "content", "glad", "elated", "jubilant", "ecstatic", "blissful", "merry", "jovial", "upbeat"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "emotion_sad": {
            "canonical": "sad",
            "synonyms": ["unhappy", "sorrowful", "melancholy", "dejected", "gloomy", "downcast", "depressed", "miserable", "mournful", "woeful", "dismal"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "emotion_angry": {
            "canonical": "angry",
            "synonyms": ["furious", "irate", "enraged", "livid", "mad", "wrathful", "incensed", "outraged", "infuriated", "indignant"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "emotion_scared": {
            "canonical": "scared",
            "synonyms": ["afraid", "frightened", "fearful", "terrified", "alarmed", "panicked", "anxious", "nervous", "worried"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "emotion_excited": {
            "canonical": "excited",
            "synonyms": ["thrilled", "enthusiastic", "eager", "animated", "energized"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "emotion_calm": {
            "canonical": "calm",
            "synonyms": ["peaceful", "serene", "tranquil", "placid", "relaxed", "composed"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "emotion_surprised": {
            "canonical": "surprised",
            "synonyms": ["astonished", "amazed", "shocked", "startled", "stunned", "astounded"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # QUALITY ADJECTIVES
        "quality_good": {
            "canonical": "good",
            "synonyms": ["excellent", "great", "fine", "superb", "wonderful", "outstanding", "superior", "splendid", "marvelous", "fantastic", "terrific", "fabulous", "stellar"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "quality_bad": {
            "canonical": "bad",
            "synonyms": ["poor", "terrible", "awful", "dreadful", "inferior", "substandard", "mediocre", "lousy", "dismal", "abysmal"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # DIFFICULTY ADJECTIVES
        "difficulty_easy": {
            "canonical": "easy",
            "synonyms": ["simple", "straightforward", "effortless", "uncomplicated", "elementary", "basic", "painless"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "difficulty_hard": {
            "canonical": "hard",
            "synonyms": ["difficult", "challenging", "tough", "arduous", "demanding", "strenuous", "laborious", "complex", "complicated"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # IMPORTANCE ADJECTIVES
        "importance_important": {
            "canonical": "important",
            "synonyms": ["significant", "crucial", "vital", "essential", "critical", "key", "major", "fundamental", "primary", "principal", "paramount"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "importance_unimportant": {
            "canonical": "unimportant",
            "synonyms": ["insignificant", "trivial", "minor", "petty", "negligible"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # QUANTITY ADJECTIVES
        "quantity_many": {
            "canonical": "many",
            "synonyms": ["numerous", "multiple", "several", "various", "countless", "abundant", "plentiful"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "quantity_few": {
            "canonical": "few",
            "synonyms": ["scarce", "rare", "limited", "sparse", "scant"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # TEMPERATURE ADJECTIVES
        "temp_hot": {
            "canonical": "hot",
            "synonyms": ["warm", "heated", "scorching", "burning", "sweltering", "torrid", "blazing", "searing", "boiling"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "temp_cold": {
            "canonical": "cold",
            "synonyms": ["chilly", "cool", "freezing", "frigid", "icy", "frosty", "arctic", "wintry"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # CERTAINTY ADJECTIVES
        "certainty_sure": {
            "canonical": "sure",
            "synonyms": ["certain", "confident", "positive", "convinced", "assured", "definite"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "certainty_unsure": {
            "canonical": "unsure",
            "synonyms": ["uncertain", "doubtful", "hesitant", "dubious", "skeptical"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # AGE ADJECTIVES
        "age_old": {
            "canonical": "old",
            "synonyms": ["ancient", "aged", "elderly", "antique", "archaic", "veteran"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "age_new": {
            "canonical": "new",
            "synonyms": ["fresh", "recent", "modern", "contemporary", "novel", "latest"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "age_young": {
            "canonical": "young",
            "synonyms": ["youthful", "juvenile", "adolescent", "immature"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # STRENGTH ADJECTIVES
        "strength_strong": {
            "canonical": "strong",
            "synonyms": ["powerful", "robust", "sturdy", "mighty", "potent", "forceful"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "strength_weak": {
            "canonical": "weak",
            "synonyms": ["feeble", "frail", "fragile", "delicate", "flimsy"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # CLEANLINESS ADJECTIVES
        "clean_clean": {
            "canonical": "clean",
            "synonyms": ["spotless", "pristine", "immaculate", "sanitary", "hygienic"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "clean_dirty": {
            "canonical": "dirty",
            "synonyms": ["filthy", "grimy", "soiled", "unclean", "muddy"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # LIGHT ADJECTIVES
        "light_bright": {
            "canonical": "bright",
            "synonyms": ["luminous", "brilliant", "radiant", "vivid", "glowing"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "light_dark": {
            "canonical": "dark",
            "synonyms": ["dim", "shadowy", "gloomy", "murky", "dusky"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # WETNESS ADJECTIVES
        "wet_wet": {
            "canonical": "wet",
            "synonyms": ["damp", "moist", "soaked", "drenched", "saturated"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "wet_dry": {
            "canonical": "dry",
            "synonyms": ["arid", "parched", "dehydrated", "desiccated"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # NOISE ADJECTIVES
        "noise_loud": {
            "canonical": "loud",
            "synonyms": ["noisy", "deafening", "thunderous", "booming", "roaring"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noise_quiet": {
            "canonical": "quiet",
            "synonyms": ["silent", "hushed", "muted", "soft", "peaceful"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # COMMUNICATION VERBS
        "verb_say": {
            "canonical": "say",
            "synonyms": ["state", "declare", "mention", "remark", "express", "articulate", "utter", "announce", "proclaim", "assert"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_ask": {
            "canonical": "ask",
            "synonyms": ["inquire", "question", "query", "request"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_tell": {
            "canonical": "tell",
            "synonyms": ["inform", "notify", "advise", "relate", "recount"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_talk": {
            "canonical": "talk",
            "synonyms": ["speak", "converse", "chat", "discuss", "communicate"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_shout": {
            "canonical": "shout",
            "synonyms": ["yell", "scream", "holler", "bellow", "roar"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_whisper": {
            "canonical": "whisper",
            "synonyms": ["murmur", "mutter", "mumble"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # MOTION VERBS
        "verb_walk": {
            "canonical": "walk",
            "synonyms": ["stroll", "saunter", "amble", "wander", "stride", "trek", "hike", "march"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_run": {
            "canonical": "run",
            "synonyms": ["sprint", "dash", "race", "bolt", "rush", "hurry"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_jump": {
            "canonical": "jump",
            "synonyms": ["leap", "bound", "hop", "spring", "vault"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_sit": {
            "canonical": "sit",
            "synonyms": ["rest", "settle", "perch"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_stand": {
            "canonical": "stand",
            "synonyms": ["rise", "arise"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_fall": {
            "canonical": "fall",
            "synonyms": ["drop", "tumble", "plunge", "descend", "collapse"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # PERCEPTION VERBS
        "verb_look": {
            "canonical": "look",
            "synonyms": ["gaze", "stare", "glance", "peer", "observe", "view", "watch", "examine", "inspect"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_see": {
            "canonical": "see",
            "synonyms": ["notice", "spot", "perceive", "detect", "discern"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_hear": {
            "canonical": "hear",
            "synonyms": ["listen", "overhear"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_smell": {
            "canonical": "smell",
            "synonyms": ["sniff", "scent"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_taste": {
            "canonical": "taste",
            "synonyms": ["sample", "savor"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_touch": {
            "canonical": "touch",
            "synonyms": ["feel", "handle", "grasp"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # COGNITION VERBS
        "verb_think": {
            "canonical": "think",
            "synonyms": ["ponder", "contemplate", "reflect", "consider", "deliberate", "meditate", "ruminate", "muse"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_know": {
            "canonical": "know",
            "synonyms": ["understand", "comprehend", "grasp", "realize"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_remember": {
            "canonical": "remember",
            "synonyms": ["recall", "recollect"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_forget": {
            "canonical": "forget",
            "synonyms": ["overlook", "disregard"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_learn": {
            "canonical": "learn",
            "synonyms": ["study", "master", "acquire"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_teach": {
            "canonical": "teach",
            "synonyms": ["instruct", "educate", "train", "tutor"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # ACTION VERBS
        "verb_make": {
            "canonical": "make",
            "synonyms": ["create", "build", "construct", "fabricate", "manufacture", "produce", "craft", "form"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_break": {
            "canonical": "break",
            "synonyms": ["shatter", "smash", "fracture", "crack", "destroy"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_fix": {
            "canonical": "fix",
            "synonyms": ["repair", "mend", "restore"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_help": {
            "canonical": "help",
            "synonyms": ["assist", "aid", "support", "facilitate"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_hurt": {
            "canonical": "hurt",
            "synonyms": ["harm", "injure", "wound", "damage"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_use": {
            "canonical": "use",
            "synonyms": ["utilize", "employ", "apply", "exercise"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_show": {
            "canonical": "show",
            "synonyms": ["display", "exhibit", "demonstrate", "present", "reveal"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_hide": {
            "canonical": "hide",
            "synonyms": ["conceal", "cover", "obscure"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_find": {
            "canonical": "find",
            "synonyms": ["discover", "locate", "uncover", "detect"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_lose": {
            "canonical": "lose",
            "synonyms": ["misplace", "forfeit"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_get": {
            "canonical": "get",
            "synonyms": ["obtain", "acquire", "procure", "secure", "gain", "receive"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_give": {
            "canonical": "give",
            "synonyms": ["provide", "supply", "offer", "grant", "bestow", "donate"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_take": {
            "canonical": "take",
            "synonyms": ["grab", "seize", "grasp", "capture"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_send": {
            "canonical": "send",
            "synonyms": ["transmit", "dispatch", "deliver", "forward"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_bring": {
            "canonical": "bring",
            "synonyms": ["carry", "transport", "convey"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_buy": {
            "canonical": "buy",
            "synonyms": ["purchase", "acquire"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_sell": {
            "canonical": "sell",
            "synonyms": ["vend", "market"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_start": {
            "canonical": "start",
            "synonyms": ["begin", "commence", "initiate", "launch"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_stop": {
            "canonical": "stop",
            "synonyms": ["cease", "halt", "terminate", "end"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_continue": {
            "canonical": "continue",
            "synonyms": ["proceed", "persist", "resume"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_change": {
            "canonical": "change",
            "synonyms": ["alter", "modify", "transform", "convert"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_keep": {
            "canonical": "keep",
            "synonyms": ["retain", "maintain", "preserve"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "verb_try": {
            "canonical": "try",
            "synonyms": ["attempt", "endeavor", "strive"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # COMMON NOUNS
        "noun_person": {
            "canonical": "person",
            "synonyms": ["individual", "human", "being"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_people": {
            "canonical": "people",
            "synonyms": ["individuals", "persons", "folks"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_child": {
            "canonical": "child",
            "synonyms": ["kid", "youngster", "youth"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_house": {
            "canonical": "house",
            "synonyms": ["home", "residence", "dwelling", "abode", "domicile"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_car": {
            "canonical": "car",
            "synonyms": ["automobile", "vehicle", "auto"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_job": {
            "canonical": "job",
            "synonyms": ["occupation", "profession", "career", "employment", "vocation", "position"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_money": {
            "canonical": "money",
            "synonyms": ["cash", "currency", "funds", "capital"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_food": {
            "canonical": "food",
            "synonyms": ["meal", "nourishment", "sustenance"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_water": {
            "canonical": "water",
            "synonyms": ["liquid", "fluid"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_place": {
            "canonical": "place",
            "synonyms": ["location", "spot", "site", "position"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_thing": {
            "canonical": "thing",
            "synonyms": ["object", "item", "article"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_time": {
            "canonical": "time",
            "synonyms": ["period", "duration", "moment"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_way": {
            "canonical": "way",
            "synonyms": ["method", "manner", "approach"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_idea": {
            "canonical": "idea",
            "synonyms": ["concept", "thought", "notion"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_problem": {
            "canonical": "problem",
            "synonyms": ["issue", "difficulty", "challenge"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "noun_answer": {
            "canonical": "answer",
            "synonyms": ["solution", "response", "reply"],
            "frequency_rank": 1,
            "domain": "general"
        },

        # ADVERBS
        "adverb_very": {
            "canonical": "very",
            "synonyms": ["extremely", "exceedingly", "exceptionally", "tremendously", "remarkably", "highly"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "adverb_quickly": {
            "canonical": "quickly",
            "synonyms": ["rapidly", "swiftly", "speedily", "hastily", "promptly"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "adverb_slowly": {
            "canonical": "slowly",
            "synonyms": ["gradually", "leisurely"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "adverb_often": {
            "canonical": "often",
            "synonyms": ["frequently", "commonly", "regularly"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "adverb_rarely": {
            "canonical": "rarely",
            "synonyms": ["seldom", "infrequently"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "adverb_always": {
            "canonical": "always",
            "synonyms": ["constantly", "continually", "perpetually"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "adverb_never": {
            "canonical": "never",
            "synonyms": ["not ever"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "adverb_well": {
            "canonical": "well",
            "synonyms": ["properly", "correctly", "effectively"],
            "frequency_rank": 1,
            "domain": "general"
        },
        "adverb_badly": {
            "canonical": "badly",
            "synonyms": ["poorly", "inadequately"],
            "frequency_rank": 1,
            "domain": "general"
        }
    }
}

# Build reverse lookup
reverse_lookup = {}
for category, info in expanded_mappings["mappings"].items():
    canonical = info["canonical"]
    for synonym in info["synonyms"]:
        reverse_lookup[synonym] = canonical

expanded_mappings["reverse_lookup"] = reverse_lookup

# Count actual mappings
total_synonyms = sum(len(info["synonyms"]) for info in expanded_mappings["mappings"].values())
expanded_mappings["metadata"]["total_synonyms"] = total_synonyms
expanded_mappings["metadata"]["total_mappings"] = len(expanded_mappings["mappings"])

# Save
with open('../mappings/synonym_to_canonical.json', 'w') as f:
    json.dump(expanded_mappings, f, indent=2)

print(f"Created comprehensive mappings:")
print(f"  Categories: {len(expanded_mappings['mappings'])}")
print(f"  Total synonym mappings: {total_synonyms}")
print(f"  Saved to: ../mappings/synonym_to_canonical.json")
