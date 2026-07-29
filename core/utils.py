ARABIC_INDIC_DIGITS = '٠١٢٣٤٥٦٧٨٩'
EXTENDED_ARABIC_INDIC_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
WESTERN_DIGITS = '0123456789'

_DIGIT_TRANSLATION = str.maketrans(
    ARABIC_INDIC_DIGITS + EXTENDED_ARABIC_INDIC_DIGITS,
    WESTERN_DIGITS * 2,
)


def normalize_digits(value):
    """Convert Arabic/Persian numerals to Western digits."""
    return str(value).translate(_DIGIT_TRANSLATION).strip()
