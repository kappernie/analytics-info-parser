# analytics-info-parser
#Implementation of  a text cleaning module which validates, parses and cleans the following as inputs: \
a) People names (e.g. Jeffery O’brien) \
b) Email addresses (e.g. devops@corvidai.com)  \
c) Phone number (e.g. +61 4123 567 891) .  \
d) HTTP URLs (e.g. https://www.linkedin.com/company/corvid/) .\
e) Addresses (e.g. 123 Accra Road, Dansoman City, Australia) \ 


<li>The main goal is to validate, clean and standardize the data, handle different scenarios, remove noise, so that it can be used further for other purposes like analytics.\</li>

<li> TODO <li/>
wrap with cmdline argument parser 

<li> SETUP <li/>

a) Make sure you have java install and get your java path from your os \
b) open terminal and create a virtual env \
c) activate and run  pip install -r requirements.txt in venv .  \
d) update java path in script \
e) run app with cmd : python cleantext.py \ 



<li> INPUT   <li/>
 you can find the usage and input examples in script
<li> OUTPUT in terminal <li/>


########EXAMPLE USAGE   ###########  \
######################[email]######################### \
('aa@aa.com', True)\
('kwaku@tmail.com', False)\
['kwaku@tmail.com', 'aa@aa.com']\
['aa@aa.com']\
######################[number]#########################\
(True, True)\
(233, 501591897, None)\
Gh: ['+233244077208', '+233501591897'] ,US: ['+15107488230', '+17034800500']\
Gh: ['+233244077208', '+233501591897'] ,US: ['+15107488230', '+17034800500']\
########################[name]#######################\
('Dr. Juan Q. Xavier de la Vega III (Doc Vega)', True)\
('Dr.', 'Juan', 'Q. Xavier', 'de la Vega', 'III', 'Doc Vega')\
False\
['invalid name input']\
['Ernest', 'John', 'Jane', 'Zii']\
['Ernest', 'John', 'Jane', 'Zii']\
#######################[url]########################\
['www.givers.com', 'https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string', 'www.google.com', 'facebook.com', 'http://test.com/method?param=wasd', 'http://test.com/method?param=wasd&params2=kjhdkjshd'] \
#######################[locations]######################## \
['china', 'canada', 'Ghana']\
###############################################\

<li>Block of Text<li/>
<p>"""My name is Ernest Appau , I am an Engineer at Corvid.ai . You can contact me on 
    02344077208 and +233501591897 or 703-4800500 . I live in Ghana and want to travel 
        one day to the US ,UK ,China,France and Australia. Corvid.ai is an Artificial Intelligence 
            consulting company .The website address is www.corvid.com .You can reach out to the administrator 
                of the site by Hr@corvid.ai or mine (kappernie@corvid.ai). Please note the website is not any of these 
                    go to https//:www.givers.com to donateThe link of this question: https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string
Also there are some urls: www.google.com, facebook.com, http://test.com/method?param=wasd, http://test.com/method?param=wasd&params2=kjhdkjshd
The code below catches all urls in text and returns urls in list . The address of the company is 123 Accra Road, Dansoman City, Australia  """
<p/>

<li>Results for Block of Text<li/>

<p>{'names': ['Ernest', 'Appau'], 'numbers': [{'GH': ['+233501591897']}, {'US': ['+233501591897', '+17034800500']}], 'emails': ['Hr@corvid.ai', 'kappernie@corvid.ai'], 'urls': ['Corvid.ai', 'Corvid.ai', 'www.corvid.com', 'corvid.ai', 'corvid.ai', 'www.givers.com', 'https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string', 'www.google.com', 'facebook.com', 'http://test.com/method?param=wasd', 'http://test.com/method?param=wasd&params2=kjhdkjshd'], 'locations': ['Ghana', 'US', 'UK', 'China', 'France', 'Australia', 'Accra', 'Road', 'Dansoman', 'City']}<p/>
