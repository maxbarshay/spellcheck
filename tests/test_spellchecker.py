from spellcheck.spellchecker import SpellChecker

spellchecker = SpellChecker(2)

text = "To iscape his tarrible flailing, I siezzed hold of my polee stikcing in him."
fixedup_text = spellchecker.fixup_text(text)

print(f"\nRaw Text:\n{text}")
print(f"Fixedup Text:\n{fixedup_text}")
corrected_text, corrected_words = spellchecker.correct_text_test(fixedup_text)
print(f"\nSpellchecked Text:\n{corrected_text}\n\nCorrected Words:\n{corrected_words}")