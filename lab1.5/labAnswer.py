from base64 import b64encode, b64decode
import binascii
import codecs
from os import terminal_size
from Crypto.Cipher import AES

def hexToBase64(text):
    output = b64encode(bytes.fromhex(text)).decode();
    return output;

def fixedXOR(number1, number2):
    return hex(number1^number2);

def singelXORCypher(text):
    nums = binascii.unhexlify(text.strip());
    strings = [];
    for key in range(128):
        strings.append((''.join(chr(num ^ key) for num in nums)));
    
    # space should be apppear at largest frequency
    return(max(strings, key=lambda s: s.count(' ')));

def calcSentenceScore(text):
    score = 0;
    for c in text:
        if c.isalpha():
            score += 1;

    return score;

def detectSignleCharXor(text):
    strings = [];
    result = [];
    tempString = '';
    for i in range(len(text)):
        if i+60 < len(text):
            tempString = text[i:i+60];
            strings.append(tempString);

    for chunk in strings:
        result.append(singelXORCypher(chunk));

    return(max(result, key=lambda s: calcSentenceScore(s)));

def repeatXOR(text, key):
    result = [text[index] ^ key[index%len(key)] for index in range(len(text))];
    result = binascii.hexlify( bytes(result));
    result = format(int(result,16),'x')
    return result;

def differentBits(a, b):
	return sum((a & (1 << i)) != (b & (1 << i)) for i in range(0, 8))

def hamming(s1, s2):
    return sum(differentBits(c1, c2) for c1, c2 in zip(s1, s2))

def aesECBDecry(text, key):
    aes_ecb128 = AES.new(key, AES.MODE_ECB);
    return aes_ecb128.decrypt(text);


def detectECB(texts):
    candidateLines = [];
    for line in texts:
        i = 0;
        blocksDict = {};
        repeatedPattern = 0;

        while i+16 < len(line):
            block = line[i:i+16];
            if block not in blocksDict:
                blocksDict[block] = 0;
            else:
                blocksDict[block] +=1;
            i = i+16;
        for key in blocksDict.keys():
            if blocksDict[key] > 1:
                repeatedPattern += 1;
        if repeatedPattern > 1:
            candidateLines.append(line);
    return candidateLines;


if __name__ == "__main__":
    print("Convert hex to base64:");
    print(hexToBase64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"));
    
    print("Fixed XOR:");
    xorOutput = fixedXOR(int("1c0111001f010100061a024b53535009181c",16), int("686974207468652062756c6c277320657965",16));
    xorOutput = format(int(xorOutput,16),'x')
    print(xorOutput);

    print("Single Byte XOR Cypher:")
    print(singelXORCypher("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"));

    
    file = open("./3.txt");
    detectInput = '';
    for line in file.readlines():
        detectInput += line.strip();
    print("Detect single-character XOR:");  
    print(detectSignleCharXor(detectInput));

    print("Repeating-key XOR");
    print(repeatXOR(b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal",b"ICE"));

    print("Hamming Distance:");
    print(hamming(b"this is a test", b"wokka wokka!!!"));

    print("AES in ECB mode");
    fd = open("./7.txt", "r")
    ciphertext = b64decode(fd.read());
    mKey = b"YELLOW SUBMARINE";
    print(aesECBDecry(ciphertext, mKey));

    print("Detect AES in ECB mode:");
    ecbFile = open("./8.txt")
    ecbTexts = ecbFile.readlines();
    print("The line in the file encrypted in ECB is")
    print(detectECB(ecbTexts));
    