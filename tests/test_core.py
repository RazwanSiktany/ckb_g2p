import pytest
from ckb_g2p import Converter

# Initialize converter
converter = Converter(use_stress=False, use_pause_markers=True, normalize=False)

TEST_CASES = [
    ("چێوار", "t̪͡ʃ̟ɛ.wäɾ"),
    ("کێوار", "t͡ʃɛ.wäɾ"),
    ("جیران", "d̪͡ʒ̟iː.ɾän"),
    ("گیران", "d͡ʒiː.ɾän"),
    ("مامم", "mä.mɪm"),
    ("گرفت", "gɪ.ɾɪft"),
    ("گرتن", "gɪɾ.tɪn"),
    ("بووین", "buːjn"),
    ("ووشە", "wu.ʃa"),
    ("چیو", "t̪͡ʃ̟iːw"),
]


@pytest.mark.parametrize("text, expected", TEST_CASES)
def test_phonemes(text, expected):
    assert converter.syllabify(text) == expected


def test_stress():
    c = Converter(use_stress=True)
    assert c.syllabify("کوردستان") == "kuɾ.dɪs.ˈtän"

    # Negative verb test (Fixed expectation to match Light Ch logic)
    # 'چ' = t̪͡ʃ̟ (Light)
    assert c.syllabify("نەچوو") == "ˈna.t̪͡ʃ̟uː"


def test_pauses():
    c = Converter(use_pause_markers=True)
    assert c.syllabify("سڵاو,") == "sɪ.ɫäw |"