class Palatalizer:
    """
    Handles the phonological process of Palatalization.
    Converts /k/ -> /t͡ʃ/ and /g/ -> /d͡ʒ/ when followed by front vowels.
    Implements the "Harmony Blocking" rule for chains of candidates.
    """

    def __init__(self):
        # Triggers: Front vowels that cause the change
        # iː (î), ɛ (ê), j (y)
        self.front_vowels = {'iː', 'ɛ', 'j'}

        # Transparent chars: These don't stop the "chain" check
        # (Based on your original code's logic)
        self.transparent = {'iː', 'ɛ', 'j', 'w', 'v', 'uː'}

    def apply(self, phonemes: tuple) -> tuple:
        if not phonemes:
            return tuple()

        plist = list(phonemes)
        n = len(plist)
        candidates = []

        # 1. Identify Candidates
        for i, p in enumerate(plist):
            if p in ['k', 'g']:
                is_candidate = False

                # Rule A: Direct Front Vowel (e.g., 'k' + 'ê')
                if i + 1 < n and plist[i + 1] in self.front_vowels:
                    is_candidate = True

                # Rule B: Glide 'w' + Front Vowel (e.g., 'kwê' -> 'chwê')
                # This matches your old project's check for 'وێ'
                elif i + 2 < n and plist[i + 1] == 'w' and plist[i + 2] in self.front_vowels:
                    is_candidate = True

                if is_candidate:
                    candidates.append(i)

        # 2. Apply Blocking Rule (Harmony)
        # If two candidates are separated ONLY by transparent characters,
        # the first one is "blocked" (remains hard).
        blocked_indices = set()

        if len(candidates) > 1:
            for k in range(len(candidates) - 1):
                idx1 = candidates[k]
                idx2 = candidates[k + 1]

                # Check what is between them
                between_slice = plist[idx1 + 1: idx2]

                # If everything between is transparent, blocking occurs
                is_chain = all(x in self.transparent for x in between_slice)

                if is_chain:
                    blocked_indices.add(idx1)

        # 3. Transform
        for i in candidates:
            if i in blocked_indices:
                continue  # Skip blocked ones

            # Apply transformation
            if plist[i] == 'k':
                plist[i] = 't͡ʃ'  # Heavy Ch
            elif plist[i] == 'g':
                plist[i] = 'd͡ʒ'  # Heavy J

        return tuple(plist)