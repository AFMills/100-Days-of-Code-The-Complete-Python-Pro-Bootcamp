morse_code_rules = {
    'a': '·−',
    'b': '−···',
    'c': '−·−·',
    'd': '−··',
    'e': '·',
    'f': '··−·',
    'g': '−−·',
    'h': '····',
    'i': '··',
    'j': '·−−−',
    'k': '−·−',
    'l': '·−··',
    'm': '−−',
    'n': '−·',
    'o': '−−−',
    'p': '·−−·',
    'q': '−−·−',
    'r': '·−·',
    's': '···',
    't': '−',
    'u': '··−',
    'v': '···−',
    'w': '·−−',
    'x': '−··−',
    'y': '−·−−',
    'z': '−−··',
    '0': '−−−−−',
    '1': '·−−−−',
    '2': '··−−−',
    '3': '···−−',
    '4': '····−',
    '5': '·····',
    '6': '−····',
    '7': '−−···',
    '8': '−−−··',
    '9': '−−−−·',
    ' ': '/',
    '?': '··--··',
    '!': '-·-·--',
    '.': '·-·-·-',
    ',': '--··--',
    ':': '---···',
    '\'': '·----·',
    '(': '-·--·',
    ')': '-·--·-',
    '_': '··--·-',
    ';': '-·-·-·',
    '+': '·-·-·',
    '-': '-····-',
    '/': '-··-·',
    '=': '-···-',
    '@': '·--·-·',
    '&': '·-···',
    '$': '···-··-',
}

ans = input("Welcome to the Morse Code Converter. \nPlease enter some text to convert:\n").lower()
output = []

def str_to_morse():
    try:
        for letter in ans:
            output.append(morse_code_rules[letter])
    except KeyError:
        print("Sorry! Your text included a symbol not included in Internation Morse Code.")
        quit()
    result = ' '.join(output)
    print(f"The Morse Code of your message is as follows:\n{result}")

str_to_morse()
