import urllib
import urllib2
import cookielib
from HTMLParser import HTMLParser
from htmlentitydefs import entitydefs
from datetime import date

# Login Information
login_1 = urllib.urlencode({'j_username': 'XXXXX',
                              'j_password': 'XXXXXXXXX'})

                              
another_email = 'tangziyi001@gmail.com'
optional_title = 'Tang Reservation'

# Final Report List
report = []

# Parser Classes
class SAMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        
        self.results=[]
        
    def handle_startendtag(self, tag, attrs):
        if tag=='input':
            
            if len(attrs)==0:
                pass
            else:
                for name,value in attrs:
                    if name == "value":
                        self.results.append(value)
                        
    def getValues(self):
        return self.results

class SLOTParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.room_values=[]
        
        
    def handle_startendtag(self, tag, attrs):
        if tag=='input':
            if len(attrs)==0:
                pass
            else:
                for name,value in attrs:
                    if name == "disabled" and value == "disabled":
                        break
                    if name == "name" and value != "reservation[room_id]":
                        break
                    if name == "value":
                        self.room_values.append(value)
                        
    def getRoomValues(self):
        return self.room_values
   
        
class INPUTParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.input_values=[]
        
        
    def handle_startendtag(self, tag, attrs):
        if tag=='input':
            if len(attrs)==0:
                pass
            else:
                for name,value in attrs:
                    if name == "name" and value == "reservation[room_id]":
                        break
                    if name == "value":
                        self.input_values.append(value)
                        
    def getInputValues(self):
        return self.input_values


# Choose Room According to an order
def chooseRoom(rooms):

    if '107' in rooms:
        room_number=107
    elif '105' in rooms:
        room_number=105
    elif '106' in rooms:
        room_number=106
    elif '94' in rooms:
        room_number=94
    elif '108' in rooms:
        room_number=108
    else:
        print "No Rooms"
    print room_number
    return room_number
    
# Translate room number
def roomRaw(room_id):
    if room_id==106:
        return 'LL2-07'
    elif room_id==107:
        return 'LL2-08'
    elif room_id==105:
        return 'LL2-22'
    elif room_id==94:
        return '(Please check your email)'
    elif room_id==108:
        return 'LL2-09'
    else:
        print "No Rooms"
    print room_number
    
# Find Date
def findDate(page):
    head = page.rfind('<strong>Date:</strong>')
    
    # Directly set to a specific date
    # return 2015-01-31
    
    # Set to today if no reservation before
    if head == -1:
        now = date.today()
        nowdate = now.strftime("%Y-%m-%d")
        
        return nowdate
        
    date = page[head+28:head+40]
    month_word = date[0:3]
    day = date[4:6]
    year = date[8:12]
    
    # Change month to number
    month = '00'
    if month_word=='Jan':
        month = '01'
    elif month_word=='Feb':
        month = '02'
    elif month_word=='Mar':
        month = '03'
    elif month_word=='Apr':
        month = '04'
    elif month_word=='May':
        month = '05'
    elif month_word=='Jun':
        month = '06'
    elif month_word=='Jul':
        month = '07'
    elif month_word=='Aug':
        month = '08'
    elif month_word=='Sep':
        month = '09'
    elif month_word=='Oct':
        month = '10'
    elif month_word=='Nov':
        month = '11'
    elif month_word=='Dec':
        month = '12'
    
    # Change numbers to int
    year = int(year)
    month = int(month)
    day = int(day)
    
    day+=2
    # Set to the day after Tomorrow
    if day>31 and (month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):   
       day=day%31
       month+=1
       if month>12:
           month=1
           year+=1
    elif day>30 and (month==4 or month==6 or month==9 or month==11):
       day=day%30
       month+=1
    elif day>28 and month==2:
        day=day%28
        month+=1
    year = str(year)
    month = str(month).rjust(2,'0')
    day = str(day).rjust(2,'0')
    newdate = year+'-'+month+'-'+day
    return newdate
    

# Main Program: The date should be default if booking a room at the day after tomorrow

