#My notes/answers from the Python intro

def c_squared (a, b):
    return a**2 + b**2

def string_slice(str, a,b,c,d):
    return str[a:b+1] + " " + str[c:d+1]

def odd_sum(a,b):
    res = 0
    for i in range(a,b):
        if i%2:
            res+=i
    return res

def even_line(inp):
    f = open(inp,"r")
    list = (f.read()).split("\n")
    f.close()
    f = open(inp,"w")
    for n in range(1,len(list),2):
        f.write(list[n]+"\n")
    f.close()

def word_count(str):
    words = {}
    for i in str.split():
        if i in words:
            words[i] += 1
        else:
            words[i] = 1
    for key,value in words.items():
        print(key,end=" ")
        print(value)
    

print(c_squared(883,880))
String1 = "OlKNHrlKQH6IMzuwv9E8NAsPPXUqtK3sQEfSNba2RJ7AH4EyqLqJvobItYki5J47YW2mDox1hf49LNMgEad93jRAiDendrelaphisuvrOikuYLQ9hPfH7v8fLe5CsgZGxNKQSS0rPro7EWSmLCjJOLg8twv6j5xfljPRJUnHvJDHFIZTrLFagamaHRQkmRIe6iul."
print(string_slice(String1,89,100,179,183))
print(odd_sum(4348,9034))
even_line("rosalind_ini5.txt")
String2 = "When I find myself in times of trouble Mother Mary comes to me Speaking words of wisdom let it be And in my hour of darkness she is standing right in front of me Speaking words of wisdom let it be Let it be let it be let it be let it be Whisper words of wisdom let it be And when the broken hearted people living in the world agree There will be an answer let it be For though they may be parted there is still a chance that they will see There will be an answer let it be Let it be let it be let it be let it be There will be an answer let it be Let it be let it be let it be let it be Whisper words of wisdom let it be Let it be let it be let it be let it be Whisper words of wisdom let it be And when the night is cloudy there is still a light that shines on me Shine until tomorrow let it be I wake up to the sound of music Mother Mary comes to me Speaking words of wisdom let it be Let it be let it be let it be yeah let it be There will be an answer let it be Let it be let it be let it be yeah let it be Whisper words of wisdom let it be"
word_count(String2)