# Orignal source code forked (& modified for my custom usecase) from Robert Dempsey at https://github.com/intridea/linkedin-data-miner
#Crafting the company data for scoring/relevance post the entity disambigution.
#Usage - picking up the "company" from the disambiguited list fetched from Disambiguated_master_company_list.py
#MOdules used BeautifulSoup, urllib2
import sys
import urllib2
from bs4 import BeautifulSoup
import csv
import time

linkedin_url_field=[]
company=["sap","amazon","google","24-7-inc","thoughtworks","vmware","ibm","yahoo","ebay","intuit","microsoft","accenture","linkedin","dell","1262","flipkart"]
for m in range(0,len(company)):
    linkedin_url_field.append("http://www.linkedin.com/company/"+company[m]+"?trk=cp_followed_name_"+company[m])
# Deutsche bank was an exception with "1262" as the company name
#print linkedin_url_field
data=[]
for k in range(0, len(linkedin_url_field)):
    url_to_get = linkedin_url_field[k]
    if url_to_get != "N/A":
    # Get the HTML contents of the page and put it into BeautifulSoup
        opener = urllib2.build_opener()
    #adding headers to let the browser think that this comes from a browser, instead of 
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
        li_company_page = opener.open(url_to_get).read()
        soup = BeautifulSoup(li_company_page.decode('utf-8', 'ignore'))

    # Get the company description & specialties from the soup
        basic_li_data = soup.find(attrs = { "class" : "text-logo"})

        if basic_li_data:
            # Get the description
            description = basic_li_data.contents[1].text if basic_li_data else "N/A"
            # Get the specialities
            specialties = basic_li_data.contents[5].text.strip().replace("\n", "") if basic_li_data and len(basic_li_data) >= 5 else "N/A"
            # Potential data to get: website, type, founded, industry, company size
            raw_li_data = soup.find_all(["dt", "dd"])
            if raw_li_data:
                clean_li_data = []
                for x in range(len(raw_li_data)):
                    clean_li_data.append(raw_li_data[x].text.strip())
                all_li_data = dict(clean_li_data[i:i+2] for i in range(0, len(clean_li_data), 2))

            company_size = all_li_data['Company Size'] if 'Company Size' in all_li_data else "N/A"
            website_url = all_li_data['Website'] if 'Website' in all_li_data else "N/A"
            company_name=website_url.replace("http://www.","").replace(".com","")
            industry = all_li_data['Industry'] if 'Industry' in all_li_data else "N/A"
            company_type = all_li_data['Type'] if 'Type' in all_li_data else "N/A"
            year_founded = all_li_data['Founded'] if 'Founded' in all_li_data else "N/A"
            data.append([company_size,website_url ,company_name,industry,company_type,year_founded])
    mywriter = csv.writer(open("C:\Users\Ekta.Grover\Desktop\LinkedinCompanyall.csv", "wb"))
    head = ("Company Size","Company Name", "Website Url", "Industry", "Company Type","Year Founded")
    mywriter.writerow(head)
    for i in range(0,len(data)):
        mywriter.writerow([data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5]])
print ' Finished writing the csv file '

