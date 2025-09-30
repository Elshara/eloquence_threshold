"""Seed global language profile placeholders for future refinement."""
from __future__ import annotations

import json
import os
import sys
from copy import deepcopy
from typing import Dict, List

import resource_paths

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
OUTPUT_FILE = str(resource_paths.language_seed_output_path())


def _entry(symbol: str, spoken: str, ipa: List[str], description: str, example: str, *notes: str) -> Dict[str, object]:
    return {
        "symbol": symbol,
        "spoken": spoken,
        "ipa": list(ipa),
        "description": description,
        "example": example,
        "notes": list(notes),
    }


SCRIPT_SAMPLES: Dict[str, List[Dict[str, object]]] = {
    "arabic_msa": [
        _entry("ق", "qaaf", ["q"], "Voiceless uvular stop with emphatic colouring", "قلب", "Backs adjacent vowels and lowers upper formants."),
        _entry("ض", "daad", ["dˤ"], "Pharyngealised alveolar stop", "ضوء", "Triggers pharyngeal harmony in following syllables."),
        _entry("ال", "al", ["al"], "Definite article prefix", "الشمس", "Assimilates to sun letters creating doubled consonants."),
    ],
    "arabic_egyptian": [
        _entry("ج", "gim", ["g"], "Egyptian g pronounced as hard /g/", "جمل", "Contrasts with /ʒ/ in Modern Standard Arabic.", "Carries secondary emphatic colour in stressed syllables."),
        _entry("ق", "ʔāf", ["ʔ"], "Glottal stop realisation of qaf", "قهوة", "Switches to /ʔ/ except in careful speech.", "Pairs with breathy release on preceding vowels."),
        _entry("ث", "sā", ["s"], "Dental fricative shifting to /s/", "ثانية", "Maintains /θ/ in formal recitation; everyday speech uses /s/."),
    ],
    "persian": [
        _entry("پ", "pe", ["p"], "Voiceless bilabial stop unique to Persian Arabic script", "پدر", "Pairs with aspirated burst at high emphasis values."),
        _entry("ژ", "zhe", ["ʒ"], "Postalveolar fricative", "ژاله", "Carries soft frication ideal for overtone sliders."),
        _entry("گ", "gāf", ["ɡ"], "Voiced velar stop", "گل", "Balances between hard /g/ and lenited /ɣ/ in casual speech."),
    ],
    "urdu": [
        _entry("ڑ", "ṛe", ["ɽ"], "Retroflex flap", "لڑکا", "Requires retroflex EQ emphasis for clarity."),
        _entry("خ", "khe", ["x"], "Voiceless velar fricative", "خواب", "Blend with whisper slider to emulate breathy releases."),
        _entry("ں", "noon ghunna", ["ŋ"], "Nasalisation marker", "ماں", "Signals nasalised vowels and word-final velar nasal."),
    ],
    "hebrew": [
        _entry("ח", "khet", ["χ"], "Voiceless uvular fricative", "חג", "Needs high-frequency boost for clarity."),
        _entry("צ", "tsadi", ["tsʼ"], "Ejective affricate in some traditions", "ציון", "Stress slider emphasises ejective burst."),
        _entry("שׁ", "shin", ["ʃ"], "Shin with dot on the right", "שלום", "Pairs with tone slider to avoid harsh hiss."),
    ],
    "ethiopic": [
        _entry("ሀ", "hä", ["h"], "Ethiopic letter ha", "ሀብታም", "Switches between [h] and [ħ] depending on emphasis."),
        _entry("ቀ", "qä", ["kʼ"], "Ejective velar stop", "ቀልጣፋ", "Inflection slider adds burst length to ejectives."),
        _entry("ጸ", "ṣä", ["sʼ"], "Ejective alveolar fricative", "ጸሐይ", "Needs overtone boost to differentiate from plain s."),
    ],
    "latin_sw": [
        _entry("ng", "ng", ["ŋ"], "Velar nasal before k/g", "ngoma", "Smoothness slider keeps nasal transitions fluid."),
        _entry("ny", "ny", ["ɲ"], "Palatal nasal sequence", "nyumbani", "Tone slider ensures bright palatal resonance."),
        _entry("ch", "ch", ["tʃ"], "Affricate pronounced with strong aspiration", "chakula", "Pair with emphasis to keep frication crisp."),
    ],
    "latin_yo": [
        _entry("ṣ", "sh", ["ʃ"], "Yoruba retroflex-like sh sound", "ṣọ́ọ̀ṣì", "Tone slider interacts with diacritics for pitch accents."),
        _entry("gb", "gb", ["ɡ͡b"], "Voiced labio-velar stop", "gbogbo", "Needs macro volume support to avoid clipping on release."),
        _entry("ọ", "aw", ["ɔ"], "Open-mid back rounded vowel", "ọmọ", "Subtone slider deepens low formants for contrast."),
    ],
    "latin_zu": [
        _entry("hl", "hl", ["ɬ"], "Voiceless lateral fricative", "hlonipha", "Overtones slider accentuates lateral hiss."),
        _entry("ngc", "ngc", ["ŋǃ"], "Nasal click cluster", "ngcobo", "Scope depth emphasises click resonance."),
        _entry("dl", "dl", ["ɮ"], "Voiced lateral fricative", "dlamini", "Smoothness slider prevents buzziness."),
    ],
    "latin_hausa": [
        _entry("ƙ", "k-alt", ["kʼ"], "Ejective velar stop", "ƙofa", "Inflection contour highlights ejective bursts."),
        _entry("sh", "sh", ["ʃ"], "Postalveolar fricative", "shiri", "Overtones slider brightens fricatives."),
        _entry("ts", "ts", ["tsʼ"], "Affricate with glottalic release", "tsuntsu", "Needs emphasis for sharp affricate transitions."),
    ],
    "cjk_mandarin": [
        _entry("的", "de", ["tɤ˙"], "Neutral tone particle", "我的", "Tone size slider keeps neutral tone subtle."),
    ],
    "cjk_cantonese": [
        _entry("的", "dik1", ["tɪk̚˥"], "High level final /k/ particle", "我的", "Tone slider emphasises level tone contrast."),
        _entry("咗", "zo2", ["tsɔ˧˥"], "Perfective marker", "食咗", "Inflection contour handles rising contour."),
        _entry("唔", "m4", ["m̩˨˩"], "Low falling nasal syllabic", "唔好", "Subtones slider supports low nasal resonance."),
    ],
    "hangul": [
        _entry("ㅎ", "hieut", ["h"], "Aspirated glottal fricative", "하늘", "Whisper slider adds airy release."),
        _entry("ㄹ", "rieul", ["ɾ", "l"], "Flap or lateral depending on position", "노랗다", "Scope depth transitions between flap and lateral states."),
        _entry("ㅆ", "ssang sieut", ["s͈"], "Fortis alveolar fricative", "쌀", "Emphasis slider strengthens tense consonants."),
    ],
    "latin_vi": [
        _entry("ă", "a-breve", ["ă"], "Short a with diacritic", "ăn", "Tone slider interacts with accent marks for contour tones."),
        _entry("đ", "dee", ["ɗ"], "Voiced implosive", "đi", "Scope depth emphasises implosive quality."),
        _entry("ngh", "ngh", ["ŋ"], "Velar nasal onset before front vowels", "nghỉ", "Smoothness slider keeps nasal onset gentle."),
    ],
    "thai": [
        _entry("ข", "kho khai", ["kʰ"], "Aspirated velar stop high class", "ขาว", "Tone slider handles high-rising vs falling contexts."),
        _entry("า", "sara aa", ["aː"], "Long open vowel", "บ้าน", "Macro volume keeps vowel length audible."),
        _entry("ไ", "sara ai mai malai", ["aj"], "Diphthong with tone marker", "ไทย", "Inflection contour transitions diphthong pitch smoothly."),
    ],
    "latin_id": [
        _entry("ng", "ng", ["ŋ"], "Velar nasal at onset", "ngeri", "Smoothness slider avoids popping on onset."),
        _entry("sy", "sy", ["ʃ"], "Loanword digraph", "syair", "Overtones slider brightens borrowed fricatives."),
        _entry("ny", "ny", ["ɲ"], "Palatal nasal", "nyala", "Tone slider emphasises nasal resonance in singing contexts."),
    ],
    "latin_ms": [
        _entry("ng", "ng", ["ŋ"], "Velar nasal", "langsung", "Macro volume ensures syllabic nasals remain audible."),
        _entry("sy", "sy", ["ʃ"], "Malay palatal fricative", "syarat", "Emphasis slider sharpens sibilant edges."),
        _entry("kh", "kh", ["x"], "Voiceless velar fricative in Arabic loans", "akhir", "Whisper slider adds airy release."),
    ],
    "latin_fil": [
        _entry("ng", "eng", ["ŋ"], "Velar nasal phoneme", "ngiti", "Smoothness slider prevents harsh transitions into vowels."),
        _entry("ñ", "enye", ["ɲ"], "Palatal nasal from Spanish loans", "piñata", "Tone slider can lighten borrowed words."),
        _entry("ts", "ts", ["ts"], "Affricate emphasised in names", "tse", "Emphasis slider helps maintain crisp onset."),
    ],
    "bengali": [
        _entry("ড়", "ṛa", ["ɽ"], "Retroflex flap", "পড়া", "Scope depth differentiates between flap and trill."),
        _entry("ঙ", "nga", ["ŋ"], "Velar nasal letter", "বাংলা", "Subtones slider supports nasal quality."),
        _entry("শ", "sha", ["ʃ"], "Palatal fricative", "শিশু", "Overtones slider brightens fricative energy."),
    ],
    "tamil": [
        _entry("ழ", "zha", ["ɻ"], "Retroflex approximant unique to Tamil", "தமிழ்", "Scope depth emphasises retroflex curve."),
        _entry("ண", "ṇa", ["ɳ"], "Retroflex nasal", "திண்ணை", "Subtones slider deepens nasal resonance."),
        _entry("ஐ", "ai", ["ai"], "Diphthong vowel", "ஐயம்", "Tone size slider can broaden diphthong transitions."),
    ],
    "telugu": [
        _entry("ఢ", "ḍha", ["ɖʱ"], "Voiced aspirated retroflex stop", "విడిఢి", "Macro volume maintains breathy release detail."),
        _entry("ఙ", "ṅa", ["ŋ"], "Velar nasal", "శంకు", "Subtones slider ensures nasal clarity before velars."),
        _entry("ౖ", "ai", ["ai"], "Dependent vowel sign", "నైతిక", "Tone slider helps articulate diphthong glides."),
    ],
    "malayalam": [
        _entry("ഴ", "zha", ["ɻ"], "Retroflex approximant", "മലയാളം", "Scope depth slider enhances retroflex swirl."),
        _entry("ങ്ക", "nga", ["ŋɡa"], "Velar nasal cluster", "അങ്കം", "Smoothness slider transitions nasal + stop gracefully."),
        _entry("റ്റ", "tta", ["ʈʈa"], "Geminated retroflex stop", "റ്റിൽ", "Emphasis slider sharpens geminate articulation."),
    ],
    "kannada": [
        _entry("ಳ", "ḷa", ["ɭ"], "Retroflex lateral", "ಕನ್ನಡ", "Scope depth slider emphasises retroflex release."),
        _entry("ಞ", "ña", ["ɲ"], "Palatal nasal", "ಜ್ಞಾನ", "Subtones slider shapes nasal resonance near palatal stops."),
        _entry("ೖ", "ai", ["ai"], "Diphthong", "ಹೈದರಾಬಾದ್", "Tone slider manages diphthong glides."),
    ],
    "marathi": [
        _entry("ळ", "ḷa", ["ɭ"], "Retroflex lateral", "मुळे", "Scope depth emphasises retroflex curvature."),
        _entry("ज्ञ", "gya", ["ɡjə", "dʒɲa"], "Complex conjunct consonant", "ज्ञान", "Smoothness slider blends consonant cluster variations."),
        _entry("ऋ", "ri", ["r̩"], "Syllabic r vowel", "ऋषी", "Subtones slider adds lower resonance to syllabic liquids."),
    ],
    "gujarati": [
        _entry("ળ", "ḷa", ["ɭ"], "Retroflex lateral unique to Gujarati", "કાળ", "Scope depth highlights retroflex articulation."),
        _entry("ઞ", "ña", ["ɲ"], "Palatal nasal", "જ્ઞાન", "Smoothness slider helps in conjunct clusters."),
        _entry("ૃ", "ru", ["r̩"], "Vowel sign vocalic r", "કૃપા", "Subtones slider increases vowel resonance."),
    ],
    "gurmukhi": [
        _entry("ੜ", "ṛa", ["ɽ"], "Retroflex flap specific to Punjabi", "ਕੜੀ", "Scope depth slider toggles between flap strength."),
        _entry("ਂ", "bindī", ["̃"], "Nasalisation marker", "ਮਾਂ", "Subtones slider emphasises nasal vowels."),
        _entry("ੱਧ", "ddha", ["d̪ːʱ"], "Geminated voiced aspirated stop", "ਅੱਧਾ", "Macro volume keeps aspiration audible during gemination."),
    ],
    "sinhala": [
        _entry("ඟ", "nga", ["ŋɡ"], "Pranasalised stop", "කඟ", "Smoothness slider preserves nasal-stop transition."),
        _entry("ඤ", "nya", ["ɲ"], "Palatal nasal letter", "ඤාණ", "Subtones slider accentuates nasal resonance."),
        _entry("ෆ", "fa", ["f"], "Voiceless labiodental fricative for loans", "ෆල", "Overtones slider brightens borrowed fricatives."),
    ],
    "khmer": [
        _entry("ញ", "nhô", ["ɲ"], "Palatal nasal", "ញ៉ាំ", "Smoothness slider blends nasal onset with vowel."),
        _entry("ឆ", "chhâ", ["cʰ"], "Aspirated affricate", "ឆ្លើយ", "Emphasis slider keeps aspiration sharp."),
        _entry("ួ", "uə", ["uə"], "Diphthong vowel", "កួរ", "Tone size slider ensures smooth glide."),
    ],
    "burmese": [
        _entry("င်", "ng", ["ŋ"], "Velar nasal final", "မြင်", "Subtones slider supports low nasal resonance."),
        _entry("ှ", "h modifier", ["ʰ"], "Aspiration diacritic", "ဖွဲ့", "Whisper slider shapes breathy onset."),
        _entry("ော", "aw", ["ɔ́"], "Diphthong with tone", "တော်", "Tone slider maintains rising contour."),
    ],
    "lao": [
        _entry("ຫນ", "hn", ["n"], "Silent h prefix controlling tone class", "ຫນອງ", "Tone slider responds to silent letter class shifts."),
        _entry("ໄ", "sara ai", ["aj"], "Diphthong vowel sign", "ໄກ່", "Inflection contour smooths tonal movement."),
        _entry("ອ", "o", ["ʔɔː"], "Glottal onset vowel carrier", "ເອື້ອ", "Macro volume ensures carrier vowel stays audible."),
    ],
    "nepali": [
        _entry("छ", "chha", ["tʃʰ"], "Aspirated affricate", "छात्र", "Emphasis slider clarifies aspiration in clusters."),
        _entry("ङ", "nga", ["ŋ"], "Velar nasal", "नेपाली", "Subtones slider keeps nasal resonance present."),
        _entry("श्र", "shra", ["ʃr"], "Consonant cluster", "श्रद्धा", "Smoothness slider merges cluster articulation."),
    ],
    "cyrillic_ru": [
        _entry("щ", "shcha", ["ɕː"], "Long palatalised fricative", "ещё", "Overtones slider refines soft fricative texture."),
        _entry("ы", "y", ["ɨ"], "Close central vowel", "сы", "Tone slider balances central resonance."),
        _entry("ж", "zhe", ["ʐ"], "Voiced retroflex fricative", "жук", "Subtones slider prevents muddiness in low register."),
    ],
    "cyrillic_uk": [
        _entry("ї", "yi", ["ji"], "Dotted i with glide", "їжа", "Tone slider smooths glide to vowel."),
        _entry("ґ", "ghe", ["ɡ"], "Voiced velar stop distinct from /ɦ/", "ґанок", "Emphasis slider keeps plosive crisp."),
        _entry("є", "ye", ["je"], "Palatalised vowel", "європа", "Smoothness slider handles palatal transitions."),
    ],
    "latin_pl": [
        _entry("ł", "w", ["w"], "Polish dark l", "łuk", "Subtones slider darkens vowel transitions."),
        _entry("ś", "sh", ["ɕ"], "Soft alveolo-palatal fricative", "świt", "Overtones slider adds gentle brightness."),
        _entry("cz", "ch", ["tʂ"], "Retroflex affricate", "czemu", "Emphasis slider keeps affricate attack defined."),
    ],
    "latin_cs": [
        _entry("ř", "rz", ["r̝"], "Raised alveolar trill", "řeka", "Scope depth slider manages trill intensity."),
        _entry("ch", "kh", ["x"], "Voiceless velar fricative", "chléb", "Whisper slider adds airy release."),
        _entry("ň", "ny", ["ɲ"], "Palatal nasal", "kůň", "Smoothness slider eases nasal transitions."),
    ],
    "latin_tr": [
        _entry("ş", "sh", ["ʃ"], "Voiceless postalveolar fricative", "şarkı", "Overtones slider brightens fricative."),
        _entry("ğ", "soft g", ["ɰ"], "Voiced velar approximant lengthening vowels", "dağ", "Scope depth slider keeps vowel extension natural."),
        _entry("ı", "undotted ı", ["ɯ"], "Close back unrounded vowel", "ışık", "Subtones slider ensures warm timbre."),
    ],
    "greek": [
        _entry("θ", "theta", ["θ"], "Voiceless dental fricative", "θέμα", "Emphasis slider prevents smearing with /s/."),
        _entry("γ", "gamma", ["ɣ"], "Voiced velar fricative", "γάλα", "Smoothness slider avoids harsh transitions."),
        _entry("ξ", "xi", ["ks"], "Cluster consonant", "ξένος", "Tone size slider keeps cluster intelligible."),
    ],
    "latin_nl": [
        _entry("ij", "ij", ["ɛi"], "Diphthong pronounced as /ɛi/", "ijs", "Tone slider keeps diphthong bright."),
        _entry("sch", "sch", ["sx"], "Sibilant + velar fricative", "school", "Whisper slider balances dual frication."),
        _entry("ui", "ui", ["œy"], "Rounded diphthong", "huis", "Scope depth slider supports rounded glide."),
    ],
    "latin_sv": [
        _entry("sj", "sj", ["ɧ"], "Voiceless coarticulated fricative", "sjö", "Overtones slider captures diffuse hiss."),
        _entry("tj", "tj", ["ɕ"], "Palatal fricative", "tjej", "Tone slider brightens soft fricatives."),
        _entry("å", "o-ring", ["oː"], "Open-mid back rounded vowel", "båt", "Macro volume keeps long vowel resonant."),
    ],
    "latin_nb": [
        _entry("kj", "kj", ["ç"], "Palatal fricative", "kjære", "Tone slider keeps fricative gentle."),
        _entry("skj", "skj", ["ʂ"], "Retroflex fricative", "skjorte", "Overtones slider clarifies retroflex energy."),
        _entry("øy", "øy", ["øːy"], "Rounded diphthong", "øy", "Scope depth slider maintains rounded glide."),
    ],
    "latin_da": [
        _entry("dg", "dg", ["tˢ"], "Affricate in loans", "adgang", "Emphasis slider keeps affricate crisp."),
        _entry("r", "r", ["ʁ"], "Uvular approximant", "rød", "Subtones slider keeps uvular resonance warm."),
        _entry("ø", "oe", ["ø"], "Front rounded vowel", "sø", "Tone slider balances brightness."),
    ],
    "latin_fi": [
        _entry("ng", "ng", ["ŋ"], "Velar nasal", "sängyssä", "Smoothness slider connects nasal to following consonant."),
        _entry("y", "y", ["y"], "Front rounded vowel", "yö", "Tone slider keeps rounded vowel bright."),
        _entry("ä", "ä", ["æ"], "Open front vowel", "ääni", "Subtones slider supports open vowel warmth."),
    ],
}


