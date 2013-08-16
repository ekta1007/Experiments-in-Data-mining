#Disambiguated_master_company_list.py
# @Author : Ekta Grover @ekta1007@gmail.com @Date of initial commit : 2nd July, 2013
#Protected under Creative Commons, feel free to borrow & use, with appopriate credits

# Problem Definition : So how much is your Network's net worth ?
# This problem is inspired and extends upon the baby problem mentioned in Matthew A. Russell ‘s Mining the Social Web on Exploring your Linkedin Network data for fun(and possibly profit)
#Future Work : Expand this module to fetch the data from Linkedin RESTTful API's on 
#External Open-source Modules used
"""Using pretty table constructs for frequency plots(prettytable-PrettyTable module) , Frequent Item set Mining (Pymining-itemining Module) and flatening a list of #lists (itertools-chain  module)"""

from prettytable import PrettyTable
from pymining import itemmining
from itertools import chain
import sys
import nltk
import csv
import re

CSV_FILE = 'C:/Users/Ekta.Grover/Desktop/Linkedin_data.csv'

"""The prelim step involves looking up the data to do frequency plots on raw data - this gives an idea of the transformations to do on it, including filtering for stop words. This is important since we do Frequent item set mining - and dont want to give more weightage to stop words like the in "The Bank of America" , The Bank of New York Mellon" - This, ofcourse is only possible since we had a good look at the frequecy maps of the raw data-set 
ALGORITHM
1. Transforming the data, Handling any known abbrevations(example -[24]7 inc is the same as 247)converting to lower case, removing the stop words - This will create a list of similar companies 
[Key is to think about reducing the working space, so that it is "scan'nable by human eyes" for discrepancies]
2. Do Frequency item set mining on the transformed dataset
3. Plot the pretty table on the "standardized data-set" 
"""


csvReader = csv.DictReader(open(CSV_FILE), delimiter=',', quotechar='"')
# Reading the contacts file created via imports in Linkedin and discarding for entries with null - some people may have no company name in the company section of the excel
contacts = [row for row in csvReader]
#Removing any empty company names in the input dataset
companies = [c['Company'].strip() for c in contacts if c['Company'].strip() != '']

#transforming for 24/7 & Walmart labs
for j in range(0,len(companies)):
    if re.search('24', companies[j]) :
        companies[j]='[24]7,Inc'
    elif re.search('walmart', companies[j].lower()) :
        companies[j]='@Walmart labs'
    else:
        try:
            companies[j]=str(companies[j]).lower()
        except UnicodeDecodeError:
            pass
print companies

""" Think data-structures - Creating a dictionary so that similar "values" go in same key, i.e VMware India, VMware inc, and VMware LLC are categorized under the same key in the dict. This comes as {"Vmware" : ['VMware India', 'VMware inc', 'VMware LLC']
Just keeping my_list & companies seperate, though they point to the same object in the memory - this ensures that debugging is clean & efficient"""

my_list=companies

#Theoretically, we could import the stop list from the Web/NLTK's comprehsive stopword list
# We haven't since the stop words in our context require a specific domain knowledge
stop_list=['the','an','a','bank','of']
arr_dict_list = dict()
p=0
for i in range(0, len(my_list)):
    p=0
    while str(my_list[i].split(' ')[p]) in stop_list :
        p=p+1
    if str(my_list[i].split(' ')[p]) in arr_dict_list:
        # append the new enity for the company to the existing array at this slot
        arr_dict_list[str(my_list[i].split(' ')[p])].append(str(my_list[i]))
    else:
        # For the 1st value found for a particular key
        arr_dict_list[str(my_list[i].split(' ')[p])] = [str(my_list[i])]

#So the arr_dict_list is a dict with keys and values as list of "similar" companies - as above        
# back-of of the same arr_dict_list object created above

arr_backup=arr_dict_list 
# Frequent item-set mining
company=[]
for key, value in arr_backup.items():
    if len(value)>1:
        # JUST in case ALL elements are same in the list/set - since a "set" does not allow for duplicates, we use this construct in here
        if len(set(value))==1:
                support = len(value)
                #converting to 1st charater in the company name back to upper case
                for i in range(0,len(value)):
                    value[i]=str(value[i][0]).upper()+str(value[i][1:])
                company.append(value)
        elif len(set(value))>1:
            list6=[]
            for m in range(0, len(value)):
                list6.append(str(value[m]).split())
            transactions=list6
            support = len(value)
            relim_input = itemmining.get_relim_input(transactions)
            report = itemmining.relim(relim_input, support)
            c=report.keys()
            c.sort()
            m=0
            flag=0
            for m in range(0, len(value)):
                for n in range(0,len(list(c[-1]))):
                    if re.search(value[m],list(c[-1])[n]):
                        flag=1
                    else :
                        flag =0
                company.append([str(value[m][0]).upper()+value[m][1:]]*support)
                break
    elif len(value)==1:
        try:
            company.append([value[0][0].upper()+value[0][1:]])
        except IndexError :
            pass
print company
#flattening out the list of list (ie,company)

company_list_final=list(chain.from_iterable(company))
print company_list_final


# now do the frequncy plotting !

pt = PrettyTable(['Company', 'Freq'])
pt.align['Company'] = 'l'
fdist = nltk.FreqDist(company_list_final)
for (company, freq) in fdist.items():
    try:
        pt.add_row([company.decode('utf-8'), freq])
    except UnicodeDecodeError:
        pass
print (pt)
# I am plotting the entire frequnecy maps, while an option could be to have a threshold, and possibly also do cumulative counts as a fraction of overall "Network" population
#Getting the pretty table in A friendlier format - you can export this directly in Excel for further analysis.
from prettytable import MSWORD_FRIENDLY
pt.set_style(MSWORD_FRIENDLY)
print(pt)

