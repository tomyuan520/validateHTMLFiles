from structure import stack
import re
import urllib.request as request

def online_check(url): #getting from internet
    response = request.urlopen(url).read()   #read out as binary
    html = response.decode('utf-8')   #encoding as utf-8 according to the website.
    return html

def readHTML(HTML):
    out_put = ''
    try:
        f = open(HTML,"r")
    except FileNotFoundError:
        print("There is no ", HTML)
    for line in f:
        if str(line).startswith('<!DOCTYPE'):   #ignore the !doctype
            continue
        if not str(line).startswith('<') and not str(line).endswith('>'):
            continue
        line = re.sub(re.compile('>.*?<'), '>   <',line)    #using regular expressions to find out only the tag names.
        line = line.replace('\n','   ')
        out_put += line
    if out_put.endswith("   "): #if there is still space at the end of the file, remove it. 
        out_put = out_put[:-3]
    return out_put

def need(line): #for our open tags, both !DOCTYPE and /(close tags) are not needed.
    if line[1] == '!':
        return False
    if line[-2] == '/': #handling the single tags like <br/>
        return False
    return True

def tagname(tag):   #exact the available tags' names.
    return tag[1:-1].split(' ')[0]

def validateHTML(html):
    opentags = stack()
    closetags = stack() #using two stacks to store the possible open and close tags. and compare each other.
    linesplit = html.split('   ')   #spliting using the spaces we set up
    for i in linesplit:
        if need(i):
            tag = tagname(i)
            if tag[0] != '/':
                opentags.push(tag)
            else:
                if opentags.peek() == tag[1:]:
                    opentags.pop()
                else:
                    i = 0
                    count = 0
                    closetags.push(tag)
                    while i < len(opentags.data):
                        if opentags.data[i] == tag[1:] and count == 0:
                            del opentags.data[i]
                            closetags.pop()
                            count += 1
                        i += 1
    if opentags.is_empty() and closetags.is_empty():    #only if all open tags are connected with the close tags, the html is valid.
        return True
    else:
        if not opentags.is_empty():  #if not, find out what the error tag is.
            print ('The error is at: ' + '<' + opentags.pop() + '>' + ';')
        if not closetags.is_empty():
            print ('The error is at: ' + '<' + closetags.pop() + '>' + ';')
        return False
if __name__ == '__main__':
    #self test
    test = readHTML(input('Input the HTML file: ',))
    print(validateHTML(test))
    
    #self test bonus
    url = "http://redive.estertion.win"
    print(validateHTML(online_check(url)))
    
    #Test 1
    htmlStr = readHTML("validHTML.html")
    assert len(htmlStr) > 0
    assert htmlStr.startswith("<html") or htmlStr.startswith("<>")
    result = validateHTML(htmlStr)
    assert result
    print("Test 1 resulted in", "valid" if result else "invalid", "HTML")


    #Test 2
    htmlStr = readHTML("invalidHTML.html")
    assert len(htmlStr) > 0
    assert htmlStr.endswith("</html>") or htmlStr.endswith("</>")
    result = validateHTML(htmlStr)
    assert not result
    print("Test 2 resulted in", "valid" if result else "invalid", "HTML")


    #Test 3
    htmlStr = readHTML("test1.html")
    assert len(htmlStr) > 0
    result = validateHTML(htmlStr)
    assert result
    print("Test 3 resulted in", "valid" if result else "invalid", "HTML")