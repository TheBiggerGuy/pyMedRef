import urllib
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)


def gsearch(paper_title):
    paper_title = paper_title + " site:ncbi.nlm.nih.gov/pubmed/"
    query = urllib.urlencode(
        {
            'q' : paper_title,
            'v' : "1.0"
        }
    )
    url = 'http://ajax.googleapis.com/ajax/services/search/web?{query}'.format(query=query)
    search_results = urllib.urlopen(url)
    jsond = json.loads(search_results.read())
    results = jsond['responseData']['results']

    return results

# *****************************************************
while True:
    try:
        userinput=raw_input("please type title: ")
        userinput=str(userinput)

        if userinput=='quit':
            break
        
        results = gsearch(userinput)

        url_result=results[0]['url']


        import urllib2
        request = urllib2.Request(url_result)
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux x86_64; es-MX; rv:1.9.2.12) Gecko/20101027 Ubuntu/10.04 (lucid) Firefox/3.6.12')
        page_source=urllib2.urlopen(request).readlines()

        for line in page_source:
            if line.find('<div class="rprt_all"><div class="rprt abstract"><p class="citation">') != -1:
                citation = line
                break

        ab_citation = []
        

        for counter in range(0, len(citation)):
            
            if citation[counter] == '>':
                index = citation.find('<',counter)
                temp=citation[counter+1:index]
                temp=temp.replace(', ',"")
                temp=temp.replace('; ',"")
                temp=temp.replace('\n',"")
                if temp == ".":
                    break
                elif temp != '':
                    ab_citation.append(temp)
            

        authors=""
        if len(ab_citation[3:]) > 1:

            for item in ab_citation[3:-1]:
                authors+= ', ' + item
            authors = authors[2:]
            authors+= ' & ' + ab_citation[len(ab_citation)-1]

        else:
            authors=ab_citation[3]

        print '{authors} ({year}). {paper_title}. {journal_title} {volume_no}, {page_number}.'.format(
            authors=authors,
            year=ab_citation[1].split(";")[0][1:5],
            paper_title=ab_citation[2][:-1],
            journal_title = ab_citation[0][:-1],
            volume_no=ab_citation[1].split(';')[1].split('(')[0],
            page_number=ab_citation[1].split(':')[1][:-1]
            )

        print
    except Exception as exception:
        print 'error \n'  
    
    #http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=aids
    #http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=21165963