def reserveRoom(account=login_1, email=another_email, title=optional_title, time='8', date='default'):
    try:
        # Cookie Settings
        jar = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(jar)
        opener = urllib2.build_opener(handler)
        opener.addheaders=[('User-Agent','Mozilla/5.0')]
        urllib2.install_opener(opener)
   
        # Load page
        print """

---------- Processing...Start Reservation for This Account----------

        """
    
        # GET the library login page
        #urlrsv = "https://login.library.nyu.edu/pds?func=load-login&institute=NYU&calling_system=https:login.library.nyu.edu&url=https%3A%2F%2Frooms.library.nyu.edu%2Fvalidate%3Freturn_url%3Dhttps%253A%252F%252Frooms.library.nyu.edu%252F%26https%3A%2F%2Flogin.library.nyu.edu_action%3Dnew%26https%3A%2F%2Flogin.library.nyu.edu_controller%3Duser_sessions"
    
        # req = urllib2.Request(urlrsv)
        # data=urllib2.urlopen(req)
        # print data.geturl()

        # GET the SSO login page
        urllogin="https://login.library.nyu.edu/Shibboleth.sso/Login?target=https%3A%2F%2Flogin.library.nyu.edu%2Fpds%3Ffunc%3Dload-login%26institute%3DNYU%26calling_system%3Dhttps%3Alogin.library.nyu.edu%26url%3Dhttps%253A%252F%252Frooms.library.nyu.edu%252Fvalidate%253Freturn_url%253Dhttps%25253A%25252F%25252Frooms.library.nyu.edu%25252F%2526https%253A%252F%252Flogin.library.nyu.edu_action%253Dnew%2526https%253A%252F%252Flogin.library.nyu.edu_controller%253Duser_sessions"
        
        req_login = urllib2.Request(urllogin)
        login_page_data=urllib2.urlopen(req_login)


        print login_page_data.read()
        print """

---------- Initial Page Request is Successful. Processing ----------

        """


        # POST the next page with login information
        url_next="https://shibboleth.nyu.edu/idp/Authn/UserPassword"
        next=urllib2.urlopen(url_next,account)
        next_page=next.read()
        print next_page
        print """

---------- Login is successful. Processing ----------

        """

        # Excerpt and Copy the SAML Information
        saml_parser=SAMLParser()
        saml_parser.feed(next_page)
        relay_state=saml_parser.getValues()[0]
        saml_response=saml_parser.getValues()[1]
        saml_parser.close()

        saml_input=urllib.urlencode({
            'RelayState':relay_state,
            'SAMLResponse':saml_response
        })
        print saml_input
        print """

---------- Successfully get the SAML Response and RS. Processing ----------

        """
        # POST after the Continuous Page
        url_saml_post="https://login.library.nyu.edu/Shibboleth.sso/SAML2/POST"
        saml_post = urllib2.urlopen(url_saml_post, saml_input)
        print saml_post.read()
        print """

---------- Successfully submit the SAML Response and RS. Processing ----------

        """
        # GET the Reservation Page
        url_rsv="https://rooms.library.nyu.edu/"
        rsv_page_open=urllib2.urlopen(url_rsv)
        rsv_page=rsv_page_open.read()
        print rsv_page
        print """

---------- Successfully Open the Reservation Page. Processing ----------

        """
    
        # Look at the latest reservation
        # or set by the programmer
        new_date = '2014-03-01'
        if date == 'default':
            new_date=findDate(rsv_page)
            print new_date
            print """
    
---------- Successfully Find the Latest Reservation. Processing ----------

            """
        else:
            new_date = date
            print new_date
            print """
    
---------- Successfully Read Your Reservation. Processing ----------

            """
        
    
        # GET the page indicationg the time slots
        url_submit="https://rooms.library.nyu.edu/reservations/new"
        submit_data=urllib.urlencode({
    
            'reservation[which_date]':new_date,
            'reservation[hour]':time,
            'reservation[minute]':'0',
            'reservation[ampm]':'pm',
            'reservation[how_long]':'120'
    
        })
        print submit_data
        print """

---------- Prepare to Fill In the Reservation Info. Processing ----------

        """

        # GET all time slots
        rsv_submit = urllib2.urlopen(url_submit+"?"+submit_data)
        available_page=rsv_submit.read()
        print available_page
        print """

---------- Successfully Load All Time Slots. Processing ----------

        """

        # Find available slots
        slot_parser = SLOTParser()
        slot_parser.feed(available_page)
        available_room=slot_parser.getRoomValues()
        print "Available Rooms:",available_room
        slot_parser.close()
        input_parser = INPUTParser()
        input_parser.feed(available_page)
        hidden_input = input_parser.getInputValues()
        print "Final Input: ",hidden_input
        input_parser.close()

        print """

---------- Successfully Get Available Slot. Processing ----------

        """

        # Choose a room
    
        room_number = chooseRoom(available_room)
        
        # Translate the room info
        room_raw = roomRaw(room_number)
        
        # POST reservation info
        final_input = urllib.urlencode({
            "utf8":"\u2713",
            #'authenticity_token':hidden_input[1],
            'reservation[room_id]':room_number,
            'reservation[title]':title,
            'reservation[cc]':email,
            'reservation[user_id]':hidden_input[1],
            'reservation[start_dt]':hidden_input[2],
            'reservation[end_dt]':hidden_input[3]
    
    
        })

        final_url="https://rooms.library.nyu.edu/reservations/"
        final_submit = urllib2.urlopen(final_url, final_input)
        final_page = final_submit.read()
        print final_page
        
    except UnboundLocalError:
        report.append("This account cannot book more rooms\n")
        print """

---------- This account cannot book more rooms ----------

        """
        
    # Comment this handling code to check what wrong
    # except:
#         report.append("This account's reservation is failed for some reason\n")
#         print """
#
# ---------- This account's reservation is failed ----------
#
#         """
    else:
        report.append("Successfully reserve a study room at "+time+"pm on "+new_date+"\nThe room id is "+room_raw+"\n")
        print """

---------- This Account's Reservation Is Completed ----------

        """
        
    
# ----------------Begin----------------

print """

---------- Program Start...This program may take 1 minute for every account to reserve a study room ----------

"""
    
# Add a parameter in format YYYY-MM-DD to set a reservation date
# The default date is the day after tomorrow
reserveRoom(login_1, another_email, optional_title, '8')




print """

---------- Reservation Report ----------

"""
for item in report:
    print item 
