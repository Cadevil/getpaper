import urllib2
import io
import random
import urllib
from bs4 import BeautifulSoup
import re
import os
import mylog
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def getHtml(url):
    user_agent = [
        'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
        'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
        'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'       
    ]
    header = {"User-Agent":random.choice(user_agent)}
    request = urllib2.Request(url,headers = header)
    html = urllib2.urlopen(request).read()
	
    soup = BeautifulSoup(html)
    return soup


# 1. ��ȡ��ѯ������б�
# 2. ��ȡ������ѯ�������Ϣ��������ѯ����ڵ����ݺ������µı��⣬����ժҪ�����ߣ�pdf������
# 3. ��ȡ���׵ı���
# 4. pdf�������ӣ��������������Ƿ������������
# 5. ���������أ���ƴ�����ӣ�http://link.springer.com
# 6. ��������


# ��ȡ��������ҳ���pdf�б�
def getallresults(url,downloadpath):
	try:
		soup = getHtml(url)
		pagestag = soup.find("span",class_="number-of-pages")
		pagesnum = int(pagestag.contents[0])
		
		uri = url.split("?")
		
		for i in range(1, pagesnum + 1):
			url = uri[0] + "/page/" + str(i) +"?" + uri[1]
			print url
			getsinglepageresults(getHtml(url),downloadpath, i)
			
		return 1
	except Exception,ex:
		tp,val,td = sys.exc_info()
		mylog.logerexception(tp, val, td)
		return 0		


# ��ȡ����ҳ���pdf�б�����������������ҳ
def getsinglepageresults(soup,downloadpath, pagenum):

    result = soup.find("ol", class_="content-item-list")
    if len(result) > 0:
		results = result.find_all("li")
		
		if len(results) > 0:
			for singleartlce in results:
				articlename = str(pagenum) + "-" + getarticlename(singleartlce)
				#print articlename
								
				articleurl = getarticleurl(singleartlce, articlename)
				#print articleurl
								
				downloadpdf(articleurl, articlename, downloadpath)
				time.sleep(random.randint(1, 2))
	

# ����pdf
def downloadpdf(articleurl,articlename,downloadpath):
	try:
		
		oldname = re.findall("10.1007%(.*?)\.pdf", articleurl)
		path = ""
		if len(oldname) > 0:
			path = downloadpath + articlename + "..." + oldname[0].encode("utf8") + ".pdf"
		else:
			path = downloadpath + articlename + ".pdf"
		
		urllib.URLopener.version = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0"
		#urllib.URLopener.addheader
		urllib.urlretrieve(articleurl,path)
		
		return 1
	except Exception,ex:
		tp,val,td = sys.exc_info()
		mylog.logerexception(tp, val, td)
		return 0


# ��ȡ������Ŀ
def getarticlename(singleartlce):

    articlename = ""

    atag = singleartlce.find_all("a",class_="title" )
	# �����Ŀ�����������йؼ��ʣ�����
    queries = [""]

    if len(atag) > 0 :
		vale = atag[0].contents
		if len(vale) > 0:
			name = vale[0].encode("utf8")
			articlename = name.replace(":","��")
			articlename = articlename.replace("?","��")
			
			for query in queries:
				if articlename.find(query) > -1:
					articlename = "��" + articlename

    return articlename

# ��ȡpdf��������
def getarticleurl(singleartlce, articlename):
    articleurl = ""
	
    span = singleartlce.find_all("span",class_="action")

    if len(span) > 0:
		als = span[0].find_all("a")
		if als is not None:
			url = als[0]["href"]
			ispdfurl = re.findall(".*?\.pdf", url)
			if ispdfurl:
				articleurl = "http://link.springer.com" + url
			else:
				mylog.logerinfor("can't download : " + articlename)

    return articleurl

#def getauther(soup):



if __name__ == "__main__":
		
	# springer�Ĳ�ѯ���
	url = ""
	# ��������ļ��ľ���·��
	downloadpath = ""
	getallresults(url, downloadpath)