import pytest
from ckb_g2p import Converter

converter = Converter(use_stress=False, use_pause_markers=True, normalize=False)

TEST_CASES = [
    ("چێوار", "t̪͡ʃ̟ɛ.wäɾ"),
    ("کێوار", "t͡ʃɛ.wäɾ"),
    ("نەچوو", "na.t̪͡ʃ̟uː"), # Light Ch check
]

@pytest.mark.parametrize("text, expected", TEST_CASES)
def test_phonemes(text, expected):
    assert converter.syllabify(text) == expected

def test_stress():
    c = Converter(use_stress=True)
    assert c.syllabify("نەچوو") == "ˈna.t̪͡ʃ̟uː"
