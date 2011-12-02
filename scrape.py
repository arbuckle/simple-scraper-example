import urllib
import urllib2
from BeautifulSoup import BeautifulSoup


#open or create the specified file.  "a" means for appending.  "r" for read-only, "w" to overwrite file contents
file = open("results.txt", "a") 
    

#function to open a web page
def get_page(url):
    #url formatting.
    url = urllib.unquote(url)

    #this opens the url and saves a response object
    response = urllib2.urlopen(url)

    #the page source is captured from the response object
    source = response.read()

    #the function returns the source code
    return source


#function to scrape a web page
def soup_it(source):

    #BeautifulSoup is a library for scraping web pages
    soup = BeautifulSoup(source)
    
    #finding each "tr" element in the page source, which will be saved in the "data" array [tr0, tr1, tr2, tr3, ...]
    data = soup.findAll('tr')
    
    #iterating through the items in the data array to pick out the ones I want
    for row in data:
        #the try/catch catches errors in the program which occur when an element doesn't match the search criteria
        try:
            #finds the contents of a "TD" element within the "TR", where the class="firstname_lastname".
            name = row.find("td", {"class": "firstname_lastname"}).contents[0]
            #removing spaces from the beginning and end of the captured name
            name = name.strip()
            
            #finds the contents of a "TD" element within the "TR" where the class="client_address"
            address = row.find("td", {"class": "client_address"}).contents[0]
            address = address.strip()
            
            # in this case, the phone number is in a "TD" with class="client_phone", but is inside of a <span> tag.  A second line is used to capture the phone # from the span
            phone = row.find("td", {"class": "client_phone"})
            phone = phone.find("span").contents[0]
            
            #here, the captured phone number has its white space and common characters removed. (find the bug)
            phone = phone.strip()
            phone = phone.replace('-', "")
            phone = phone.replace('(', "")
            phone = phone.replace(')', "")
            
            #finally, each iteration of the loop will write the captured name, address, and phone# to the file.
            file.write(name + "\n" + address + "\n" + phone + "\n\n")
        except:
            pass
    
    
#these are function calls that drive the program itself
source = get_page("http://CatTo5k.com/target.htm")
soup_it(source)
