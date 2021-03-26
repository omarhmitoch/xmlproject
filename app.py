from flask import Flask , render_template , request
import urllib.request
from bs4 import BeautifulSoup as bs
from xml.dom import minidom
from lxml import etree , html
import lxml.html as lh
from lxml.etree import parse, XSLT
import xml.etree.ElementTree as ET 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


# array of Moroccan kings through 12 generation 
Kings = ['Moulay Ali Cherif' , 'Ismail','Abdallah II','Mohammed III','Hisham','Abd al-Rahman ibn Hicham','Mohammed IV','Hassan I','Youssef','Mohammed V  ','Hassan II ','Mohammed VI']
# get route
@app.route("/get")
def getHtmlPage():
    link = request.args.get('link')
    # get html code from wikipedia
    page = urllib.request.urlopen(link)
    soup = bs(page)
    
    # search for image with a monarch 'alt' attribute
    imgs = soup.body.findAll('img',alt="Monarch")[0]
    title = soup.body.find('h1',id="firstHeading")
    # getting the tree within the parent table > retrieving all table rows
    tables_data = imgs.parent.parent.parent.parent
    trs = tables_data.find_all("tr")

        # loop through every row(generation) >> get the name of every generation member
    st = ""
    for tr in trs:
        tds = tr.find_all("td")
        for td in tds:
                if (td.find("a") == None) & (len(td.text) > 0):
                    st= st + td.text +","
                if (td.find("a") != None) & (len(td.text) > 0):
                    st= st + td.text + ","
        st= st + "*"
        # store every generation in an array
        tab = st.split("****")

        generation_id_count = 0
        # create xml file root element 'Familytree' that contains all generation from single family tree
        root = ET.Element('familytree')
        root.set("familyName",str(title.text))
        mydict = {}

        for x in tab:
            gen = x.split(",") #split every generation from the first array to store every generation in a single array within the family tree array
            gen.pop()
            generation = ET.SubElement(root, 'generation') # create xml element 'generation' that's going to store every generation members data
            generation.set('id', str(generation_id_count)) # every generation has and id that distinguish it from other gens
            ref_count = 1
               
            check = False
            for y in gen: #loop through every member of a generation
                name = y
                # Had to add this part of code to remove some extra text added to members name (wikipedia's mistake)
                if "spouse" in name.lstrip():
                    spouseword = y[y.find("spouse") : len(y)]
                    newWord=y.replace(spouseword, "").lstrip()
                else:
                    newWord = name.lstrip()
                if(len(newWord)<5):
                        continue
                if "°" in newWord:
                    tempword = newWord[newWord.find("°")-1 : newWord.find("°")+1]
                    newWord=newWord.replace(tempword, "").lstrip()
                
                # create xml 'personne' element that contains every memeber name
                ref = str(generation_id_count) + str(ref_count) # id of every memeber is {generationID + counter from 1 to n / n = every generation members count}
                personne = ET.SubElement(generation, 'personne') 
                personne.set('ref', str(ref))
                #check if a member of a generation is the king to attach a special attribute 'estroi' to it
                if newWord in Kings:
                    if check == False:
                        personne.set('estroi', str(True))
                        mydict[generation_id_count] = ref
                        check = True
                    else:
                        personne.set('estroi', str(False))
                else:
                    personne.set('estroi', str(False))
                # add the member name value to the 'personne' element
                nomcomplet = ET.SubElement(personne, "nomcomplet")
                nomcomplet.text = newWord.lstrip()

                ref_count = ref_count + 1
            # add reference to the parent of every generation with 'link' attribute // 'link' value refers to the last generation king {parent of the actual one here}
            if(generation_id_count>0):
                parent = ET.SubElement(generation, 'parent')
                parent.set('link', str(mydict[generation_id_count -1]))
            else:
                parent = ET.SubElement(generation, 'parent')
                parent.set('link', "")
            #increment the generation count 
            generation_id_count = generation_id_count + 1
            
        # after generatin our xml file , we pass it through an xml parser
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open("./dataFiles/tree_Database.xml", "w", encoding="utf-8") as f:
            f.write(xmlstr)
        


        xslDoc = etree.parse("./dataFiles/index.xsl")
        xsltTransformer = etree.XSLT(xslDoc)
        
        xmlDoc = etree.parse("./dataFiles/tree_Database.xml")
        outputDoc = xsltTransformer(xmlDoc)
        root = lh.tostring(outputDoc) #convert the generated HTML to a string
        soup = bs(root)                #make BeautifulSoup
        prettyHTML = soup.prettify()  

    return str(prettyHTML)




if __name__ == '__main__':
    app.run(debug=True)