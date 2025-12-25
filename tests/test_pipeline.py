import pytest

# --- Test Data ---
# Format: (Input Word, Expected Syllabified Output)
LINGUISTIC_CASES = [
    # --- 1. Basic Vocabulary & Vowels ---
    ("کورد", "ˈkuɾd"),  # u (Short u) preferred over w
    ("دوو", "ˈduː"),  # uː (Long u) digraph
    ("ناو", "ˈnäw"),  # ä (a) + w (glide) = Diphthong
    ("سەر", "ˈsaɾ"),  # a (Schwa)
    ("شین", "ˈʃiːn"),  # iː (Long i)
    ("خۆر", "ˈxo̞ɾ"),  # o̞ (Short o)
    ("ئاو", "ˈʔäw"),  # Initial Glottal + ä + w
    ("باوک", "ˈbäwk"),  # w-k coda
    ("دایک", "ˈdäjk"),  # j-k coda
    ("کوڕ", "ˈkur"),  # r (Trill)
    ("پیاو", "ˈpjäw"),  # Cj Onset (py) preserved
    ("باران", "bä.ˈɾän"),  # Rain (r -> ɾ)
    ("ئاسمان", "ʔäs.ˈmän"),  # Sky (Final Stress)
    ("چاو", "ˈt̪͡ʃ̟äw"),  # Eye (Light Ch)
    ("دەنگ", "ˈdang"),  # Voice
    ("خوێ", "ˈxwɛ"),  # Salt (Cw onset)
    ("سەوز", "ˈsawz"),  # Green
    ("سوور", "ˈsuːɾ"),  # Red

    # --- 2. Palatalization (Standard & Glide Lookahead) ---
    ("کێو", "ˈt͡ʃɛw"),  # k -> t͡ʃ before ê (Standard)
    ("کێک", "ˈt͡ʃɛk"),  # First k -> t͡ʃ, Last k -> k
    ("گیان", "ˈd͡ʒjän"),  # g -> d͡ʒ before y (j)
    ("جەرگ", "ˈd̪͡ʒ̟aɾg"),  # Standard j (d̪͡ʒ̟) vs g (g)
    ("کوردی", "kuɾ.ˈdiː"),  # k remains k before u
    ("گۆڕان", "go̞.ˈrän"),  # g remains g before o
    ("بچووک", "bɪ.ˈt̪͡ʃ̟uːk"),  # ch (t̪͡ʃ̟) is standard

    # [NEW] Glide Lookahead Palatalization (The logic we just fixed)
    ("کوێ", "ˈt͡ʃwɛ"),  # k + w + ê -> ch
    ("گوێ", "ˈd͡ʒwɛ"),  # g + w + ê -> j
    ("کێ", "ˈt͡ʃɛ"),  # k + ê -> ch
    ("گێ", "ˈd͡ʒɛ"),  # g + ê -> j
    ("کی", "ˈt͡ʃiː"),  # k + î -> ch
    ("گی", "ˈd͡ʒiː"),  # g + î -> j

    # --- 3. Harmony Blocking Rule (Transparent Characters) ---
    ("گورگێکی", "guɾ.gɛ.ˈt͡ʃiː"),  # First G hard, K soft
    ("کێکێکی", "kɛ.kɛ.ˈt͡ʃiː"),  # First Ks hard, Last K soft

    # --- 4. Bizroka (Epenthesis) - Initial Clusters ---
    ("برد", "ˈbɪɾd"),  # br -> bɪr
    ("گرتن", "gɪɾ.ˈtɪn"),  # gr -> gɪr
    ("کتێب", "kɪ.ˈtɛb"),  # kt -> kɪt
    ("منداڵ", "ˈmɪn.däɫ"),  # mn -> mɪn
    ("ژن", "ˈʒɪn"),  # zh-n -> zhɪn
    ("برا", "bɪ.ˈɾä"),  # br -> bɪr
    ("سپین", "sɪ.ˈpiːn"),  # sp -> sɪp
    ("خستن", "xɪs.ˈtɪn"),  # xst -> xɪst

    # --- 5. Bizroka (Epenthesis) - Final Clusters ---
    ("کورد", "ˈkuɾd"),  # r(5) -> d(1): Falling (Valid)
    ("دەست", "ˈdast"),  # s(3) -> t(1): Falling (Valid)
    ("مانگ", "ˈmäng"),  # n(4) -> g(1): Falling (Valid)
    ("بەفر", "ba.ˈfɪɾ"),  # f(3) -> r(5): Rising (Invalid -> Insert ɪ)
    ("ئاگر", "ʔä.ˈgɪɾ"),  # g(1) -> r(5): Rising (Invalid -> Insert ɪ)
    ("مەغز", "ˈma.ɣɪz"),  # ɣ(3) -> z(3): Flat (Split prefered)
    ("سەقف", "sa.ˈqɪf"),  # q(1) -> f(3): Rising (Invalid -> Insert ɪ)

    # --- 6. Bizroka (Epenthesis) - Medial Clusters ---
    ("نیشتمان", "ˈniːʃt.män"),  # ʃt (Valid Coda)
    ("باڵندە", "bäɫn.ˈda"),  # l-n-d OK
    ("پێشمەرگە", "pɛʃ.maɾ.ˈga"),  # sh-m broken?

    # --- 7. Emphatics (Distinct Phonemes) ---
    ("صەد", "ˈsˤad"),  # Sad (sˤ) preserved
    ("تەط", "ˈtatˤ"),  # Ta (tˤ) preserved
    ("عەلی", "ʕa.ˈliː"),  # Ayn (ʕ) preserved
    ("غەریب", "ɣa.ˈɾiːb"),  # Ghayn (ɣ) preserved
    ("زوڵم", "ˈzuɫm"),  # ɫ (Dark l)

    # --- 8. Stress Rules ---
    ("کوردستان", "kuɾ.dɪs.ˈtän"),  # Normal -> Final Stress
    ("نەچوو", "ˈna.t̪͡ʃ̟uː"),  # Negative 'na' -> Initial Stress
    ("مەکە", "ˈma.ka"),  # Negative 'ma' -> Initial Stress
    ("نازانم", "ˈnä.zä.nɪm"),  # Negative 'na'
    ("مەڕۆ", "ˈma.ro̞"),  # Negative 'ma'

    # --- 9. Complex/Compound Words ---
    ("سلێمانی", "sɪ.lɛ.mä.ˈniː"),  # sl -> sɪl
    ("هەولێر", "haw.ˈlɛɾ"),  # haw-ler
    ("کەرکووک", "kaɾ.ˈkuːk"),  # kar-kuk
    ("دهۆک", "dɪ.ˈho̞k"),  # dh -> dɪh
    ("هەڵەبجە", "ha.ɫab.ˈd̪͡ʒ̟a"),  # Halabja
    ("نەورۆز", "ˈnaw.ɾo̞z"),  # Nawroz
    ("قوتابخانە", "qu.täb.xä.ˈna"),  # School
    ("ئازادی", "ʔä.zä.ˈdiː"),  # Freedom

    # --- 10. Syllable Structure & Onsets ---
    ("خوێندن", "xwɛn.ˈdɪn"),  # xw (Cw) is valid onset
    ("خوار", "ˈxwäɾ"),  # xw valid onset
    ("ژیان", "ˈʒjän"),  # Monosyllabic interpretation
    ("رووبار", "ɾuː.ˈbäɾ"),  # ruː-bar
    ("ئەستێرە", "ʔas.tɛ.ˈɾa"),  # as-te-ra
    ("مامۆستا", "ˈmä.mo̞s.tä"),  # ma-mos-ta
    ("بەیانی", "ba.jä.ˈniː"),  # Morning
    ("شەو", "ˈʃaw"),  # Night
    ("ڕۆژ", "ˈro̞ʒ"),  # Day
    ("خۆشەویستی", "xo̞.ʃa.wiːs.ˈtiː"),  # Love
    ("بەختیار", "bax.ˈtjäɾ"),  # Bakhtyar

    # --- 11. Additional Examples ---
    ("بەهار", "ba.ˈhäɾ"),  # Spring
    ("زستان", "zɪs.ˈtän"),  # Winter
    ("پاییز", "pä.ˈjiːz"),  # Autumn
    ("هاوین", "hä.ˈwiːn"),  # Summer
    ("شەممە", "ʃam.ˈma"),  # Saturday
    ("یەکشەممە", "jak.ʃam.ˈma"),  # Sunday
    ("ماڵ", "ˈmäɫ"),  # Home
    ("دەرگا", "daɾ.ˈgä"),  # Door
    ("پەنجەرە", "pan.d̪͡ʒ̟a.ˈɾa"),  # Window
    ("کورسی", "kuɾ.ˈsiː"),  # Chair
    ("مێز", "ˈmɛz"),  # Table
    ("قەڵەم", "qa.ˈɫam"),  # Pen
    ("دەفتەر", "daf.ˈtaɾ"),  # Notebook
]


@pytest.mark.parametrize("word, expected", LINGUISTIC_CASES)
def test_full_conversion(converter, word, expected):
    """
    Runs the full pipeline for a word and checks the final syllabified output.
    """
    # Convert to syllables
    result = converter.convert(word, output_format="syllables", normalize=False)

    # Check strict equality
    assert result[0] == expected