LANGUAGE_SPECS = [
    {
        "id": "ar-msa-seed",
        "language": "ar",
        "display": "Arabic (Modern Standard) – emphatic backbone",
        "description": "Seeded MSA profile capturing emphatic coronals and the sun/moon assimilation patterns.",
        "tags": ["arabic", "msa", "seed", "lang:ar"],
        "stress": [
            "Stress defaults to the final heavy syllable unless vowel length or sukun dictates otherwise.",
            "Qur'anic recitation keeps long vowels fully articulated even at fast rates."
        ],
        "sentence": [
            "Verb–Subject–Object remains the neutral order for narrative speech.",
            "Adjectives typically follow nouns and inherit definiteness from the article."
        ],
        "grammar": [
            "Sun letters assimilate the /l/ in the definite article while moon letters retain it.",
            "Emphatic consonants back neighbouring vowels and call for darker timbre settings."
        ],
        "template_id": "eloquence-seed-ar-msa",
        "template_name": "Eloquence seed – Arabic (MSA)",
        "template_description": "Placeholder timbre emphasising emphatic consonants and uvular frication while we gather community recordings.",
        "template_tags": ["eloquence", "seed", "arabic", "placeholder"],
        "template_variant": "1",
        "template_gender": 0,
        "script": "arabic_msa",
        "param_overrides": {"pitch": 96, "headSize": 118, "roughness": 24, "breathiness": 18},
        "advanced_overrides": {"timbre": 108, "tone": 96, "vocalLayers": 104, "overtones": 92, "subtones": 110, "vocalRange": 102}
    },
    {
        "id": "ar-eg-seed",
        "language": "ar-EG",
        "display": "Arabic (Egyptian) – colloquial glide",
        "description": "Captures Cairene consonant shifts (gīm→/g/, qāf→/ʔ/) so phoneme EQ can mimic everyday Egyptian Arabic.",
        "tags": ["arabic", "egyptian", "seed", "lang:ar"],
        "stress": [
            "Colloquial stress leans toward penultimate syllables unless closed final syllables intervene.",
            "Sentence-final questions rise sharply; tone slider should mirror that cadence."
        ],
        "sentence": [
            "Verb–Subject–Object dominates conversational speech though topicalisation is common.",
            "Negation wraps verbs with ما ... ش framing that benefits from macro volume balance."
        ],
        "grammar": [
            "Dental fricatives merge with /s/ and /z/ in casual contexts, so emphasis must recover clarity.",
            "The glottal realisation of qāf requires extra whisper control to avoid harsh stops."
        ],
        "template_id": "eloquence-seed-ar-eg",
        "template_name": "Eloquence seed – Arabic (Egyptian)",
        "template_description": "Placeholder voice tuned for Cairene consonant mergers and the breezy Egyptian cadence.",
        "template_tags": ["eloquence", "seed", "arabic", "egyptian"],
        "template_variant": "1",
        "template_gender": 1,
        "script": "arabic_egyptian",
        "param_overrides": {"rate": 106, "pitch": 108, "inflection": 58, "breathiness": 26},
        "advanced_overrides": {"emphasis": 112, "tone": 104, "whisper": 112, "macroVolume": 108}
    },
    {
        "id": "fa-ir-seed",
        "language": "fa",
        "display": "Persian (Farsi) – smooth ezafe",
        "description": "Seeded Persian profile that foregrounds ezafe liaisons and the soft postalveolar fricatives common in Tehrani speech.",
        "tags": ["persian", "farsi", "seed", "lang:fa"],
        "stress": [
            "Stress falls on the final syllable unless enclitics are present.",
            "Colloquial intonation keeps declaratives falling quickly after the verb."
        ],
        "sentence": [
            "Subject–Object–Verb order pairs with light ezafe vowels between linked nouns.",
            "Question particles such as آیا cue rising inflection even with falling lexical accents."
        ],
        "grammar": [
            "Voiceless stops often aspirate; emphasis and smoothness should balance that breathiness.",
            "Distinct letters پ, ژ, and گ need overtone support to avoid collapsing into Arabic neighbours."
        ],
        "template_id": "eloquence-seed-fa-ir",
        "template_name": "Eloquence seed – Persian",
        "template_description": "Placeholder tuning that keeps Persian fricatives silky and highlights ezafe vowels for chaining nouns.",
        "template_tags": ["eloquence", "seed", "persian"],
        "template_variant": "2",
        "template_gender": 1,
        "script": "persian",
        "param_overrides": {"rate": 98, "pitch": 114, "inflection": 60, "breathiness": 28},
        "advanced_overrides": {"timbre": 112, "smoothness": 118, "tone": 110}
    },
    {
        "id": "ur-pk-seed",
        "language": "ur",
        "display": "Urdu – poetic glide",
        "description": "Urdu placeholder capturing retroflex flaps and aspirated stops used in ghazal recitation and newscasts.",
        "tags": ["urdu", "seed", "lang:ur"],
        "stress": [
            "Stress remains penultimate in native words but shifts with Persian and Arabic loans.",
            "Poetic couplets prefer even pacing; macro volume should keep nasal vowels audible."
        ],
        "sentence": [
            "Subject–Object–Verb order dominates while subordinate clauses precede the verb.",
            "Postpositions follow nouns and influence tone contour on trailing vowels."
        ],
        "grammar": [
            "Retroflex consonants and aspiration need scope depth plus whisper to avoid smearing.",
            "Nasalisation marker نٙ (noon ghunna) calls for subtone boosts to avoid drop-outs."
        ],
        "template_id": "eloquence-seed-ur-pk",
        "template_name": "Eloquence seed – Urdu",
        "template_description": "Placeholder voice balancing poetic softness with the textured consonants of modern Urdu broadcasts.",
        "template_tags": ["eloquence", "seed", "urdu"],
        "template_variant": "3",
        "template_gender": 0,
        "script": "urdu",
        "param_overrides": {"rate": 94, "pitch": 112, "inflection": 64, "headSize": 116},
        "advanced_overrides": {"emphasis": 116, "subtones": 112, "whisper": 108, "scopeDepth": 108}
    },
    {
        "id": "he-il-seed",
        "language": "he",
        "display": "Hebrew – modern articulation",
        "description": "Modern Israeli Hebrew placeholder accentuating uvular frication and ejective-like tsadi bursts.",
        "tags": ["hebrew", "seed", "lang:he"],
        "stress": [
            "Lexical stress varies but often falls on the final syllable; the tone slider should highlight last vowels.",
            "Yes/no questions rise sharply on the final syllable, while wh-questions show wider inflection.",
        ],
        "sentence": [
            "Verb–Subject–Object is common in formal speech, with Subject–Verb alternations in conversation.",
            "Construct state nouns bind tightly; smoothness keeps these clusters intelligible."
        ],
        "grammar": [
            "Khet /χ/ and tav /t/ assimilation require overtones to preserve contrast against /s/ and /ʃ/.",
            "Tsere and kamatz vowels change quality with stress; macro volume preserves the shift."
        ],
        "template_id": "eloquence-seed-he-il",
        "template_name": "Eloquence seed – Hebrew",
        "template_description": "Placeholder timbre tuned for uvular consonants and modern Israeli cadence.",
        "template_tags": ["eloquence", "seed", "hebrew"],
        "template_variant": "2",
        "template_gender": 0,
        "script": "hebrew",
        "param_overrides": {"rate": 104, "pitch": 118, "inflection": 56},
        "advanced_overrides": {"emphasis": 120, "overtones": 116, "macroVolume": 104}
    },
    {
        "id": "am-et-seed",
        "language": "am",
        "display": "Amharic – ejective cadence",
        "description": "Placeholder emphasising Amharic ejectives and the seven-syllable abugida patterns.",
        "tags": ["amharic", "seed", "lang:am"],
        "stress": [
            "Penultimate stress is common, with pitch lowering on final syllables.",
            "Questions add rising contour that should engage inflection sliders."
        ],
        "sentence": [
            "Subject–Object–Verb order with rich verb inflection; subordinate clauses take verb-final participles.",
            "Relative clauses introduce pronoun markers that alter rhythm and require macro volume balance."
        ],
        "grammar": [
            "Ejectives need strong emphasis but limited overtones to avoid harshness.",
            "Gemination is phonemic; smoothness must preserve doubled consonants distinctly."
        ],
        "template_id": "eloquence-seed-am-et",
        "template_name": "Eloquence seed – Amharic",
        "template_description": "Placeholder voice projecting Amharic ejectives with balanced nasal vowels.",
        "template_tags": ["eloquence", "seed", "amharic"],
        "template_variant": "1",
        "template_gender": 0,
        "script": "ethiopic",
        "param_overrides": {"rate": 92, "pitch": 116, "inflection": 68, "roughness": 22},
        "advanced_overrides": {"emphasis": 126, "scopeDepth": 112, "vocalRange": 108}
    },
    {
        "id": "ha-ng-seed",
        "language": "ha",
        "display": "Hausa – vibrant glottalic stops",
        "description": "Captures Hausa ejective stops and high/low tone contrasts for the Latin orthography.",
        "tags": ["hausa", "seed", "lang:ha"],
        "stress": [
            "Tone rather than stress carries contrast; tone slider should remain responsive across phrases.",
            "Emphatic focus raises pitch and loudness on the final syllable."
        ],
        "sentence": [
            "Subject–Verb–Object order dominates with prepositions preceding noun phrases.",
            "Relative clauses follow nouns and require smoothness to keep glottalic bursts legible."
        ],
        "grammar": [
            "Ejective consonants need inflection contour to emphasise release.",
            "Nasal vowels appear before certain consonants; subtone boosts keep them resonant."
        ],
        "template_id": "eloquence-seed-ha-ng",
        "template_name": "Eloquence seed – Hausa",
        "template_description": "Placeholder Hausa tuning to keep ejective bursts crisp and tones balanced.",
        "template_tags": ["eloquence", "seed", "hausa"],
        "template_variant": "3",
        "template_gender": 0,
        "script": "latin_hausa",
        "param_overrides": {"rate": 104, "pitch": 122, "inflection": 70},
        "advanced_overrides": {"emphasis": 124, "tone": 128, "scopeDepth": 110}
    },
    {
        "id": "sw-ke-seed",
        "language": "sw",
        "display": "Swahili – coastal clarity",
        "description": "Swahili placeholder emphasising prenasalised consonants and open vowels for East African dialects.",
        "tags": ["swahili", "seed", "lang:sw"],
        "stress": [
            "Stress is penultimate; macro volume keeps long final vowels audible.",
            "Questions raise pitch on the final mora and need tone slider support."
        ],
        "sentence": [
            "Subject markers attach to verbs; maintaining smoothness keeps these prefixes distinct.",
            "Noun classes drive agreement prefixes across clauses and require consistent rhythm."
        ],
        "grammar": [
            "Prenasalised clusters (ng, ny) need smooth transitions to avoid clicks.",
            "Loan digraph ch retains affricate quality; emphasis slider should brighten it."
        ],
        "template_id": "eloquence-seed-sw-ke",
        "template_name": "Eloquence seed – Swahili",
        "template_description": "Placeholder voice blending coastal Swahili openness with crisp consonant clusters.",
        "template_tags": ["eloquence", "seed", "swahili"],
        "template_variant": "2",
        "template_gender": 1,
        "script": "latin_sw",
        "param_overrides": {"rate": 108, "pitch": 120, "inflection": 54},
        "advanced_overrides": {"emphasis": 112, "smoothness": 120, "vocalLayers": 106}
    },
    {
        "id": "yo-ng-seed",
        "language": "yo",
        "display": "Yoruba – tonal resonance",
        "description": "Yoruba placeholder covering three-level tone diacritics and labio-velar stops.",
        "tags": ["yoruba", "seed", "lang:yo"],
        "stress": [
            "Tone tiers (high, mid, low) matter more than stress; tone size slider must track diacritics.",
            "Downstep sequences benefit from macro volume to avoid drop-offs."
        ],
        "sentence": [
            "Subject–Verb–Object with preverbal tense/aspect particles that change tonal melody.",
            "Relative clauses follow nouns and often drop prenasalisation cues unless emphasis is applied."
        ],
        "grammar": [
            "Labio-velar stop /ɡ͡b/ needs scope depth to maintain separation from plain /b/.",
            "Rhotacised vowels in loanwords benefit from overtone boosts."
        ],
        "template_id": "eloquence-seed-yo-ng",
        "template_name": "Eloquence seed – Yoruba",
        "template_description": "Placeholder Yoruba timbre tuned for three-level tone diacritics and labio-velar stops.",
        "template_tags": ["eloquence", "seed", "yoruba"],
        "template_variant": "4",
        "template_gender": 1,
        "script": "latin_yo",
        "param_overrides": {"rate": 100, "pitch": 126, "inflection": 78},
        "advanced_overrides": {"tone": 136, "toneSize": 124, "vocalRange": 118, "subtones": 116}
    },
    {
        "id": "zu-za-seed",
        "language": "zu",
        "display": "Zulu – click-rich texture",
        "description": "Zulu placeholder mixing click consonants with lateral fricatives to prep the phoneme editor.",
        "tags": ["zulu", "seed", "lang:zu"],
        "stress": [
            "Penultimate stress drives rhythm; macro volume should protect the final syllable.",
            "Wh-questions trigger rising-falling intonation requiring inflection contour support."
        ],
        "sentence": [
            "Subject markers prefix verbs, and object markers embed before the stem; smoothness keeps them distinct.",
            "Relative clauses use concord prefixes; emphasis must highlight click releases in these contexts."
        ],
        "grammar": [
            "Clicks paired with nasals or lateral releases need scope depth and overtones to avoid muddy blending.",
            "Voiced lateral fricatives prefer higher smoothness values to stay stable." 
        ],
        "template_id": "eloquence-seed-zu-za",
        "template_name": "Eloquence seed – Zulu",
        "template_description": "Placeholder Zulu timbre that keeps click clusters sharp without harsh resonance.",
        "template_tags": ["eloquence", "seed", "zulu"],
        "template_variant": "4",
        "template_gender": 0,
        "script": "latin_zu",
        "param_overrides": {"rate": 102, "pitch": 116, "inflection": 68, "roughness": 26},
        "advanced_overrides": {"overtones": 128, "scopeDepth": 120, "vocalLayers": 108}
    },
    {
        "id": "zh-cn-seed",
        "language": "zh-CN",
        "display": "Chinese (Mandarin) – tonal baseline",
        "description": "Mandarin placeholder emphasising neutral tones, retroflex affricates, and aspect particles.",
        "tags": ["mandarin", "seed", "lang:zh"],
        "stress": [
            "Lexical tone carries primary contrast; neutral tone syllables need macro volume support.",
            "Sentence-final particles adjust contour; inflection contour should mirror rising/falling shifts."
        ],
        "sentence": [
            "Topic–comment structures are frequent; smoothness maintains clarity across tonal resets.",
            "Resultative compounds require emphasis to differentiate successive tone sandhi outcomes."
        ],
        "grammar": [
            "Retroflex initials zh/ch/sh need overtone management to avoid hissing.",
            "Neutral tone particles such as 的 and 了 demand macro volume to stay audible after full-tone syllables."
        ],
        "template_id": "eloquence-seed-zh-cn",
        "template_name": "Eloquence seed – Mandarin",
        "template_description": "Placeholder Mandarin mapping to keep retroflex affricates crisp and neutral tones audible.",
        "template_tags": ["eloquence", "seed", "mandarin"],
        "template_variant": "1",
        "template_gender": 0,
        "script": "cjk_mandarin",
        "param_overrides": {"rate": 112, "pitch": 124, "inflection": 80},
        "advanced_overrides": {"tone": 138, "toneSize": 126, "macroVolume": 110, "vocalRange": 122}
    },
    {
        "id": "yue-hk-seed",
        "language": "yue-Hant-HK",
        "display": "Chinese (Cantonese) – six-tone contour",
        "description": "Cantonese placeholder covering high level, low falling, and nasal-only syllables.",
        "tags": ["cantonese", "seed", "lang:yue"],
        "stress": [
            "Tone categories define contrast; the tone slider must stay sensitive across six level and contour tones.",
            "Sentence particles add attitudinal nuance; inflection contour keeps the rising patterns natural."
        ],
        "sentence": [
            "Topic-prominent clauses rely on aspect particles like 咗 and 緊; smoothness ensures stacking remains legible.",
            "Classifiers precede nouns and alter cadence; macro volume should emphasise low-tone classifiers."
        ],
        "grammar": [
            "Entering tone finals (-p/-t/-k) need emphasis for stop closure.",
            "Syllabic nasals such as 唔 require subtone support to avoid drop-outs."
        ],
        "template_id": "eloquence-seed-yue-hk",
        "template_name": "Eloquence seed – Cantonese",
        "template_description": "Placeholder Cantonese timbre tuned for level tones and syllabic nasals.",
        "template_tags": ["eloquence", "seed", "cantonese"],
        "template_variant": "2",
        "template_gender": 1,
        "script": "cjk_cantonese",
        "param_overrides": {"rate": 116, "pitch": 130, "inflection": 88},
        "advanced_overrides": {"tone": 142, "toneSize": 130, "macroVolume": 112, "scopeDepth": 114}
    },
    {
        "id": "ko-kr-seed",
        "language": "ko",
        "display": "Korean – fortis balance",
        "description": "Korean placeholder balancing tense consonants, aspiration, and vowel harmony cues.",
        "tags": ["korean", "seed", "lang:ko"],
        "stress": [
            "Syllable timing is even; smoothness should prioritise transitions over stress.",
            "Sentence-final particles modulate politeness levels; inflection sliders reflect rising pitch in questions."
        ],
        "sentence": [
            "Subject–Object–Verb order with topic markers 은/는; macro volume keeps particles audible.",
            "Honorific endings lengthen vowels; scope depth supports contrast between declaratives and questions."
        ],
        "grammar": [
            "Fortis consonants require high emphasis while maintaining controlled overtones.",
            "ㄹ alternates between flap and lateral; smoothness mediates position-based transitions."
        ],
        "template_id": "eloquence-seed-ko-kr",
        "template_name": "Eloquence seed – Korean",
        "template_description": "Placeholder Korean tuning for tense consonants and polite sentence endings.",
        "template_tags": ["eloquence", "seed", "korean"],
        "template_variant": "3",
        "template_gender": 0,
        "script": "hangul",
        "param_overrides": {"rate": 108, "pitch": 118, "inflection": 72, "headSize": 114},
        "advanced_overrides": {"emphasis": 128, "smoothness": 124, "scopeDepth": 116}
    },
    {
        "id": "vi-vn-seed",
        "language": "vi",
        "display": "Vietnamese – six-tone brilliance",
        "description": "Vietnamese placeholder highlighting tone contours, implosives, and short vowels.",
        "tags": ["vietnamese", "seed", "lang:vi"],
        "stress": [
            "Tone diacritics encode contour; tone slider must track both acute and dot diacritics.",
            "Northern rising tones need inflection contour to avoid overshooting."
        ],
        "sentence": [
            "Topic-comment with classifiers; macro volume emphasises short function words.",
            "Question particles like không require rising final pitch; tone size balances the contour."
        ],
        "grammar": [
            "Implosive /ɓ/ and /ɗ/ need scope depth plus subtone support.",
            "ngh onset before front vowels should remain smooth to avoid plosive artefacts."
        ],
        "template_id": "eloquence-seed-vi-vn",
        "template_name": "Eloquence seed – Vietnamese",
        "template_description": "Placeholder Vietnamese timbre emphasising contour tones and implosives.",
        "template_tags": ["eloquence", "seed", "vietnamese"],
        "template_variant": "1",
        "template_gender": 1,
        "script": "latin_vi",
        "param_overrides": {"rate": 118, "pitch": 134, "inflection": 90},
        "advanced_overrides": {"tone": 144, "toneSize": 132, "vocalRange": 126, "scopeDepth": 110}
    },
    {
        "id": "th-th-seed",
        "language": "th",
        "display": "Thai – tonal glide",
        "description": "Thai placeholder featuring high-class consonants, long vowels, and diphthongs.",
        "tags": ["thai", "seed", "lang:th"],
        "stress": [
            "Tone supersedes stress; tone slider should reflect contour shifts triggered by class markers.",
            "Sentence-final particles (ครับ, ค่ะ) require subtle rising inflection."
        ],
        "sentence": [
            "Subject–Verb–Object with frequent topic fronting; smoothness keeps topicalised phrases fluid.",
            "Classifier constructions need macro volume to highlight numeral and classifier pairings."
        ],
        "grammar": [
            "Aspirated stops (ข, ถ, ผ) require emphasis to stay distinct from unaspirated pairs.",
            "Long vowels mark lexical contrast; macro volume ensures length perception."
        ],
        "template_id": "eloquence-seed-th-th",
        "template_name": "Eloquence seed – Thai",
        "template_description": "Placeholder Thai mapping for high-class consonants and long vowels.",
        "template_tags": ["eloquence", "seed", "thai"],
        "template_variant": "2",
        "template_gender": 0,
        "script": "thai",
        "param_overrides": {"rate": 112, "pitch": 128, "inflection": 84},
        "advanced_overrides": {"tone": 140, "toneSize": 128, "macroVolume": 112}
    },
    {
        "id": "id-id-seed",
        "language": "id",
        "display": "Indonesian – archipelago clarity",
        "description": "Indonesian placeholder capturing prenasalised onsets and clear loan consonants.",
        "tags": ["indonesian", "seed", "lang:id"],
        "stress": [
            "Stress is generally penultimate but light; macro volume keeps phrase-final vowels audible.",
            "Questions and focus words rely on pitch height rather than stress; inflection slider should track this."
        ],
        "sentence": [
            "Subject–Verb–Object order with optional topicalisation; smoothness ensures vowel harmony in reduplication.",
            "Particles like kok and dong adjust pragmatics and need tone adjustments for nuance."
        ],
        "grammar": [
            "Prenasalised ng-, ny- clusters should remain smooth to avoid pops.",
            "Loan digraph sy should sparkle via overtone boosts without sounding harsh."
        ],
        "template_id": "eloquence-seed-id-id",
        "template_name": "Eloquence seed – Indonesian",
        "template_description": "Placeholder Indonesian timbre mixing velar nasals with bright loanword fricatives.",
        "template_tags": ["eloquence", "seed", "indonesian"],
        "template_variant": "3",
        "template_gender": 0,
        "script": "latin_id",
        "param_overrides": {"rate": 110, "pitch": 118, "inflection": 60},
        "advanced_overrides": {"smoothness": 118, "tone": 108}
    },
    {
        "id": "ms-my-seed",
        "language": "ms",
        "display": "Malay – peninsular warmth",
        "description": "Malay placeholder aligned with peninsular pronunciation, balancing Arabic loans and Malay vowels.",
        "tags": ["malay", "seed", "lang:ms"],
        "stress": [
            "Stress tends to the penultimate syllable; macro volume keeps open finals resonant.",
            "Tone is not phonemic but rising questioning intonation uses the inflection slider heavily."
        ],
        "sentence": [
            "Subject–Verb–Object with preposed relative clauses; smoothness preserves clarity when pronoun clitics attach.",
            "Reduplication adds rhythmic pairs; emphasis ensures repeated syllables remain crisp."
        ],
        "grammar": [
            "Arabic loan fricative kh requires whisper plus overtones for airy release.",
            "Velar nasals appear word-finally; subtone slider keeps them warm."
        ],
        "template_id": "eloquence-seed-ms-my",
        "template_name": "Eloquence seed – Malay",
        "template_description": "Placeholder Malay timbre mixing Arabic loan consonants with mellow Malay vowels.",
        "template_tags": ["eloquence", "seed", "malay"],
        "template_variant": "2",
        "template_gender": 1,
        "script": "latin_ms",
        "param_overrides": {"rate": 106, "pitch": 116, "inflection": 58},
        "advanced_overrides": {"smoothness": 116, "whisper": 112}
    },
    {
        "id": "fil-ph-seed",
        "language": "fil",
        "display": "Filipino – Tagalog clarity",
        "description": "Filipino placeholder addressing velar nasals, Spanish ñ loans, and affricate onsets.",
        "tags": ["filipino", "tagalog", "seed", "lang:fil"],
        "stress": [
            "Stress alternates between penultimate and ultimate; macro volume should announce the stressed vowel.",
            "Question particles like ba rely on rising contours; inflection slider should mirror the shift."
        ],
        "sentence": [
            "Verb–Subject–Object common with focus markers; smoothness ensures enclitic pronouns stay audible.",
            "Aspect markers (mag-, nag-, -um-) adjust vowel quality; emphasis keeps transitions clear."
        ],
        "grammar": [
            "Velar nasal ng as a standalone syllable needs subtle subtone support.",
            "Spanish loan ñ requires overtone brightening to avoid blending with ny."
        ],
        "template_id": "eloquence-seed-fil-ph",
        "template_name": "Eloquence seed – Filipino",
        "template_description": "Placeholder Filipino timbre mixing Austronesian vowels with Spanish consonant loans.",
        "template_tags": ["eloquence", "seed", "filipino"],
        "template_variant": "3",
        "template_gender": 1,
        "script": "latin_fil",
        "param_overrides": {"rate": 108, "pitch": 120, "inflection": 62},
        "advanced_overrides": {"smoothness": 120, "emphasis": 114, "tone": 108}
    },
    {
        "id": "bn-bd-seed",
        "language": "bn",
        "display": "Bengali – retroflex melody",
        "description": "Bengali placeholder emphasising retroflex flaps, palatal fricatives, and nasal vowels.",
        "tags": ["bengali", "seed", "lang:bn"],
        "stress": [
            "Stress is typically on the penultimate syllable but light; macro volume retains vowel colour.",
            "Questions rise at the end; tone slider should support the upward glide."
        ],
        "sentence": [
            "Subject–Object–Verb order with postpositions; smoothness keeps conjunct letters legible.",
            "Compound verbs pair light verbs; emphasis ensures the semantic verb remains forward."
        ],
        "grammar": [
            "Retroflex flap ড় requires scope depth to avoid merging with alveolar d.",
            "Palatal fricatives benefit from overtone boost to stay bright."
        ],
        "template_id": "eloquence-seed-bn-bd",
        "template_name": "Eloquence seed – Bengali",
        "template_description": "Placeholder Bengali timbre tuned for retroflex flaps and palatal fricatives.",
        "template_tags": ["eloquence", "seed", "bengali"],
        "template_variant": "2",
        "template_gender": 1,
        "script": "bengali",
        "param_overrides": {"rate": 100, "pitch": 122, "inflection": 66},
        "advanced_overrides": {"scopeDepth": 116, "overtones": 118, "subtones": 112}
    },
    {
        "id": "ta-in-seed",
        "language": "ta",
        "display": "Tamil – classical resonance",
        "description": "Tamil placeholder anchoring retroflex approximants and geminate stops for Sangam-style articulation.",
        "tags": ["tamil", "seed", "lang:ta"],
        "stress": [
            "Stress is weak; rhythm flows from syllable timing so smoothness should stay high.",
            "Question particles such as ஆ? at the end raise pitch; inflection slider must respond accordingly."
        ],
        "sentence": [
            "Subject–Object–Verb order with agglutinative suffixes; macro volume keeps case endings audible.",
            "Relative participles precede nouns; emphasis keeps retroflex clusters intelligible."
        ],
        "grammar": [
            "Unique retroflex approximant ழ requires scope depth for clarity.",
            "Geminated retroflex stops need high emphasis without saturating overtones."
        ],
        "template_id": "eloquence-seed-ta-in",
        "template_name": "Eloquence seed – Tamil",
        "template_description": "Placeholder Tamil timbre balancing classical retroflex consonants with smooth syllable timing.",
        "template_tags": ["eloquence", "seed", "tamil"],
        "template_variant": "1",
        "template_gender": 0,
        "script": "tamil",
        "param_overrides": {"rate": 94, "pitch": 114, "inflection": 58, "headSize": 118},
        "advanced_overrides": {"scopeDepth": 120, "subtones": 118, "emphasis": 124}
    },
    {
        "id": "te-in-seed",
        "language": "te",
        "display": "Telugu – lyrical aspiration",
        "description": "Telugu placeholder centred on aspirated retroflexes, velar nasals, and diphthong glides.",
        "tags": ["telugu", "seed", "lang:te"],
        "stress": [
            "Stress remains light; musical metre focuses on mora counts requiring smooth transitions.",
            "Yes/no questions rise slightly; inflection contour should emphasise the glide." 
        ],
        "sentence": [
            "Subject–Object–Verb with extensive participial clauses; smoothness keeps sandhi boundaries intelligible.",
            "Object markers like -ni shift rhythm; macro volume ensures suffix vowels stay present."
        ],
        "grammar": [
            "Aspirated retroflex stops need macro volume plus emphasis to maintain breathy release.",
            "Dependent vowel signs (like ఐ) must glide cleanly; tone slider assists the transition."
        ],
        "template_id": "eloquence-seed-te-in",
        "template_name": "Eloquence seed – Telugu",
        "template_description": "Placeholder Telugu voice balancing aspirated retroflexes with smooth vowel glides.",
        "template_tags": ["eloquence", "seed", "telugu"],
        "template_variant": "2",
        "template_gender": 0,
        "script": "telugu",
        "param_overrides": {"rate": 96, "pitch": 118, "inflection": 62},
        "advanced_overrides": {"macroVolume": 112, "scopeDepth": 116, "subtones": 114}
    },
    {
        "id": "ml-in-seed",
        "language": "ml",
        "display": "Malayalam – retroflex waves",
        "description": "Malayalam placeholder tuned for retroflex approximants, nasal clusters, and geminated stops.",
        "tags": ["malayalam", "seed", "lang:ml"],
        "stress": [
            "Stress is weak but long vowels extend rhythm; macro volume preserves their length.",
            "Questions raise pitch softly; inflection slider should keep endings lively."
        ],
        "sentence": [
            "Subject–Object–Verb order with extensive agglutination; smoothness ensures morpheme boundaries remain clear.",
            "Relative clauses use participles; emphasis maintains clarity in consonant clusters."
        ],
        "grammar": [
            "Retroflex approximant ഴ needs scope depth; geminated retroflex stops need strong emphasis.",
            "Velar nasal clusters demand smoothness to avoid clicks."
        ],
        "template_id": "eloquence-seed-ml-in",
        "template_name": "Eloquence seed – Malayalam",
        "template_description": "Placeholder Malayalam timbre emphasising retroflex waves and nasal clusters.",
        "template_tags": ["eloquence", "seed", "malayalam"],
        "template_variant": "3",
        "template_gender": 1,
        "script": "malayalam",
        "param_overrides": {"rate": 92, "pitch": 112, "inflection": 58},
        "advanced_overrides": {"scopeDepth": 122, "smoothness": 120, "subtones": 120}
    },
    {
        "id": "kn-in-seed",
        "language": "kn",
        "display": "Kannada – gentle palatals",
        "description": "Kannada placeholder covering retroflex laterals, palatal nasals, and diphthongs used in literary Kannada.",
        "tags": ["kannada", "seed", "lang:kn"],
        "stress": [
            "Stress is syllable-timed; macro volume keeps vowel reductions audible.",
            "Questions raise intonation on sentence-final vowels; inflection slider ensures clarity."
        ],
        "sentence": [
            "Subject–Object–Verb with extensive postpositions; smoothness avoids merging sandhi outcomes.",
            "Verb auxiliaries stack at the end; emphasis keeps sequential consonants articulate."
        ],
        "grammar": [
            "Retroflex lateral ಳ and palatal nasal ಞ require scope depth and subtone boost.",
            "Diphthong sign ೈ needs tone slider assistance for gliding vowels."
        ],
        "template_id": "eloquence-seed-kn-in",
        "template_name": "Eloquence seed – Kannada",
        "template_description": "Placeholder Kannada tuning for palatal nasals and retroflex laterals.",
        "template_tags": ["eloquence", "seed", "kannada"],
        "template_variant": "3",
        "template_gender": 0,
        "script": "kannada",
        "param_overrides": {"rate": 100, "pitch": 116, "inflection": 60},
        "advanced_overrides": {"scopeDepth": 118, "subtones": 114, "tone": 108}
    },
    {
        "id": "mr-in-seed",
        "language": "mr",
        "display": "Marathi – syllabic liquids",
        "description": "Marathi placeholder focusing on syllabic /r̩/, retroflex laterals, and complex consonant conjuncts.",
        "tags": ["marathi", "seed", "lang:mr"],
        "stress": [
            "Stress usually falls on the first syllable; macro volume needs to preserve trailing vowels.",
            "Questions raise pitch at the end; inflection slider handles the climb."
        ],
        "sentence": [
            "Subject–Object–Verb order with enclitic pronouns; smoothness keeps bound forms distinct.",
            "Participles modify nouns; emphasis ensures conjuncts like ज्ञ remain legible."
        ],
        "grammar": [
            "Retroflex lateral ळ and syllabic ऋ demand scope depth and subtone support.",
            "Conjunct ज्ञ requires smoothness to avoid merging with ज."
        ],
        "template_id": "eloquence-seed-mr-in",
        "template_name": "Eloquence seed – Marathi",
        "template_description": "Placeholder Marathi timbre balancing syllabic liquids and retroflex articulations.",
        "template_tags": ["eloquence", "seed", "marathi"],
        "template_variant": "2",
        "template_gender": 1,
        "script": "marathi",
        "param_overrides": {"rate": 100, "pitch": 118, "inflection": 64},
        "advanced_overrides": {"scopeDepth": 118, "subtones": 116}
    },
    {
        "id": "gu-in-seed",
        "language": "gu",
        "display": "Gujarati – vocalic resonances",
        "description": "Gujarati placeholder emphasising retroflex laterals, palatal nasals, and vocalic r vowels.",
        "tags": ["gujarati", "seed", "lang:gu"],
        "stress": [
            "Stress tends to penultimate syllables; macro volume prevents final vowels from disappearing.",
            "Questions add rising contour; inflection slider should adapt quickly."
        ],
        "sentence": [
            "Subject–Object–Verb with enclitic particles; smoothness ensures joined vowels remain intelligible.",
            "Reduplicated adjectives require emphasis to avoid monotony."
        ],
        "grammar": [
            "Vocalic r (ૃ) needs subtones to stay resonant.",
            "Retroflex lateral ળ requires scope depth to contrast with લ."
        ],
        "template_id": "eloquence-seed-gu-in",
        "template_name": "Eloquence seed – Gujarati",
        "template_description": "Placeholder Gujarati timbre focusing on retroflex laterals and vocalic r vowels.",
        "template_tags": ["eloquence", "seed", "gujarati"],
        "template_variant": "3",
        "template_gender": 0,
        "script": "gujarati",
        "param_overrides": {"rate": 102, "pitch": 120, "inflection": 62},
        "advanced_overrides": {"scopeDepth": 116, "subtones": 116}
    },
    {
        "id": "pa-in-seed",
        "language": "pa",
        "display": "Punjabi – tonal Gurmukhi",
        "description": "Punjabi placeholder aligning retroflex flaps, nasalisation, and tonal contrasts in Gurmukhi.",
        "tags": ["punjabi", "seed", "lang:pa"],
        "stress": [
            "Tone variations (high-falling, low-rising) require responsive tone sliders.",
            "Boliyan call-and-response uses macro volume to highlight question-response cadence."
        ],
        "sentence": [
            "Subject–Object–Verb with postpositions; smoothness maintains enclitic pronoun clarity.",
            "Relative clauses often omit copulas; emphasis ensures tonal cues remain."
        ],
        "grammar": [
            "Retroflex flap ੜ needs scope depth to avoid merging with ਡ.",
            "Bindī nasal marker demands subtone support for vowel nasalisation."
        ],
        "template_id": "eloquence-seed-pa-in",
        "template_name": "Eloquence seed – Punjabi",
        "template_description": "Placeholder Punjabi timbre tuned for tonal Gurmukhi and nasal vowels.",
        "template_tags": ["eloquence", "seed", "punjabi"],
        "template_variant": "2",
        "template_gender": 0,
        "script": "gurmukhi",
        "param_overrides": {"rate": 104, "pitch": 126, "inflection": 70},
        "advanced_overrides": {"tone": 132, "subtones": 118, "scopeDepth": 118}
    },
    {
        "id": "si-lk-seed",
        "language": "si",
        "display": "Sinhala – rounded cadence",
        "description": "Sinhala placeholder emphasising prenasalised stops, palatal nasals, and loan fricatives.",
        "tags": ["sinhala", "seed", "lang:si"],
        "stress": [
            "Stress is weak and tends toward the penultimate syllable; macro volume retains vowel resonance.",
            "Tone is absent but pitch rises on interrogatives; inflection slider handles the rise." 
        ],
        "sentence": [
            "Subject–Object–Verb with postpositions; smoothness prevents nasal-stop clusters from clicking.",
            "Loanword fricatives require overtones to remain distinct."
        ],
        "grammar": [
            "Pranasalised stops (ඟ) need smoothness to keep the nasal lead-in.",
            "Loan fricative ෆ requires overtone support to stand out."
        ],
        "template_id": "eloquence-seed-si-lk",
        "template_name": "Eloquence seed – Sinhala",
        "template_description": "Placeholder Sinhala timbre balancing prenasalised clusters with borrowed fricatives.",
        "template_tags": ["eloquence", "seed", "sinhala"],
        "template_variant": "3",
        "template_gender": 1,
        "script": "sinhala",
        "param_overrides": {"rate": 96, "pitch": 118, "inflection": 58},
        "advanced_overrides": {"smoothness": 118, "overtones": 116, "subtones": 114}
    },
    {
        "id": "km-kh-seed",
        "language": "km",
        "display": "Khmer – diphthong radiance",
        "description": "Khmer placeholder capturing palatal nasals, aspirated affricates, and complex vowel nuclei.",
        "tags": ["khmer", "seed", "lang:km"],
        "stress": [
            "Khmer lacks lexical tone; macro volume maintains contrast between reduced and full vowels.",
            "Sentence-final particles soften pitch; inflection slider assists subtle fall."
        ],
        "sentence": [
            "Verb serialization and aspect markers change rhythm; smoothness keeps stacked consonants legible.",
            "Dependent vowels shift quality by context; tone size slider should track glides."
        ],
        "grammar": [
            "Palatal nasal ញ requires smooth onset; aspirated affricate ឆ needs emphasis for aspiration.",
            "Diphthong sign ើ/ួ demands tone-size control to avoid monotone delivery."
        ],
        "template_id": "eloquence-seed-km-kh",
        "template_name": "Eloquence seed – Khmer",
        "template_description": "Placeholder Khmer timbre tuned for aspirated affricates and glide-heavy vowels.",
        "template_tags": ["eloquence", "seed", "khmer"],
        "template_variant": "1",
        "template_gender": 0,
        "script": "khmer",
        "param_overrides": {"rate": 110, "pitch": 120, "inflection": 62},
        "advanced_overrides": {"smoothness": 118, "toneSize": 112, "emphasis": 112}
    },
    {
        "id": "my-mm-seed",
        "language": "my",
        "display": "Burmese – creaky tone balance",
        "description": "Burmese placeholder highlighting creaky vs modal tone, aspiration markers, and vowel colouring.",
        "tags": ["burmese", "seed", "lang:my"],
        "stress": [
            "Tone quality (creaky, high, low) is key; tone slider needs to range across phonation types.",
            "Particles such as မ require final pitch drop handled by inflection contour."
        ],
        "sentence": [
            "Verb-final particles express modality; macro volume keeps them audible after long vowels.",
            "Reduplication and compounding require smoothness to avoid glottal clicks." 
        ],
        "grammar": [
            "Nasal finals -င် require subtone boosts; aspiration diacritic needs whisper to add breathiness.",
            "Diphthong ို needs tone slider management for rising contour."
        ],
        "template_id": "eloquence-seed-my-mm",
        "template_name": "Eloquence seed – Burmese",
        "template_description": "Placeholder Burmese timbre balancing creaky tones, aspiration, and nasal finals.",
        "template_tags": ["eloquence", "seed", "burmese"],
        "template_variant": "2",
        "template_gender": 1,
        "script": "burmese",
        "param_overrides": {"rate": 104, "pitch": 122, "inflection": 76},
        "advanced_overrides": {"tone": 132, "toneSize": 120, "whisper": 116}
    },
    {
        "id": "lo-la-seed",
        "language": "lo",
        "display": "Lao – tone class guidance",
        "description": "Lao placeholder emphasising silent-h tone class markers, diphthongs, and vowel carriers.",
        "tags": ["lao", "seed", "lang:lo"],
        "stress": [
            "Tone classes dictate contour; tone slider must respond to high/low class shifts.",
            "Glottal carriers demand macro volume to stay audible at phrase edges."
        ],
        "sentence": [
            "Subject–Verb–Object with topic fronting; smoothness keeps vowel sequences stable.",
            "Classifier phrases require emphasis to highlight tone patterns."
        ],
        "grammar": [
            "Silent h prefix modifies tone; inflection slider should adapt accordingly.",
            "Glottal carrier ອ ensures initial vowel; macro volume prevents drop-out."
        ],
        "template_id": "eloquence-seed-lo-la",
        "template_name": "Eloquence seed – Lao",
        "template_description": "Placeholder Lao timbre tuned for tone-class prefixes and vowel carriers.",
        "template_tags": ["eloquence", "seed", "lao"],
        "template_variant": "1",
        "template_gender": 0,
        "script": "lao",
        "param_overrides": {"rate": 110, "pitch": 126, "inflection": 82},
        "advanced_overrides": {"tone": 136, "toneSize": 122, "macroVolume": 110}
    },
    {
        "id": "ne-np-seed",
        "language": "ne",
        "display": "Nepali – Himalayan cadence",
        "description": "Nepali placeholder emphasising aspirated affricates, velar nasals, and consonant clusters with /r/.",
        "tags": ["nepali", "seed", "lang:ne"],
        "stress": [
            "Stress falls on the penultimate syllable; macro volume keeps final vowels audible.",
            "Questions raise contour at the end; inflection slider supports the rise."
        ],
        "sentence": [
            "Subject–Object–Verb with extensive postpositions; smoothness prevents cluster smearing.",
            "Honorific forms lengthen vowels; scope depth needs to preserve the change."
        ],
        "grammar": [
            "Aspirated affricates छ /tʃʰ/ need emphasis to differentiate from unaspirated pairs.",
            "Clusters like श्र require smoothness to keep consonants distinct."
        ],
        "template_id": "eloquence-seed-ne-np",
        "template_name": "Eloquence seed – Nepali",
        "template_description": "Placeholder Nepali timbre tuned for aspirated affricates and consonant clusters.",
        "template_tags": ["eloquence", "seed", "nepali"],
        "template_variant": "3",
        "template_gender": 1,
        "script": "nepali",
        "param_overrides": {"rate": 102, "pitch": 120, "inflection": 66},
        "advanced_overrides": {"emphasis": 120, "smoothness": 118, "subtones": 112}
    },
    {
        "id": "ru-ru-seed",
        "language": "ru",
        "display": "Russian – palatal richness",
        "description": "Russian placeholder tuned for palatalised consonants, retroflex fricatives, and reduced vowels.",
        "tags": ["russian", "seed", "lang:ru"],
        "stress": [
            "Stress is contrastive; macro volume keeps unstressed vowels from disappearing.",
            "Questions raise pitch on the final syllable; inflection slider follows the contour."
        ],
        "sentence": [
            "Flexible word order with stress-driven focus; smoothness ensures consonant clusters stay distinct.",
            "Aspect pairs require emphasis on prefixes to mark perfective/imperfective contrasts."
        ],
        "grammar": [
            "Palatalised consonants need overtones to highlight the [j] offglide.",
            "Retroflex fricative ж benefits from subtone support to avoid muddiness."
        ],
        "template_id": "eloquence-seed-ru-ru",
        "template_name": "Eloquence seed – Russian",
        "template_description": "Placeholder Russian timbre balancing palatalisation and retroflex frication.",
        "template_tags": ["eloquence", "seed", "russian"],
        "template_variant": "1",
        "template_gender": 0,
        "script": "cyrillic_ru",
        "param_overrides": {"rate": 104, "pitch": 118, "inflection": 58},
        "advanced_overrides": {"overtones": 118, "subtones": 110, "smoothness": 112}
    },
    {
        "id": "uk-ua-seed",
        "language": "uk",
        "display": "Ukrainian – bright palatals",
        "description": "Ukrainian placeholder focusing on palatalised consonants, /ɦ/ vs /g/, and melodic intonation.",
        "tags": ["ukrainian", "seed", "lang:uk"],
        "stress": [
            "Stress varies lexically; macro volume preserves vowel quality across unstressed syllables.",
            "Questions have rising-falling melody; inflection slider should handle the contour."
        ],
        "sentence": [
            "Subject–Verb–Object dominates; smoothness preserves vowel sequences in open syllables.",
            "Aspectual prefixes require emphasis to differentiate motion verbs."
        ],
        "grammar": [
            "Distinct letters ї and є need smooth glides; ґ must remain a true /g/ via emphasis.",
            "Palatalisation requires overtones without excessive hiss."
        ],
        "template_id": "eloquence-seed-uk-ua",
        "template_name": "Eloquence seed – Ukrainian",
        "template_description": "Placeholder Ukrainian timbre balancing melodic intonation with palatal consonants.",
        "template_tags": ["eloquence", "seed", "ukrainian"],
        "template_variant": "2",
        "template_gender": 1,
        "script": "cyrillic_uk",
        "param_overrides": {"rate": 106, "pitch": 122, "inflection": 62},
        "advanced_overrides": {"tone": 112, "overtones": 120, "smoothness": 118}
    },
    {
        "id": "pl-pl-seed",
        "language": "pl",
        "display": "Polish – sibilant contrast",
        "description": "Polish placeholder emphasising alveolo-palatal vs retroflex sibilants and dark ł vowels.",
        "tags": ["polish", "seed", "lang:pl"],
        "stress": [
            "Stress typically lands on the penultimate syllable; macro volume must protect final vowels.",
            "Questions increase pitch near the end; inflection slider handles the lift."
        ],
        "sentence": [
            "Subject–Verb–Object order; smoothness prevents consonant clusters from blending.",
            "Perfective/imperfective aspect prefixes require emphasis for clarity."
        ],
        "grammar": [
            "Soft sibilants ś/ź need overtone tweaks to avoid merging with hard counterparts.",
            "Dark ł (w) requires subtone emphasis to keep timbre warm."
        ],
        "template_id": "eloquence-seed-pl-pl",
        "template_name": "Eloquence seed – Polish",
        "template_description": "Placeholder Polish timbre tuned for soft vs hard sibilants and dark ł.",
        "template_tags": ["eloquence", "seed", "polish"],
        "template_variant": "3",
        "template_gender": 0,
        "script": "latin_pl",
        "param_overrides": {"rate": 108, "pitch": 118, "inflection": 60},
        "advanced_overrides": {"overtones": 120, "subtones": 108, "emphasis": 118}
    },
    {
        "id": "cs-cz-seed",
        "language": "cs",
        "display": "Czech – trill precision",
        "description": "Czech placeholder emphasising the ř trill, velar fricative ch, and palatal nasals.",
        "tags": ["czech", "seed", "lang:cs"],
        "stress": [
            "Stress falls on the first syllable; macro volume prevents trailing vowels from dropping.",
            "Questions raise pitch on the final syllable; inflection slider ensures smooth rise."
        ],
        "sentence": [
            "Subject–Verb–Object with frequent clitic stacking; smoothness keeps clitics audible.",
            "Aspectual pairs rely on prefixes; emphasis should highlight them."
        ],
        "grammar": [
            "Ř trill requires scope depth to avoid harshness.",
            "Voiceless velar fricative ch needs whisper to stay airy."
        ],
        "template_id": "eloquence-seed-cs-cz",
        "template_name": "Eloquence seed – Czech",
        "template_description": "Placeholder Czech timbre balancing ř trills and velar fricatives.",
        "template_tags": ["eloquence", "seed", "czech"],
        "template_variant": "1",
        "template_gender": 0,
        "script": "latin_cs",
        "param_overrides": {"rate": 106, "pitch": 118, "inflection": 58},
        "advanced_overrides": {"scopeDepth": 122, "whisper": 112, "smoothness": 118}
    },
    {
        "id": "tr-tr-seed",
        "language": "tr",
        "display": "Turkish – vowel harmony",
        "description": "Turkish placeholder emphasising vowel harmony, soft g, and postalveolar fricatives.",
        "tags": ["turkish", "seed", "lang:tr"],
        "stress": [
            "Stress usually falls on the final syllable; macro volume keeps suffix vowels clear.",
            "Yes/no questions add rising intonation; inflection slider should adapt."
        ],
        "sentence": [
            "Subject–Object–Verb with agglutinative suffixes; smoothness maintains harmony across endings.",
            "Question particle mi requires emphasis to stand out between suffixes."
        ],
        "grammar": [
            "Soft g ğ lengthens vowels; scope depth ensures gentle lengthening.",
            "Ş and ç need overtone support to stay sharp without harshness."
        ],
        "template_id": "eloquence-seed-tr-tr",
        "template_name": "Eloquence seed – Turkish",
        "template_description": "Placeholder Turkish timbre balancing vowel harmony with soft-g vowel lengthening.",
        "template_tags": ["eloquence", "seed", "turkish"],
        "template_variant": "2",
        "template_gender": 0,
        "script": "latin_tr",
        "param_overrides": {"rate": 108, "pitch": 120, "inflection": 62},
        "advanced_overrides": {"smoothness": 120, "tone": 110, "scopeDepth": 112}
    },
    {
        "id": "el-gr-seed",
        "language": "el",
        "display": "Greek – consonant balance",
        "description": "Greek placeholder emphasising dental fricatives, velar fricatives, and consonant clusters.",
        "tags": ["greek", "seed", "lang:el"],
        "stress": [
            "Stress is contrastive and indicated orthographically; macro volume protects unstressed vowels.",
            "Questions raise pitch mid-word; inflection slider supports the rise."
        ],
        "sentence": [
            "Subject–Verb–Object common; smoothness ensures consonant clusters remain intelligible.",
            "Clitics attach to verbs; emphasis should keep them audible."
        ],
        "grammar": [
            "Dental fricatives θ/ð require emphasis to maintain clarity.",
            "Velar fricative γ needs smoothness to avoid roughness."
        ],
        "template_id": "eloquence-seed-el-gr",
        "template_name": "Eloquence seed – Greek",
        "template_description": "Placeholder Greek timbre balancing dental and velar fricatives with smooth clusters.",
        "template_tags": ["eloquence", "seed", "greek"],
        "template_variant": "1",
        "template_gender": 1,
        "script": "greek",
        "param_overrides": {"rate": 104, "pitch": 118, "inflection": 60},
        "advanced_overrides": {"emphasis": 118, "smoothness": 116, "tone": 108}
    },
    {
        "id": "nl-nl-seed",
        "language": "nl",
        "display": "Dutch – diphthong clarity",
        "description": "Dutch placeholder focusing on diphthongs IJ/UI and the sch/gt fricative cluster.",
        "tags": ["dutch", "seed", "lang:nl"],
        "stress": [
            "Stress often penultimate but lexical; macro volume keeps reduced vowels audible.",
            "Questions raise pitch on the final diphthong; inflection slider emphasises the glide."
        ],
        "sentence": [
            "Subject–Verb–Object with V2 inversion; smoothness ensures clitic pronouns remain distinct.",
            "Modal particles like toch adjust tone; emphasis clarifies them."
        ],
        "grammar": [
            "IJ and UI diphthongs need tone-size support to remain bright.",
            "sch cluster requires whisper plus overtones to avoid harshness."
        ],
        "template_id": "eloquence-seed-nl-nl",
        "template_name": "Eloquence seed – Dutch",
        "template_description": "Placeholder Dutch timbre balancing bright diphthongs with velar fricatives.",
        "template_tags": ["eloquence", "seed", "dutch"],
        "template_variant": "2",
        "template_gender": 0,
        "script": "latin_nl",
        "param_overrides": {"rate": 110, "pitch": 116, "inflection": 56},
        "advanced_overrides": {"smoothness": 114, "toneSize": 112, "whisper": 110}
    },
    {
        "id": "sv-se-seed",
        "language": "sv",
        "display": "Swedish – pitch accent",
        "description": "Swedish placeholder emphasising sj/tj fricatives and tonal accent pairs.",
        "tags": ["swedish", "seed", "lang:sv"],
        "stress": [
            "Primary stress often on the first syllable with tonal accent 1 vs 2; tone slider handles pitch patterns.",
            "Questions rise late in the phrase; inflection slider adds the uplift."
        ],
        "sentence": [
            "Verb-second order; smoothness keeps clitic pronouns audible after verbs.",
            "Compound nouns require emphasis to highlight primary vs secondary stress."
        ],
        "grammar": [
            "Sj-sound /ɧ/ needs overtone balancing to avoid white noise.",
            "Tj /ɕ/ should stay bright but not piercing; tone slider helps."
        ],
        "template_id": "eloquence-seed-sv-se",
        "template_name": "Eloquence seed – Swedish",
        "template_description": "Placeholder Swedish timbre tuned for sj/tj fricatives and tonal accents.",
        "template_tags": ["eloquence", "seed", "swedish"],
        "template_variant": "3",
        "template_gender": 1,
        "script": "latin_sv",
        "param_overrides": {"rate": 108, "pitch": 124, "inflection": 64},
        "advanced_overrides": {"tone": 128, "toneSize": 120, "overtones": 118}
    },
    {
        "id": "nb-no-seed",
        "language": "nb",
        "display": "Norwegian (Bokmål) – tonal balance",
        "description": "Norwegian placeholder capturing palatal kj, retroflex skj, and pitch accent pairs.",
        "tags": ["norwegian", "seed", "lang:nb"],
        "stress": [
            "Pitch accents differentiate word pairs; tone slider must follow accent 1 vs 2.",
            "Questions rise at the end; inflection slider should raise final syllables."
        ],
        "sentence": [
            "Verb-second word order; smoothness ensures clitics remain audible.",
            "Modal particles like vel and jo adjust tone; emphasis clarifies them."
        ],
        "grammar": [
            "Palatal kj /ç/ requires tone smoothing to avoid hiss.",
            "Retroflex skj /ʂ/ needs overtones for clarity."
        ],
        "template_id": "eloquence-seed-nb-no",
        "template_name": "Eloquence seed – Norwegian",
        "template_description": "Placeholder Norwegian timbre tuned for kj/skj fricatives and pitch accents.",
        "template_tags": ["eloquence", "seed", "norwegian"],
        "template_variant": "1",
        "template_gender": 0,
        "script": "latin_nb",
        "param_overrides": {"rate": 104, "pitch": 122, "inflection": 62},
        "advanced_overrides": {"tone": 126, "overtones": 116, "smoothness": 118}
    },
    {
        "id": "da-dk-seed",
        "language": "da",
        "display": "Danish – stød scaffolding",
        "description": "Danish placeholder highlighting stød, uvular r, and vowel reductions.",
        "tags": ["danish", "seed", "lang:da"],
        "stress": [
            "Stress usually on first syllable but stød adds creaky phonation; tone slider must represent it.",
            "Questions raise pitch near the end; inflection slider handles the rise."
        ],
        "sentence": [
            "Verb-second order; smoothness keeps clitic pronouns audible despite reductions.",
            "Stød-bearing syllables need macro volume to highlight creaky voice."
        ],
        "grammar": [
            "Uvular r /ʁ/ requires subtone support to stay warm.",
            "Affricate dg in loans should maintain crispness via emphasis."
        ],
        "template_id": "eloquence-seed-da-dk",
        "template_name": "Eloquence seed – Danish",
        "template_description": "Placeholder Danish timbre tuned for stød and uvular r.",
        "template_tags": ["eloquence", "seed", "danish"],
        "template_variant": "2",
        "template_gender": 1,
        "script": "latin_da",
        "param_overrides": {"rate": 102, "pitch": 118, "inflection": 60},
        "advanced_overrides": {"tone": 120, "subtones": 110, "whisper": 112}
    },
    {
        "id": "fi-fi-seed",
        "language": "fi",
        "display": "Finnish – vowel length discipline",
        "description": "Finnish placeholder covering vowel length contrasts, front rounded vowels, and velar nasals.",
        "tags": ["finnish", "seed", "lang:fi"],
        "stress": [
            "Stress on the first syllable; macro volume ensures length differences stay audible.",
            "Questions raise pitch at the end; inflection slider adds the lift."
        ],
        "sentence": [
            "Subject–Verb–Object with rich case endings; smoothness keeps suffix vowels crisp.",
            "Consonant gradation changes stops; emphasis must highlight alternations."
        ],
        "grammar": [
            "Front rounded vowel y needs tone slider to maintain brightness.",
            "Open front vowel ä requires subtone support to remain warm."
        ],
        "template_id": "eloquence-seed-fi-fi",
        "template_name": "Eloquence seed – Finnish",
        "template_description": "Placeholder Finnish timbre tuned for vowel length and front rounded vowels.",
        "template_tags": ["eloquence", "seed", "finnish"],
        "template_variant": "3",
        "template_gender": 0,
        "script": "latin_fi",
        "param_overrides": {"rate": 100, "pitch": 118, "inflection": 56},
        "advanced_overrides": {"tone": 112, "subtones": 116, "smoothness": 120}
    },
]

