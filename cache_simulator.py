'''
Trabalho: Simulador de memória cache parametrizável
Linguagem: Python
Nomes: Christopher Conceição Moura, Yuri Borges Sena
Disciplina: Arquitetura e organização de computadores II
'''
from datetime import datetime # for log files
from random import randint  # for random
def cacheFull(cache): # checks if cache is full
    for x in cache:
        if x[0] == -1:
            return False
    return True
def readBuffer(buffer): # reads the buffer to set the cache configuration ([nsets:bsize:assoc] file)
    setup = []
    if buffer[0] == 'd':    # d = default setup
        print('default setup:\nnsets: 1024, bsize: 4, assoc: 1')
        setup.append(1024)  # nsets
        setup.append(4)     # bsize
        setup.append(1)     # assoc
        return setup
    aux = ""    # auxiliar string
    for i in buffer:
        if i.isdigit() == True:
            aux += i
        else:
            setup.append(int(aux))
            if len(setup) == 3:
                break
            aux = ""
    return setup
def setBlock(cache, random, i, bsize): # sets contiguous words in the block
    if bsize == 4:
        cache[random][0] = i
        return cache
    else:
        cache[random][i%int(bsize/4)] = i
        for word in range(0, int(bsize/4)):
            if cache[random][word] != i:
                cache[random][word] = i-(i%int(bsize/4))+word
    return cache
def getFileName(buffer): # reads the file name in the buffer (nsets:bsize:assoc [file])
    fileName = ''
    i=0
    while buffer[i] != ' ': # while i not in space - buffer: [nsets:bsize:assoc |here| file]
        i+=1
    i+=1
    while i != len(buffer):
        fileName += buffer[i]
        i+=1
    return fileName
def createCache(nsets, bsize, assoc): # creates cache structure
    auxArray = []   # auxiliary array for module values
    cache = []
    c=assoc-1
    if assoc == 1:
        auxArray.append([0, nsets])
    else:
        for i in range(0, nsets):
            if i == 0:
                auxArray.append([0, c])
                c+=1
            else:
                auxArray.append([c, c+assoc-1])
                c+=assoc
    for i in range(0, nsets*assoc):
        cache.append([])
        for j in range(0, int(bsize/4)):
            cache[i].append(-1)
    return auxArray, cache
def readFile(buffer):  # reads input binary file
    valueList = []
    with open(getFileName(buffer), "rb") as file_content:
        for num in iter(lambda: file_content.read(4), b''):
            valueList.append(int.from_bytes(num, byteorder='big'))
    return valueList
def getTestIndex(): # iterates index of log files
    file = open("cache_logs/testIndex [don't delete this].txt", "r")
    idx = file.read()
    file.close()
    file = open("cache_logs/testIndex [don't delete this].txt", 'w')
    file.write(str(int(idx)+1))
    file.close()
    return idx
def genLogFile(hit, accesses, compulsory, capacity, conflict, fileName, cache_setup): # generates log files
    testIndex = getTestIndex()
    logFile = open('cache_logs/log-file_%s.txt' % testIndex, 'w')
    logFile.write('Data/hora do relatório:              %s\n' % datetime.now())
    logFile.write('---------------------------------------------------------------------------\n')
    logFile.write('Cache config (nsets:bsize:assoc):    %s\n' % cache_setup)
    logFile.write('Nome do benchmark:                   %s\n' % fileName)
    logFile.write('Total de acessos:                    %s\n' % str(accesses))
    logFile.write('Total de hits:                       %s /' % str(hit))
    logFile.write(' %s%% (taxa)\n' % str(round(float(round(hit/accesses, 2))*100, 1)))
    logFile.write('Total de misses:                     %s /' % str(compulsory+capacity+conflict))
    logFile.write(' %s%% (taxa)\n' % str(round(float(round(1-hit/accesses, 2))*100, 1)))
    logFile.write('Total de misses compulsórios:        %s\n' % str(compulsory))
    logFile.write('Total de misses de capacidade:       %s\n' % str(capacity))
    logFile.write('Total de misses de conflito:         %s\n' % str(conflict))
    logFile.close()
    print('\nCache simulada com sucesso!')
    print('---------------------------------------------------------')
    print('Cache config (nsets:bsize:assoc):    %s' % cache_setup)
    print('Nome do benchmark:                   %s' % fileName)
    print('Total de acessos:                    %s' % str(accesses))
    print('Total de hits:                       %s /' % str(hit) + ' %s%% (taxa)' % str(round(float(round(hit/accesses, 2))*100, 1)))
    print('Total de misses:                     %s /' % str(compulsory+capacity+conflict) + ' %s%% (taxa)' % str(round(float(round(1-hit/accesses, 2))*100, 1)))
    print('Total de misses compulsórios:        %s' % str(compulsory))
    print('Total de misses de capacidade:       %s' % str(capacity))
    print('Total de misses de conflito:         %s' % str(conflict))
    print('\n< Arquivo de log criado em /cache_logs/log-file_%s.txt >\n' % testIndex)
def testCache(cache, auxArray, valueList, nsets, bsize, assoc):  # cache test
    flag = 0    # flag variable for miss cases
    hit = 0     # hit counter
    compulsory = 0  # compulsory counter
    capacity = 0    # capacity counter
    conflict = 0    # conflict counter
    for i in valueList:
        if assoc > 1:
            rangeArray = auxArray[i % nsets]
            randomPosition = randint(rangeArray[0], rangeArray[1])
        else:
            rangeArray = auxArray[0]
            randomPosition = i%rangeArray[1]
        for j in range(rangeArray[0], rangeArray[1]):   # j = index of sets
            if cache[j][i%int(bsize/4)] == i:
                hit += 1
                flag = 2
                break
        if cacheFull(cache) == False and flag != 2:
            if cache[randomPosition][i%int(bsize/4)] == -1 and flag != 2:
                compulsory += 1
                flag = 1
            elif flag != 2 and cache[randomPosition][i%int(bsize/4)] != -1:
                conflict += 1
                flag = 1
        elif flag != 2:
            capacity+=1
        if flag != 2:
            cache = setBlock(cache, randomPosition, i, bsize)
        flag = 0
    return compulsory, capacity, conflict, hit
# main
while(0<1):
    print("\nEntre com um dos seguintes formatos\n\nConfiguração de cache:  nsets:bsize:assoc nome_do_arquivo.dat\nConfiguração default:   d nome_do_arquivo.dat\nSair do programa:       exit\n")
    buffer = input()
    if buffer != "exit":
        cache_setup = readBuffer(buffer)    # cache_setup = [nsets, bsize, assoc]
        if cache_setup[1] > 3:  # doesn't accept block size less than a word
            valueList = readFile(buffer)
            auxArray, cache = createCache(cache_setup[0], cache_setup[1], cache_setup[2])
            accesses = len(valueList)
            compulsory, capacity, conflict, hit = testCache(cache, auxArray, valueList, cache_setup[0], cache_setup[1], cache_setup[2])  # starts the test in the cache and saves the results
            genLogFile(hit, accesses, compulsory, capacity, conflict, getFileName(buffer), cache_setup) # generates the log file with previously saved results
        else:
            print('< Erro: bsize deve ser maior que 4 >')
    else:
        print("Encerrando cache_simulator...")
        break
