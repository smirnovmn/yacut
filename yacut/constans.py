from wtforms.validators import Length

ORIGINAL_LINK_RANGE = Length(1, 256)
ORIGINAL_LINK_MAX_LENGTH = 256
CUSTOM_ID_RANGE = Length(1, 128)
SHORT_LINK_MAX_LENGTH = 128
LENGTH_SHORT_LINK = 6
#В ТЗ говорится про 6 символов поэтому 6...
