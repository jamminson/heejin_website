import re

text = "   This is a   string with   spaces.   "
text_without_spaces = re.sub(r"\s+", "", text)
print(text_without_spaces)
