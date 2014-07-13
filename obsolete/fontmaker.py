## start by reading the file

original = open('originalFont', 'r')
dataset = []

for line in original:
    line = line.strip()
    char = line[-1]
    line = line.split(',')
    line[-1] = char
    dataset.append(line)

original.close()


newfile = open('newFont', 'w')

newFont = {}
for i in range(len(dataset)):
    newLetter = ['' for temp in range(7)]
    for j in range(len(dataset[i])-1):
        binrep =bin(int(dataset[i][j], 16))[2:].zfill(7)
        for k in range(7):
            newLetter[k] += (binrep[k])
    newfile.write("{},{},{},{},{},{},{},{}\n".format(dataset[i][5], 
        newLetter[0], newLetter[1], newLetter[2], newLetter[3], 
        newLetter[4], newLetter[5], newLetter[6]))
    newFont[dataset[i][5]] = newLetter
    
##print(newFont)
