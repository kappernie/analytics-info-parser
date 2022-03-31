# Author : Appau Ernest

from email_validator import validate_email, EmailNotValidError 
import phonenumbers,re
from nameparser import HumanName
import nltk
import nltk.tag as st
import os

# make sure you install java first
# set your java path for nltk dependency
java_path = "/usr/share/java/"
os.environ['JAVAHOME'] = java_path


# check out postal for location parsing if it works for you 
# go to this link to install dependencies for your env 
# https://github.com/openvenues/libpostal
#before installing the py module 

 
class Data():
    # named the class data since I dont know what you want to analyze logs etc 
    def __init__(self,name = None , email = None ,\
         address = None , phoneNo = None , url = None , Geocode = None ,text = None  ):
        # handle default lib stuff init here 
        self.text = text
        self.name = name
        self.email = email
        self.address = address
        self.phoneNo = phoneNo
        self.url = url
        self.logger = 'syslog' #set logger to log errors :Todo
        self.Geocode = ['GH','US']  
        #get more info about \ 2 digit country codes on this url {https://countrycode.org/}
        self.english_file = './stanford-ner/english.all.3class.distsim.crf.ser.gz'
        self.ner_file = './stanford-ner/stanford-ner.jar'
                
       

    ################## name methods 
    #issue here: its going to be tough parsing names linked 
    # to specific Geographics like Ama or shi jing ping 
    # My suggestion, you can make the parse method better 
    # by training and Adding named entity recognizer for unique names  


    def validate_name(self , name ):
        # checks if the input has one of the features of a name
        # and returns Bool
        # we can add nltk ner implemetation here too if need @ Jeff as a fail safe 
        name_status  = False
        try:
            t,f,m,l,s,n = self.parse_name(name)
            if isinstance(f,str) and isinstance(m,str) and isinstance(l,str):
                name_status = True
                return name ,name_status 
            return name ,name_status
        except:
            return name_status


    def parse_name(self ,name):
        # expects a single name (alphanum or str )
        if name  and  isinstance(name,str):
            self.name = name 
            try:
                name = HumanName(name)
                return name.title,name.first,name.middle,name.last\
                ,name.suffix ,name.nickname
            except Exception as e :
                return ["invalid name input"]
        return ["invalid name input"]

    def parse_names_in_noise(self ,text):
        # Jeff can add any extra regex or nltk stuff\
        #   here to parse names from text or use custom ner
        names = []
        if isinstance(text, str):
            st1 = st.StanfordNERTagger(self.english_file , self.ner_file)
            for sent in nltk.sent_tokenize(text):
                tokens = nltk.tokenize.word_tokenize(sent)
                tags = st1.tag(tokens)
                for tag in tags:
                    if list(tag)[1] =='PERSON':
                        if list(tag)[0] not in names:
                            names.append(list(tag)[0])
            return names
        return ['invalid text input']


    def clean_names(self, names):
        # get a list of names from the method
        #  above and validates them
        valid_names = []
        if names:
            for name in names:
                _,status = self.validate_name(name)
                if status:
                    valid_names.append(name)
            return valid_names
        return " [no valid names]"


    
        pass

    ########### email methods 
    def validate_email(self,email):
        email_status = False
        if email and isinstance(email, str):
            self.email = email 
            try:
                valid = validate_email(email)
                email = valid.email
                email_status = True
                return email,email_status 
            except EmailNotValidError as e:
                return email,email_status
        else:
            return email,email_status

    def parse_email_in_noise(self ,text):
        # get all email addresses in text 
        if text:
            emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
            return emails 
        else:
            return "[no text passed]"

    def clean_email(self , emails):
        # clean will have to be some extra custom regex stuff from jeff

        # NB: current implementation is to go through the response from the above
        # method and return valid emails 
    
        valid_mails = []
        if emails:
            for mail in emails:
                _,status = self.validate_email(mail)
                if status:
                    valid_mails.append(mail)
            return valid_mails
        return " [no valid mails]"

    ############### phone number methods

    def validate_phonenumber(self ,number):
        # ideally I would assume this would  interact 
        # with an api but we just check of its a number
        if number:
            self.number = number 
        number = phonenumbers.parse(number , None)
        try:
            # check if number is possible 
            is_possible = phonenumbers.is_possible_number(number )
            # check if number is valid 
            is_number  = phonenumbers.is_valid_number(number )
            return is_possible,is_number
        except Exception as e:
            # print(e)
            return "not a pnumber"

    def parse_phonenumber(self , number):
        # get the  cc,nn,l0 if a number 
        if number:
            self.number = number 
        try:
            number = phonenumbers.parse(number , None)
            return number.country_code , number.national_number ,\
                number.number_of_leading_zeros
        except Exception as e :
            # print(e)
            return "Not a pnumber"

    def parse_phonenumber_in_noise(self , text , geocode):
        # get all the country numbers in text,default gh
        pnum_list = []
        if geocode and geocode in self.Geocode:
            pass
        elif not geocode:
            geocode = 'GH' # change default here to your preferred country code 
        else:
            return "Geocode does not exist"
        for match in phonenumbers.PhoneNumberMatcher(text,geocode):
            match = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
            pnum_list.append(match) 
        return pnum_list

    def clean_phonenumber(self ,numbers):
        # clean will have to be some excustom regex stuff from jeff 

        # otherwise the default is to go through the results 
        # from the method above and validate the phonenumbers 
        valid_numbers = []
        if numbers:
            for number in numbers:
                _,status = self.validate_phonenumber(number)
                if status:
                    valid_numbers.append(number)
            return valid_numbers
        return " [no Valid numbers]"

    ########## url methods 
    def validate_url(self):
        # depends on your csutomization eg ping that url to checkk if it exists
        pass
    def parse_url_in_noise(self ,text):
        if text:
            urls=  re.findall(r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+" , text)
            return urls
        return ['invalid text input']

    def clean_url(self):
        # clean will have to be some custom regex stuff from jef
        pass

    ########## address methods 
    #issue here: its going to be tough parsing  address names linked 
    # to specific Geographics like Accra or ' broadie bebu abo me'
    # My suggestion, you can make the parse method better
    # by training and Adding named entity recognizer for locations 
    # or add and keep updating a list of location names 
    # others could include using a google map location as a validator 
    
    def parse_address_in_noise(self,text):
        # postal would be ideal , you chedk it out 
        # https://github.com/openvenues/libpostal

        # This just gets address names
        locations = []
        if isinstance(text, str):
            st1 = st.StanfordNERTagger(self.english_file , self.ner_file)
            for sent in nltk.sent_tokenize(text):
                tokens = nltk.tokenize.word_tokenize(sent)
                tags = st1.tag(tokens)
                for tag in tags:
                    if list(tag)[1] =='LOCATION':
                        if list(tag)[0] not in locations:
                            locations.append(list(tag)[0])
            return locations
        return ['invalid text input']

    def analyze_text(self,text = None , geocode = None):
        if text and  isinstance(text,str):
            self.text=text
        if geocode and  isinstance(text,list):
            self.Geocode = geocode
        if self.text:
            get_names       = self.parse_names_in_noise(self.text)
            get_numbers     = [{i : self.parse_phonenumber_in_noise(self.text, i)} for i in self.Geocode ]
            get_emails     = self.parse_email_in_noise(self.text)
            get_urls        = self.parse_url_in_noise(self.text)
            get_locations   = self.parse_address_in_noise(self.text)
            return get_names,get_numbers,get_emails,get_urls,get_locations
        return '[Invalid text input]'
        
 
   
    

# ToDo
# email - done
# phone number number - done 
# name - almost
# url  - almost
# email-address - MultiNested  - almost -check postal package  



print('########EXAMPLE USAGE   ###########')

print("######################[email]#########################")
# usage: email
mail1 = "aa@aa.com"
mail2 = "kwaku@tmail.com"
text = 'my link is kwaku@tmail.com and aa@aa.com'
singleMailsValidation1 =Data().validate_email(mail1)
singleMailsValidation2 =Data().validate_email(mail2)
emails = Data().parse_email_in_noise(text)
vmails = Data().clean_email(emails)

print(singleMailsValidation1) #valid mail
print(singleMailsValidation2) #invalid mail
print(emails) # parse mail from text
print(vmails) # clean parsed mail from text


print("######################[number]#########################")

# usage: phonenumber
number1 = "+442083661177"
number2 = "+233501591897"
text = "Call me at 510-748-8230 if it's before 9:30, or on 703-4800500  or 0244077208 or 233501591897 or after 10am."
singlenumValidation1 =Data().validate_phonenumber(number1)
singlenumValidation2 =Data().parse_phonenumber(number2)
numbers_gh = Data().parse_phonenumber_in_noise(text , "GH")
numbers_us = Data().parse_phonenumber_in_noise(text , "US")
vnumbers_gh = Data().clean_phonenumber(numbers_gh)
vnumbers_us = Data().clean_phonenumber(numbers_us)

print(singlenumValidation1) #valid number
print(singlenumValidation2) #invalid number 
print('Gh:',numbers_gh , ",US:" , numbers_us ) # parse numbers from text with specific geocode
print('Gh:',vnumbers_gh , ",US:" , vnumbers_us ) # clean parsed numbers from text

print("########################[name]#######################")
# usage: name
# notice its not bullet proof for african names lol -African lives matter 
# to missing some names you are expecting per Geolocation  add a list per geo
name1 = "Dr. Juan Q. Xavier de la Vega III (Doc Vega)"
name2 = 1
text = 'Ernest , John and Jane are not African names.Ernest ,\
    Ama and kofi are bed fellows ,Zii jing ping is the president of China 5678 and Canada'
singlenamesValidation1 =Data().validate_name(name1)
singlenamesValidation10 =Data().parse_name(name1)
singlenamesValidation2 =Data().validate_name(name2)
singlenamesValidation20 =Data().parse_name(name2)
names = Data().parse_names_in_noise(text)
vnames = Data().clean_names(names)

print(singlenamesValidation1) #valid name
print(singlenamesValidation10) #valid name
print(singlenamesValidation2) #invalid name
print(singlenamesValidation20) #valid name
print(names) # parse name from text
print(vnames) # clean parsed name from text


print("#######################[url]########################")

# usage: url
text = """go to https//:www.givers.com to donateThe link of this question: https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string
Also there are some urls: www.google.com, facebook.com, http://test.com/method?param=wasd, http://test.com/method?param=wasd&params2=kjhdkjshd
The code below catches all urls in text and returns urls in list. """
urls = Data().parse_url_in_noise(text)
print(urls)

print("#######################[locations]########################")

# usage: physical addresses
text = "china,canada and Ghana are some countries in the world."
addresses  = Data().parse_address_in_noise(text)
print(addresses)

print("#####################[Block of text]#########################")
text1 = """My name is Ernest Appau , I am an Engineer at Corvid.ai . You can contact me on 
    02344077208 and +233501591897 or 703-4800500 . I live in Ghana and want to travel 
        one day to the US ,UK ,China,France and Australia. Corvid.ai is an Artificial Intelligence 
            consulting company .The website address is www.corvid.com .You can reach out to the administrator 
                of the site by Hr@corvid.ai or mine (kappernie@corvid.ai). Please note the website is not any of these 
                    go to https//:www.givers.com to donateThe link of this question: https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string
Also there are some urls: www.google.com, facebook.com, http://test.com/method?param=wasd, http://test.com/method?param=wasd&params2=kjhdkjshd
The code below catches all urls in text and returns urls in list . The address of the company is 123 Accra Road, Dansoman City, Australia  """


try:
    a,b,c,d,e = Data(text = text1).analyze_text()
    print({'names':a,'numbers':b,'emails':c,'urls':d,'locations':e})
    if 
except:
    pass