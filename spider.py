from bs4 import BeautifulSoup
import requests
import re
import os


def chaucer_spider(outdir="/data/html/"):
    # Crawls the www.librarius.com site and downloads the various HTML files
    # containing the parallel text for the Canterbury Tales.

    # URL for top-level table of contents
    toc_url = 'http://www.librarius.com/cantales/contensm.htm'
    print("Beginning crawl...")
    print("Retrieving table of contents...")

    # Grab TOC
    toc_req = requests.get(toc_url)
    toc_dump = toc_req.text
    toc_soup = BeautifulSoup(toc_dump, 'lxml')

    # Find all of the links within the TOC, and filter out only the relevant ones
    # (those that lead to deeper tables of contents containing links to the
    # parallel translations). Add those to a list.
    section_list = []
    re_toc = re.compile('canttran')

    for url in toc_soup.findAll('a'):
        base = url.get('href')
        mo = re_toc.search(str(base))
        if mo is not None:
            link = "http://www.librarius.com/cantales/" + str(base)
            print("Found section " + link)
            section_list.append(link)

    # Now look deeper into each section. The problem here is that these links
    # don't themselves lead to a list of links, but to a frame page, where one
    # of those frames is the page containing the list we need. So we need to find
    # that page for each section.
    section_toc_list = []
    re_frame = re.compile('tr\.htm')

    for section in section_list:
        section_req = requests.get(section)
        section_dump = section_req.text
        section_soup = BeautifulSoup(section_dump, 'lxml')

        for frame in section_soup.findAll('frame'):
            file = frame.get('src')
            mo = re_frame.search(str(file))
            if mo is not None:
                link = "http://www.librarius.com/canttran/" + str(file)
                print("Found section TOC " + link)
                section_toc_list.append(link)

    # Now, at last, parse the TOC for each section and grab all of the
    # HTML files containing the parallel text for that section, and save
    # them to disk.
    re_linenum = re.compile('\d+-\d+')
    re_trim = re.compile('(.*/)')

    for stoc in section_toc_list:
        stoc_req = requests.get(stoc)
        stoc_dump = stoc_req.text
        stoc_soup = BeautifulSoup(stoc_dump, 'lxml')

        # Trim the URL to get the parent directory, so we can append the HTML
        # file names we find to it.
        trim_mo = re_trim.search(stoc)
        base_url = trim_mo.group(1)
        re_prefix = re.compile('(.*?)\d+')

        for url in stoc_soup.findAll('a'):
            base = url.get('href')
            mo = re_linenum.search(str(base))
            if mo is not None:
                link = str(base_url) + str(base)
                print("Found page " + link)
                page_req = requests.get(link)
                pref_mo = re_prefix.search(str(base))
                prefix = pref_mo.group(1)
                
                engs = [[],[],[]]
                which = 2
                soup = BeautifulSoup(page_req.text)
                for line in soup.select('tr td tr td + td'):
                    if re.search('width="85%"',str(line)):
                        which = (which + 1) % 2
                    l_text = line.get_text().strip()
                    if l_text and not re.search('^\d+$',l_text):
                        engs[which].append(l_text)
                # Save file to disk
                outfile = str(os.getcwd()) + str(outdir) + str(prefix) + "/" + str(base)
                os.makedirs(os.path.dirname(outfile), exist_ok=True)
                with open(outfile, 'w') as f:
                    for l1, l2 in zip(engs[0],engs[1]):
                        print(l1,l2,sep='\n',file=f)

    return


chaucer_spider()
