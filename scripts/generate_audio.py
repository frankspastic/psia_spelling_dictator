#!/usr/bin/env python3
"""
Generate high-quality audio files for spelling words using Google Cloud Text-to-Speech.

This script generates MP3 files for all spelling words in both grade levels.
It uses Google Cloud TTS Standard voices which are free within the 4M character/month limit.

Prerequisites:
1. Install dependencies: uv pip install -r requirements.txt
2. Set up Google Cloud credentials:
   - Create a project at https://console.cloud.google.com
   - Enable Text-to-Speech API
   - Create a service account and download JSON key
   - Set environment variable: export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"

Usage:
    python generate_audio.py [--voice-type male|female] [--grade-level gr23|gr45|both]
"""

import os
import sys
import argparse
import re
from pathlib import Path
from google.cloud import texttospeech

# Word lists (copied from words.js)
SPELLING_WORDS_GR23 = [
    "abduction", "abnormal", "accountant", "accurate", "actress", "adjust", "admire", "adverb", "agreement", "airport",
    "allowance", "almost", "altar", "animated", "ankle", "answer", "antonym", "anxious", "apparel", "applaud",
    "ashamed", "assemble", "atom", "attach", "attorney", "awaken", "awkward", "baffle", "baggage", "balcony",
    "banquet", "baritone", "barrette", "basement", "beginner", "behave", "beholder", "belittle", "beneath", "between",
    "beyond", "bicycle", "biscuit", "blackberry", "blazer", "bleach", "blunder", "boast", "bobsled", "borderline",
    "bouquet", "bowlegged", "bowling", "brassy", "breakfast", "brilliant", "buffalo", "burglary", "bursting", "buttercup",
    "cameo", "cancer", "candle", "career", "catnip", "caught", "cavity", "certificate", "channel", "chapter",
    "chilly", "choosy", "citizen", "cling", "clutch", "cobbler", "college", "collie", "comedy", "commit",
    "complete", "composure", "comrade", "connect", "cornflakes", "correction", "countable", "coupon", "creature", "crescent",
    "crimson", "cringe", "cursive", "daily", "dainty", "deacon", "decay", "decision", "decode", "decrease",
    "deflate", "depend", "deposit", "deputy", "destiny", "detach", "diagram", "difficult", "digest", "discover",
    "disordered", "disown", "disturb", "domino", "donor", "downward", "drafty", "dressy", "drone", "drumstick",
    "dry-clean", "dusty", "eager", "earlobe", "earring", "earthen", "easily", "eastern", "editor", "eggbeater",
    "eighteen", "elastic", "elbow", "elegant", "elfin", "emblem", "emperor", "enchantment", "endanger", "enemy",
    "engineer", "engrave", "entitle", "equality", "erase", "errand", "eruption", "evacuate", "evasion", "exam",
    "exhale", "explain", "explode", "expression", "extreme", "fabric", "factory", "famine", "farsighted", "fearful",
    "feather", "February", "fetch", "fiction", "fierce", "fingerprint", "finish", "floral", "fluoride", "foolish",
    "forenoon", "forever", "forward", "foursome", "frankly", "freeze", "friend", "frighten", "frigid", "frosting",
    "fruitless", "furnace", "gallery", "gaseous", "gateway", "gather", "gavel", "gecko", "generate", "gentleman",
    "geography", "germinate", "ghastly", "glassware", "glider", "glisten", "globally", "goofy", "governor", "gracious",
    "grateful", "grease", "gripe", "grocery", "grouch", "growl", "grudge", "guesswork", "gulp", "gumdrop",
    "gutsy", "guzzle", "habitat", "halve", "hammock", "handicap", "happily", "harmless", "harpoon", "haunt",
    "hayloft", "healthy", "helpless", "heptagon", "herb", "hidden", "hillside", "hippo", "hire", "historian",
    "hockey", "holiday", "homework", "honest", "horrible", "hostage", "hostess", "humanly", "humble", "humbug",
    "husband", "icing", "idolize", "illusion", "illustrate", "imagine", "imperial", "important", "incomplete", "incorrect",
    "indent", "infancy", "infect", "initial", "inkwell", "innate", "innermost", "innkeeper", "inorganic", "insecure",
    "instep", "intense", "intent", "interior", "invade", "involve", "irrigate", "isolate", "jackknife", "jangle",
    "jasper", "jaywalk", "jell", "jinx", "jowl", "jukebox", "jumbo", "junction", "keeping", "kettle",
    "kidney", "kindergarten", "kindred", "knave", "krill", "label", "ladies", "lamppost", "landfill", "language",
    "laser", "lava", "lawsuit", "layer", "leather", "ledger", "legend", "library", "lifesaving", "likewise",
    "lilac", "linen", "livelihood", "lobster", "locate", "locomotive", "lonely", "loosen", "lopsided", "lowercase",
    "luckily", "lunge", "lurk", "luxury", "macaroon", "magician", "mainland", "maintain", "mammal", "manage",
    "manicure", "material", "mattress", "mayor", "melodic", "mental", "merriment", "message", "mightily", "miracle",
    "miserable", "mixture", "moisture", "moment", "motorist", "multiple", "musician", "nameless", "narrow", "naughty",
    "nearly", "nectarine", "needfully", "neighborly", "neither", "nerve", "network", "newsy", "nickel", "ninety",
    "ninny", "nitpick", "noble", "nodding", "noisy", "nondairy", "nonfat", "noodle", "nostril", "notebook",
    "notice", "notify", "novelist", "November", "nugget", "number", "numerous", "nursery", "nutrition", "oath",
    "oatmeal", "obvious", "occasion", "occur", "ocean", "oddball", "offering", "officer", "olive", "omission",
    "omit", "open-and-shut", "opener", "operable", "oppose", "optional", "ordain", "ordered", "organist", "orphan",
    "outcome", "outrank", "overtime", "overweight", "oyster", "package", "pamper", "paperback", "parade", "parka",
    "partial", "partner", "passageway", "pattern", "pavement", "peculiar", "penalty", "performance", "period", "persuade",
    "petticoat", "phony", "pioneer", "plastic", "pleasure", "plywood", "poison", "popular", "possible", "prefix",
    "pretend", "prewash", "prickly", "provoke", "pumpkin", "purple", "quake", "qualified", "quarrel", "quarterly",
    "queenly", "question", "quicken", "quiet", "quip", "quitter", "quote", "rabies", "ragged", "raincoat",
    "random", "ranger", "raspy", "rattlesnake", "readily", "reason", "rebel", "recover", "rectangle", "reflex",
    "rehearse", "relative", "relief", "remember", "republic", "request", "retire", "review", "revolve", "rhythm",
    "rightful", "risky", "roomy", "rosy", "routine", "rubbish", "running", "rural", "salsa", "salvage",
    "sanitary", "sardine", "satisfy", "scissors", "scoundrel", "scrawny", "seasonal", "sensible", "separate", "shortage",
    "shoulder", "signature", "skillful", "smuggle", "solution", "soothe", "spaghetti", "splinter", "squirm", "squirrel",
    "standard", "steeple", "straight", "stylist", "subscribe", "success", "summon", "surface", "survey", "sympathy",
    "tactful", "tadpole", "tailored", "talkative", "teacher", "teaspoon", "telethon", "tendency", "terrible", "texture",
    "therapy", "thief", "thistle", "thousand", "tidewater", "timeless", "tinker", "tiresome", "toddler", "tongue",
    "tradition", "trait", "transplant", "tremble", "tribute", "trickery", "tropical", "trousers", "trumpet", "tweezers",
    "twilight", "twitch", "typical", "ultrasound", "unadorned", "unbuckle", "understand", "uneaten", "unhinge", "uniform",
    "unity", "unlace", "unload", "unplug", "unreported", "unshaven", "unsinkable", "unwise", "unzip", "uproar",
    "upwind", "useful", "utmost", "vacancy", "vaccine", "valid", "vanish", "varied", "varnish", "vegetable",
    "velvety", "venison", "verbal", "verge", "verify", "victim", "violin", "viper", "vision", "vivid",
    "voice", "volcano", "volleyball", "wafer", "waffle", "wail", "wanting", "wayward", "weakling", "weary",
    "weird", "whimper", "wedding", "wilderness", "witness", "worried", "wrapper", "xebec", "Yankee", "yardstick",
    "yearbook", "yellowish", "yogurt", "youngish", "yummy", "zeal", "zero", "zigzag", "zodiac", "zoom"
]

