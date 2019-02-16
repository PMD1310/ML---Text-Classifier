import os, copy, random, math
global folder_list, file_name, path, group
group = 'NULL'
print ('The NewsFolder dataset path: C:/Users/pramo/PycharmProjects/TextClassifier/20_newsgroups/')
path = 'C:/Users/pramo/PycharmProjects/TextClassifier/20_newsgroups/'


#To naviagte through the Folder structures to get to the Files we need for preprocessing.
def retreiveFile():
    global group
    while (len(folder_list)):
        #Random_Folder_Index is used for the random generation of an index of a Folder, which will be preprocessed.
        random_folder_index = random.randint(0,len(folder_list)-1)
        #Folder name will be retreived accoridng to the Folder-List's index generated.
        folder_name = folder_list[random_folder_index]
        #Remove the Folder whose length is ZERO.
        if len(file_name[folder_name])== 0:
            folder_list.remove(folder_name)
        else:
            #Random_File_Index is used for the random generation of an index of the file in the Random Folder.
            random_file_index = random.randint(0, len(file_name[folder_name])-1)
            file = file_name[folder_name][random_file_index]
            file_name[folder_name].remove(file)
            group = folder_name
            #Opne the file in read Access Mode
            data = open(path + folder_name + '/'+ file,'r')
            return data.read()
    group = 'NULL'
    return 'NULL'



#To calculate the Probability by passing Words and Word Count.
def calculate_probab(words, word_count):
    sum_ = sum(word_count.values())
    probab = 0.0
    for wo in words:
        value = word_count.get(wo, 0.0) + 0.0001
        probab = probab + math.log(float(value)/float(sum_))
    return probab

#To clean and preprocess the data, the following method will be called.
def cleanData(data):
    data = data.replace('\n', ' ')
    remove_list = ['<','>','?','.','"',')','(','|','-','#','*','+']
    replace_list = ["'",'!','/','\\','=',',',':']
    #To change all the words to lower case.
    data = data.lower()
    #Using a For loop to replace the Remove_List data with "Nothing"
    for rem in remove_list:
        data = data.replace(rem,'')
     #Using a For loop to replace the Replace_List data with "empty Spaces".
    for rep in replace_list:
        data = data.replace(rep,' ')
    return data
#--------------------------Main --------------------------------------------#
#Training set size is 500 since the Test set and the Training set size are 50-50.
training_set = 900
fold_list = os.listdir(path)
i = 0
total_word_count = {}               #Total word count in the file.
word_count_in_folder = {}           #Total Word count in the folder.
file_name ={}                       #Dictionary for the folders and their keys
group = 'NULL'
#print "Starting training part...."
for fo in fold_list:
    #Dictionary to get the word count of all the individual files
    word_count = {}
    #Naivgating to the Folder and the files for the training data set
    folder_train_set = path + fo
    files_train_set = os.listdir(folder_train_set)
    iterator = 0
    for fi in files_train_set:
        iterator = iterator + 1
        if iterator > training_set:
            break
        newPath = folder_train_set + '/'+fi     #Path to reach the file to train the data.
        myfile = open(newPath,'r')
        data = cleanData(myfile.read())          #Cleaning the data  beforehand.
        words = data.split(' ')                     #Splitting the data based on spaces to get the word count.
        for word in words:
            if word == ' ' or word == '':
                continue
            value = word_count.get(word, 0)         #Word count ine each individual file
            value_total = total_word_count.get(word, 0)  #Word count in the entire folder selected.
            if value == 0:
                word_count[word] = 1                #on encountering a new word, its count is set to 1.
            else:
                word_count[word] = value + 1        #On encountering the same word, its count is incremented.
            if value_total == 0:
                total_word_count[word] = 1             #on encountering a new word, its count is set to 1.
            else:
                total_word_count[word] = value_total + 1   #On encountering the same word, its count is incremented.
                #Removing the file after its word count is determined.
        files_train_set.remove(fi)
    file_name[fo] = files_train_set
    word_count_in_folder[fo] = word_count
#print len(total_word_count), 'different words found in all files_train_set'
#print "Starting testing part...."
data = 1
folder_list = copy.deepcopy(fold_list)
iteration = 0
accuracy = 0
while (data):
    data = retreiveFile()   #Calling the Retreive function to get the file.
    iteration = iteration + 1
    if data =='NULL':
        break
    data = cleanData(data) #Calling the CleanData method to preprocess the data.
    #Splitting the data based on the empty spaces
    words = data.split(' ')
    #Removing the empty spaces.
    if '' in words: words.remove('')
    if ' ' in words: words.remove(' ')
    #Probability list for all the probabilities calculated in each individual file/Folder.
    total_probability = []
    #For loop to get the probability of the randomly selected folders.
    for c in folder_list:
        total_probability.append(calculate_probab(words,word_count_in_folder[c]))
    if group == folder_list[total_probability.index(max(total_probability))]:
        accuracy = accuracy + 1
        #Accuracy rate calculation.
print ('accuracy rate = %.1f'% (float(accuracy)/float(iteration - 1)*100))


