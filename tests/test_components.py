import pytest
from ckb_g2p.core.grapheme_parser import GraphemeParser
from ckb_g2p.core.generator import Generator
from ckb_g2p.core.evaluator import Evaluator
from ckb_g2p.core.syllabifier import Syllabifier


def test_parser_greedy_matching():
    """Test if the Trie grabs the longest match ('وو' vs 'و')."""
    parser = GraphemeParser()
    # "دوو" -> d + uː (not d + w + w)
    tokens = parser.tokenize("دوو")
    assert tokens == ['d', 'uː']


def test_generator_ambiguity():
    """Test if Generator creates 'w' and 'u' options for 'و'."""
    gen = Generator()
    # 'kwrd' -> [('k', 'w', 'r', 'd'), ('k', 'u', 'r', 'd')]
    candidates = gen.generate_candidates(['k', 'w', 'ɾ', 'd'])
    assert len(candidates) >= 2
    assert ('k', 'u', 'ɾ', 'd') in candidates


def test_evaluator_vowel_preference():
    """Test if Evaluator picks 'kurd' over 'kwrd'."""
    evaluator = Evaluator()
    # kwrd (no vowel) vs kurd (vowel)
    bad = ('k', 'w', 'ɾ', 'd')
    good = ('k', 'u', 'ɾ', 'd')

    score_bad = evaluator.calculate_penalty(bad)
    score_good = evaluator.calculate_penalty(good)

    assert score_good < score_bad


def test_syllabifier_stress():
    """Test Stress Logic."""
    syllabifier = Syllabifier()

    # 1. Normal Final Stress
    # kur.di -> kur.ˈdi
    res_normal = syllabifier.syllabify(['k', 'u', 'ɾ', 'd', 'iː'])
    assert res_normal == "kuɾ.ˈdiː"

    # 2. Negative Verb Initial Stress
    # ne.chu -> ˈne.chu
    res_negative = syllabifier.syllabify(['n', 'a', 't̪͡ʃ̟', 'uː'])
    assert res_negative == "ˈna.t̪͡ʃ̟uː"