SPELLING_WORDS_GR45 = [
    "abdomen", "abrasive", "abridged", "abrupt", "absolutely", "accentuate", "acceptable", "accomplish", "acquaint", "activate",
    "actually", "addendum", "admittance", "advantage", "advertise", "aerobics", "affirmative", "aggressive", "agriculture", "airborne",
    "alarmist", "allegation", "allocate", "alternative", "altogether", "ambulance", "amethyst", "amputate", "anecdote", "angrily",
    "anonymous", "antagonist", "apologetic", "appetizer", "appliance", "apprehend", "apprentice", "approach", "armored", "arrogance",
    "assess", "association", "attendant", "audit", "authentic", "averaging", "bachelor", "background", "backstroke", "bandage",
    "bandanna", "bankrupt", "baptism", "barbershop", "barometer", "barracks", "baseline", "beautician", "becoming", "bedrock",
    "begrime", "begrudge", "behavior", "benignant", "berserk", "biceps", "binocular", "biography", "biological", "bittersweet",
    "blameless", "blockbuster", "bloodmobile", "blueprint", "bombard", "bonanza", "botanical", "bottleneck", "bought", "boulder",
    "brainstorming", "breakable", "breathe", "broadband", "brutish", "buffoon", "bulging", "bullheaded", "burdensome", "burial",
    "butterscotch", "calcium", "calligraphy", "cancerous", "captivate", "carelessness", "carnival", "carousel", "cartilage", "ceaseless",
    "celebrity", "centerpiece", "chairperson", "chaos", "characteristic", "cheerleader", "circular", "civilize", "classical", "cleanse",
    "clientele", "coleslaw", "collapse", "collarbone", "collide", "commentary", "committee", "commonplace", "commune", "companion",
    "competitor", "component", "compost", "comprise", "conclusion", "condense", "consonant", "constellation", "continental drift", "convenient",
    "convey", "coordination", "countries", "courteous", "crevice", "crisply", "cultivate", "custodian", "cylinder", "dachshund",
    "daredevil", "deadline", "debris", "debug", "deceive", "deception", "decompose", "deepwater", "defensive", "deliberate",
    "delicatessen", "delightful", "denominator", "denture", "despise", "despondent", "deterrent", "devour", "diagonal", "difficulty",
    "digestion", "dilemma", "dimension", "disaster", "discriminate", "dishearten", "dislodge", "dispenser", "distressful", "division",
    "do-it-yourself", "domesticate", "dormancy", "dowdy", "downgrade", "dreadful", "dreary", "drudgery", "duplex", "duplicate",
    "durable", "earthenware", "ecology", "ecstatic", "effortless", "egocentric", "election", "electronics", "elementary", "embargo",
    "embarrass", "embellish", "emergency", "emission", "employment", "emptying", "enamel", "encourage", "encumber", "endearment",
    "energize", "engagement", "enliven", "ensue", "entertain", "envisage", "equinox", "eradication", "escapade", "eulogy",
    "evaporate", "exaggerate", "examination", "exception", "excursion", "exert", "exhibit", "expedition", "experiment", "expressway",
    "exquisite", "exuberance", "eyewitness", "facility", "failing", "familiar", "fantasy", "fast-forward", "fatality", "fatherly",
    "fathom", "favoritism", "fellowship", "felon", "fertilizer", "fester", "fetching", "fictitious", "fidgety", "filibuster",
    "filthy", "financier", "fireproof", "flagship", "flattery", "flimsy", "flourish", "fluent", "forecast", "foremost",
    "forgetting", "formality", "formulate", "forthcoming", "fortify", "frailty", "franchise", "fraud", "freakish", "freshened",
    "fulfill", "function", "gadabout", "gaggle", "gallantry", "gamma", "gardenia", "generally", "generator", "genetic engineering",
    "geographer", "gesturing", "gewgaw", "ghetto", "giddily", "gladiator", "glittery", "global", "glossary", "glowworm",
    "glucose", "goalie", "go-between", "goober", "gooseflesh", "gopher", "goulash", "gourmet", "grammar", "grandeur",
    "granular", "gratuitous", "gravitate", "greenhouse effect", "gremlin", "grimness", "groundwork", "gruesome", "guffaw", "gusher",
    "gymnast", "halfhearted", "halibut", "hallmark", "handkerchief", "handling", "handwritten", "haphazard", "hardening", "harebrained",
    "harmonious", "harvest moon", "hastily", "hazing", "heartily", "heckle", "heiress", "helium", "henpeck", "hermitage",
    "heroism", "hesitating", "hibernate", "hiccup", "hijack", "homecoming", "hominy", "honestly", "honeysuckle", "hopefully",
    "hopscotch", "hospital", "hourglass", "hubbub", "huckleberry", "humanity", "humdrum", "hydroplane", "hygiene", "hyperlink",
    "hypnotism", "icebreaker", "icon", "identically", "identifiable", "ignition", "ignorant", "illiterate", "illogical", "imaginary",
    "immaculate", "immaterial", "immoral", "impacted", "impairment", "impersonal", "improvement", "impurity", "inaudible", "inaugurate",
    "inclusion", "increasingly", "industrial", "inexcusable", "inflation", "inflict", "injunction", "inoculate", "insecticide", "instrument",
    "intelligence", "interlude", "interrupt", "interspace", "intolerant", "intruding", "inventor", "invisible", "iodine", "ironic",
    "irritable", "italicize", "jackrabbit", "Japanese", "javelin", "jealously", "jet stream", "jewelry", "jittery", "jokingly",
    "journalist", "jovial", "joystick", "judgment", "juvenile", "Kabuki", "kangaroo", "karate", "kazoo", "kerchief",
    "kettledrum", "kickstand", "kilogram", "kilt", "kindle", "kinetic", "kneecap", "knee-deep", "knickknack", "knightly",
    "knoll", "knotted", "koala", "laceration", "lacquer", "ladylike", "lanolin", "larynx", "lateral", "laughter",
    "laurel", "lazyish", "leaden", "leadership", "leech", "legendary", "legislator", "letterhead", "levator", "libel",
    "liberal", "lifestyle", "ligament", "lightweight", "limitation", "linebacker", "linguist", "literacy", "loathsome", "locust",
    "lodging", "lonesomeness", "longitude", "lordly", "loudspeaker", "lounging", "low-grade", "lurch", "lusciousness", "luster",
    "macaw", "magenta", "magnetizable", "mahogany", "maladjusted", "malaria", "malformation", "mammoth", "manifold", "manipulate",
    "marginal", "marshmallow", "marsupial", "mathematics", "mawkish", "meander", "meaningless", "measurement", "mediate", "memoir",
    "memorable", "merciless", "mesmerize", "mettlesome", "microphone", "migraine", "millionaire", "minimize", "minuet", "misdemeanor",
    "misfortune", "missile", "missionary", "modular", "molecule", "momentary", "monstrous", "monument", "motive", "multicultural",
    "mutiny", "mutual", "mythical", "nailbrush", "narrative", "nationality", "natty", "nausea", "needlepoint", "negation",
    "Neptune", "nestling", "neutrality", "newlywed", "nicety", "nigh", "nightfall", "nineteen", "nitrite", "nocturnal",
    "nominee", "nonmetallic", "nonthreatening", "nontraditional", "normality", "Northerner", "notable", "notarize", "nourishment", "nova",
    "nowadays", "nucleus", "numerical", "nurseryman", "nurturing", "nutritional", "nuttiness", "obesity", "objection", "obligatory",
    "obscurity", "obsession", "occurrence", "octagon", "odorous", "oldish", "olfaction", "omelet", "omen", "once-over",
    "oneself", "opaque", "openmouthed", "opportunity", "opposition", "optician", "opus", "oratory", "orchestrate", "organism",
    "originality", "ornateness", "osmosis", "ossify", "outerwear", "outfitted", "outsider", "outspoken", "overcritical", "overstuffed",
    "overturn", "owlet", "ownership", "ozone", "painkiller", "palatable", "pancreas", "paraffin", "paragraph", "parentage",
    "parsonage", "patience", "patriotism", "paunchy", "pedestrian", "peninsula", "penmanship", "pension", "perceive", "perform",
    "perishable", "permanent", "persistent", "personalize", "pertain", "philosophy", "planetarium", "plaque", "pollution", "ponderous",
    "population", "portrayal", "postpone", "potatoes", "precipitation", "precisely", "predator", "prevailing", "previous", "printable",
    "progressive", "prominent", "property", "pulsate", "pyramid", "quaking", "qualify", "quarrelsome", "quarto", "quickening",
    "quintillion", "quipped", "quittance", "raccoon", "racecourse", "racket", "radiology", "rallying", "rancid", "ravenous",
    "rayon", "reactor", "reality", "recede", "receipt", "receptionist", "recondition", "reconsider", "referendum", "reflective",
    "refugee", "regardless", "relative humidity", "reliable", "reluctant", "repetitious", "rephrase", "replenish", "reputation", "reservoir",
    "residue", "resourceful", "response", "retrieval", "reunite", "revival", "revolution", "rhapsody", "riddance", "rigorous",
    "rinsing", "roommate", "roster", "roustabout", "rummy", "rumored", "saintly", "sanctify", "sanctuary", "satisfaction",
    "scenario", "scenic", "scientific", "scrunch", "secluded", "segregate", "selection", "seminary", "sensibility", "session",
    "shadowy", "shamefaced", "shredded", "similarity", "simplify", "situate", "skeletal", "slanderous", "sleepwalk", "sociology",
    "solace", "somersault", "southwesterly", "spectator", "speculation", "squeamish", "statistical", "stature", "stencil", "subdivision",
    "submerge", "submissive", "supervision", "suppress", "surgeon", "surrender", "suspense", "symphony", "tablespoonful", "tabloid",
    "tandem", "tangible", "tattoo", "taxpayer", "teammate", "technique", "telegram", "temperate", "tendon", "terminal",
    "testimonial", "theatergoer", "thenceforth", "therapist", "thickset", "threadbare", "thunderous", "thyroid", "tiller", "titanic",
    "toffee", "tolerant", "toolshed", "topaz", "torturous", "towhead", "toxic", "transcript", "transgress", "translucent",
    "tributary", "trillion", "tubular", "turmoil", "tutorial", "tuxedo", "typhoon", "ulster", "ultimate", "unaware",
    "unbalanced", "unbeatable", "uncluttered", "underage", "unearthly", "ungrateful", "unique", "unitarian", "united", "unrighteous",
    "unsportsmanlike", "untouchable", "upstream", "Uranus", "vagrancy", "vague", "vandalize", "variance", "varicolored", "vegan",
    "vegetation", "vein", "ventilate", "verbally", "versatile", "vertebra", "vertically", "vessel", "Virgo", "virtuous",
    "vitamin", "voiceless", "voluntarily", "voucher", "vulnerable", "waft", "wandering", "warbling", "warmhearted", "warrior",
    "washbasin", "watchful", "watercolor", "wedlock", "whence", "whichever", "whispery", "wingspread", "wistful", "withdrawn",
    "worthy", "wristband", "xerophyte", "yak", "yammering", "yard sale", "yielding", "yippee", "zinc", "zombie"
]


