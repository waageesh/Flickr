fa = open("myfile.txt", "a+")

fa.write("Now the file has one more line!\n")
fa.write("...and 4th one!\n")



fr = open("myfile.txt", "r")
print(fr.readlines())

fa.flush()
print(fr.readlines())


import requests
image = requests.get('https://simpleisbetterthancomplex.com/media/2018/02/thumbnail-tip22.jpg')