from collections import Counter

# Ciphertext from the document
ciphertext = """lrvmnir bpr sumvbwvr jx bpr lmiwv yjeryrkbi jx qmbm wi

bpr xjvni mkd ymibrut jx irhx wi bpr riirkvr jx

ymbinlmtmipw utn qmumbr dj w ipmhh but bj rhnvwdmbr bpr

yjeryrkbi jx bpr qmbm mvvjudwko bj yt wkbrusurbmbwjk

lmird jk xjubt trmui jx ibndt

wb wi kjb mk rmit bmiq bj rashmwk rmvp yjeryrkb mkd wbi

iwokwxwvmkvr mkd ijyr ynib urymwk nkrashmwkrd bj ower m

vjyshrbr rashmkmbwjk jkr cjnhd pmer bj lr fnmhwxwrd mkd

wkiswurd bj invp mk rabrkb bpmb pr vjnhd urmvp bpr ibmbr

jx rkhwopbrkrd ywkd vmsmlhr jx urvjokwgwko ijnkdhrii

ijnkd mkd ipmsrhrii ipmsr w dj kjb drry ytirhx bpr xwkmh

mnbpjuwbt lnb yt rasruwrkvr cwbp qmbm pmi hrxb kj djnlb

bpmb bpr xjhhjcwko wi bpr sujsru msshwvmbwjk mkd

wkbrusurbmbwjk w jxxru yt bprjuwri wk bpr pjsr bpmb bpr

riirkvr jx jqwkmcmk qmumbr cwhh urymwk wkbmvb"""

# Function to compute letter frequency
def letter_frequency(text):
    text = text.replace(" ", "").replace("\n", "")  # Remove spaces and newlines
    frequency = Counter(text)
    total_letters = sum(frequency.values())
    return {char: round(count / total_letters, 4) for char, count in frequency.items()}

# Compute and print frequencies
cipher_freq = letter_frequency(ciphertext)

print("Ciphertext Letter Frequencies:")
for letter, freq in sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True):
    print(f"{letter}: {freq}")

# Improved manual substitution based on frequency analysis
substitutions = {
    'b': 't', 'p': 'h', 'r': 'e', 'y': 'o', 'j': 'a', 'e': 'r',
    'k': 's', 'v': 'i', 'm': 'n', 'n': 'd', 'i': 'c', 'w': 'm',
    'x': 'y', 'd': 'u', 'l': 'w', 's': 'l', 'u': 'g', 'o': 'b',
    'c': 'f', 'h': 'p', 'a': 'j', 't': 'v', 'q': 'x'
}

# Decrypt the message
decrypted_text = "".join(substitutions.get(char, char) for char in ciphertext)

# Compute decrypted text frequency
decrypted_freq = letter_frequency(decrypted_text)

print("\nDecrypted Message:")
print(decrypted_text)

print("\nDecrypted Text Letter Frequencies:")
for letter, freq in sorted(decrypted_freq.items(), key=lambda x: x[1], reverse=True):
    print(f"{letter}: {freq}")
