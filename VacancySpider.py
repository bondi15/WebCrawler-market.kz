#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 19:36:11 2019

@author: bondi
"""

from bs4 import BeautifulSoup
import requests
import csv



# HELPER FUNCTION FOR GATHERING INFO ABOUT ELEMENTS UNDER A 'DIV' FIRST TAG AND UNDEFINED SECOND TAG - VACANCY NAME, SALARY, OWNER, DESCRIPTION

def notoptional_attributes(soup, class_, secondtag, firsttag = 'div'):
    attribute_container = soup.find(firsttag, class_)
    if attribute_container == None:
        print("Not found, check first tag and class!")
        return
    attribute = attribute_container.findChild(secondtag)
    if attribute != None:
        attribute_string = attribute.get_text().strip()
        return attribute_string
    else:
        print("Attribute not found! Returning empty string.")
        return ''


# HELPER FUNCTION FOR GATHERING OPTIONAL JOB SPECIFIC INFO, ALL UNDER SAME PLACE AND STRUCTURE (div->dl->dt->dd) - COMPANY, SPECIALIZATION, EXPERIENCE,
#                                                                                                                  WORK TYPE, SCHEDULE,

def attr(soup,tag,title):
    vac_attr = soup.find(tag, {'title' : title})
    if vac_attr != None:
        attribute = vac_attr.find_next_sibling('dd')
        attr_str = attribute.get_text().strip()
        return attr_str
    else:
        print("Attribute not found! Returning empty string.")
        return ''

#HELPER FUNCTION: SEARCHING BY TEXT. USE ONLY FOR CITY.
        
def attributeloc_text(soup, firsttag, text_, secondtag = 'dd'):
    attribute_container = soup.find(firsttag, text = text_)
    if attribute_container == None:
        print("Not found, check first tag and text!")
        return
    attribute = attribute_container.find_next_sibling(secondtag)
    if attribute != None:
        attribute_string = attribute.get_text().strip()
        return attribute_string
    else:
        print("Attribute not found! Returning empty string.")
        return ''
    


page = requests.get("https://market.kz/rabota/")                    # MAIN PAGE REQUEST
adv_pattern = 'https://market.kz/a/'                                # STRING PATTERN OF ADVERTISMENT PAGES


soup = BeautifulSoup(page.content, 'html.parser')                   # SOUP OBJECT INITIALIZATION


page_main_part = soup.find('div', 'grid_16')                        # SELECTING PAGE PART WHERE ADVERTISMENTS ARE (NEEDED TO SKIP ADVERTISMENT FROM RIGHT SIDE)
links = page_main_part.findChildren('a')                            # GETTING ALL URLS ON THIS PART

advert_links = [link.get('href') for link in links                  # SELECTING URLS LINKED TO ADVERTISMENTS
                if link.get('href').startswith(adv_pattern)]
advert_links = list(set(advert_links))                              # DUMP DUPLICATES



count = 1

with open('VacancyInfo.csv','w') as f1:                                                                  
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)                                               #SETTING UP CSV FILE
    writer.writerow(["URL", "VACANCY NAME", "COMPANY NAME", "SPECIALIZATION", "EXPERIENCE NEEDED", 
                     "WORK TYPE", "SCHEDULE", "DESCRIPTION", "SALARY", "CITY", "OWNER"])

    
    
    # GATHETRING INFO FROM THE DIFFERENT ADVERTISMENT PAGES
    
    for advert_link in advert_links:
                                                                                
        advert_page = requests.get(advert_link)                                                # REQUEST, SOUP, LIST INIT -> CSV
        soup_advert = BeautifulSoup(advert_page.content, 'html.parser')
        CSV_list = []
        CSV_list.append(advert_link)
        
#        print(str(count) + ".  Get for " + advert_link)                                       # PRINTING OUT URL
#        count = count + 1
        
        vacname_str = notoptional_attributes(soup_advert, 'show-header', 'h1')                 # VACANCY NAME
        CSV_list.append(vacname_str)
#        print(vacname_str)
        
        company_str = attr(soup_advert, 'dt', 'Название компании')
        CSV_list.append(company_str)                                                           # COMPANY NAME
#        print(company_str)
        
        spec_str = attr(soup_advert, 'dt', 'Специализация')
        CSV_list.append(spec_str)                                                              # SPECIALIZATION
#        print(spec_str)
        
        exp_str = attr(soup_advert, 'dt', 'Опыт работы')      
        CSV_list.append(exp_str)                                                               # EXPERIENCE
#        print(exp_str)
        
        work_type_str = attr(soup_advert, 'dt', 'Тип занятости')
        CSV_list.append(work_type_str)                                                         # WORK TYPE
#        print(work_type_str)
        
        schedule_str = attr(soup_advert, 'dt', 'График работы')
        CSV_list.append(schedule_str)                                                          # SCHEDULE
#        print(schedule_str)
        
        description_str = notoptional_attributes(soup_advert, 'description', 'p')
        CSV_list.append(description_str)                                                       # DESCRIPTION
#        print(description_str)
        
        salary_str = notoptional_attributes(soup_advert, 'misc-fields field-price', 'dd')
        CSV_list.append(salary_str)                                                            # SALARY
#        print(salary_str)
        
        city_str = attributeloc_text(soup_advert, 'dt', 'Город')                               # CITY
        CSV_list.append(city_str)
#        print(city_str)
        
        owner_str = notoptional_attributes(soup_advert, 'advert-owner__name', 'a')
        CSV_list.append(owner_str)                                                             # OWNER
#        print(owner_str)
        

        CSV_list = ["\"" + element + "\"" for element in CSV_list]              # NEEDED TO SHOW CORRESPONDENT ELEMENTS CORRECTLY AFTER 
                                                                                # EXPORTING TO CSV (DUE TO THE PRESENT COMMAS IN THE GATHERED INFO)
    
    
        writer.writerow(CSV_list)                                               # WRITE LIST INTO A ROW IN CSV