BASE_TEMPLATE_PARAMETERS = {
    "rate": 100,
    "pitch": 112,
    "inflection": 60,
    "headSize": 110,
    "roughness": 20,
    "breathiness": 22,
    "volume": 92,
}

VOICE_OUTPUT_FILE = str(resource_paths.voice_seed_output_path())


def _ensure_repo_on_path() -> None:
    import sys

    if REPO_ROOT not in sys.path:
        sys.path.insert(0, REPO_ROOT)


_ensure_repo_on_path()

from voice_parameters import ADVANCED_VOICE_PARAMETER_SPECS  # noqa: E402

ADVANCED_DEFAULTS = {name: int(spec.get("default", 100)) for name, spec in ADVANCED_VOICE_PARAMETER_SPECS.items()}


def build_language_profiles() -> List[Dict[str, object]]:
    profiles: List[Dict[str, object]] = []
    for spec in LANGUAGE_SPECS:
        script_key = spec["script"]
        samples = deepcopy(SCRIPT_SAMPLES.get(script_key, ()))
        if not samples:
            continue
        profile = {
            "id": spec["id"],
            "language": spec["language"],
            "displayName": spec["display"],
            "description": spec["description"],
            "tags": spec["tags"],
            "stress": spec["stress"],
            "sentenceStructure": spec["sentence"],
            "grammar": spec["grammar"],
            "defaultVoiceTemplates": [spec["template_id"]],
            "characters": samples,
        }
        profiles.append(profile)
    return profiles