def sanitize_filename(word):
    """Convert word to safe filename (lowercase, replace spaces with underscores)."""
    # Convert to lowercase
    filename = word.lower()
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Keep only alphanumeric, underscores, and hyphens
    filename = re.sub(r'[^a-z0-9_-]', '', filename)
    return filename


def generate_audio_for_word(client, word, voice_name, output_path):
    """Generate audio for a single word using Google Cloud TTS."""
    # Set up the synthesis input
    synthesis_input = texttospeech.SynthesisInput(text=word)

    # Set up the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name
    )

    # Set up the audio config
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.9  # Slightly slower for clarity
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Write the response to an MP3 file
    with open(output_path, 'wb') as out:
        out.write(response.audio_content)


def main():
    parser = argparse.ArgumentParser(description='Generate audio files for spelling words')
    parser.add_argument('--voice-type', choices=['male', 'female'], default='female',
                        help='Voice gender (default: female)')
    parser.add_argument('--grade-level', choices=['gr23', 'gr45', 'both'], default='both',
                        help='Which grade level to generate (default: both)')
    parser.add_argument('--use-wavenet', action='store_true',
                        help='Use WaveNet voices (higher quality, costs ~$0.20 total)')

    args = parser.parse_args()

    # Determine voice name
    if args.use_wavenet:
        voice_name = 'en-US-Wavenet-C' if args.voice_type == 'female' else 'en-US-Wavenet-D'
        print(f"Using WaveNet voice: {voice_name} (premium quality)")
    else:
        voice_name = 'en-US-Standard-C' if args.voice_type == 'female' else 'en-US-Standard-D'
        print(f"Using Standard voice: {voice_name} (free tier)")

    # Initialize the Text-to-Speech client
    try:
        client = texttospeech.TextToSpeechClient()
    except Exception as e:
        print("\n❌ Error: Could not initialize Google Cloud TTS client.")
        print("Make sure you have:")
        print("1. Installed dependencies: uv pip install -r requirements.txt")
        print("2. Set up Google Cloud credentials:")
        print("   - Create project at https://console.cloud.google.com")
        print("   - Enable Text-to-Speech API")
        print("   - Create service account and download JSON key")
        print("   - Set: export GOOGLE_APPLICATION_CREDENTIALS='path/to/key.json'")
        print(f"\nError details: {e}")
        sys.exit(1)

    # Create output directories
    base_dir = Path(__file__).parent / 'audio'
    base_dir.mkdir(exist_ok=True)

    # Determine which grade levels to process
    grade_levels = []
    if args.grade_level in ['gr23', 'both']:
        grade_levels.append(('gr23', SPELLING_WORDS_GR23))
    if args.grade_level in ['gr45', 'both']:
        grade_levels.append(('gr45', SPELLING_WORDS_GR45))

    # Process each grade level
    total_words = sum(len(words) for _, words in grade_levels)
    processed = 0

    print(f"\nGenerating audio for {total_words} words...")
    print("=" * 60)

    for grade, words in grade_levels:
        grade_dir = base_dir / grade
        grade_dir.mkdir(exist_ok=True)

        print(f"\n📚 Processing {grade.upper()} ({len(words)} words)")
        print("-" * 60)

        for i, word in enumerate(words, 1):
            filename = sanitize_filename(word) + '.mp3'
            output_path = grade_dir / filename

            try:
                generate_audio_for_word(client, word, voice_name, output_path)
                processed += 1

                # Progress indicator
                if i % 10 == 0 or i == len(words):
                    progress = (processed / total_words) * 100
                    print(f"  [{processed}/{total_words}] {progress:.1f}% - {word} → {filename}")

            except Exception as e:
                print(f"  ❌ Error generating '{word}': {e}")

    print("\n" + "=" * 60)
    print(f"✅ Complete! Generated {processed}/{total_words} audio files")
    print(f"\nFiles saved in:")
    for grade, _ in grade_levels:
        grade_dir = base_dir / grade
        print(f"  - {grade_dir}/")

    # Calculate total size
    total_size = sum(f.stat().st_size for f in base_dir.rglob('*.mp3'))
    size_mb = total_size / (1024 * 1024)
    print(f"\nTotal size: {size_mb:.2f} MB")

    # Calculate cost estimate
    total_chars = sum(len(word) for _, words in grade_levels for word in words)
    if args.use_wavenet:
        cost = (total_chars / 1_000_000) * 16
        print(f"Estimated cost: ${cost:.2f} (WaveNet pricing)")
    else:
        print(f"Cost: FREE (within {total_chars:,} character free tier)")


if __name__ == '__main__':
    main()
