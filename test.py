import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

text = "This is a example text with some grammatically mistakes."
matches = tool.check(text)
corrected_text = tool.correct(text)

print("Original Text:", text)
print("Corrected Text:", corrected_text)