def build_voice_templates() -> List[Dict[str, object]]:
    templates: List[Dict[str, object]] = []
    for spec in LANGUAGE_SPECS:
        params = dict(BASE_TEMPLATE_PARAMETERS)
        params.update(spec.get("param_overrides", {}))
        params["gender"] = spec["template_gender"]
        for adv_name, default in ADVANCED_DEFAULTS.items():
            params[adv_name] = spec.get("advanced_overrides", {}).get(adv_name, default)
        template = {
            "id": spec["template_id"],
            "name": spec["template_name"],
            "language": spec["language"],
            "description": spec["template_description"],
            "tags": spec["template_tags"],
            "baseVoice": "enu",
            "variant": spec["template_variant"],
            "defaultLanguageProfile": spec["id"],
            "sourceVoice": "Seed placeholder",
            "parameters": params,
            "extras": {
                "phonemeFallback": "ipaFirst",
                "notes": [
                    "Seed template awaiting community tuning for regional authenticity.",
                    "Advanced sliders stay at documented defaults unless overrides are provided.",
                ],
            },
        }
        templates.append(template)
    return templates


def _write_json(path: str, payload: dict[str, object]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def main() -> None:
    from datetime import datetime, timezone

    profiles = build_language_profiles()
    templates = build_voice_templates()
    profile_payload = {"profiles": profiles}
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    voice_payload = {
        "metadata": {
            "source": "Seeded placeholder templates for global language coverage",
            "generated": timestamp,
            "notes": [
                "Templates provide neutral slider baselines so phoneme customizer work can begin immediately.",
                "Community contributors are encouraged to replace these placeholders with recordings and tuned parameters.",
            ],
        },
        "templates": templates,
    }
    _write_json(OUTPUT_FILE, profile_payload)
    _write_json(VOICE_OUTPUT_FILE, voice_payload)
    print(f"Wrote {len(profiles)} language profiles to {OUTPUT_FILE}")
    print(f"Wrote {len(templates)} voice templates to {VOICE_OUTPUT_FILE}")


if __name__ == "__main__":
    main()
