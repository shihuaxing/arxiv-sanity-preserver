import os
import time
import pickle
import shutil
import random
from  urllib.request import urlopen
import asyncio
import aiohttp
from utils import Config
timeout_secs = 20 # after this many seconds we give up on a paper
#if not os.path.exists(Config.pdf_dir): os.makedirs(Config.pdf_dir)
#have = set(os.listdir(Config.pdf_dir)) # get list of all pdfs we already have
pdf_dir="/BackupDisk2/arxiv-sanity/arxiv-sanity-preserver/test_asyn_download"
if not os.path.exists(pdf_dir): os.makedirs(pdf_dir)
#have = set(os.listdir(Config.pdf_dir)) # get list of all pdfs we already have
have = set() # get list of all pdfs we already have


numok = 0
numtot = 0
db = pickle.load(open(Config.db_path, 'rb'))

async def fetch(url, timeout_secs,fname,semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            aiohttp.Timeout(timeout_secs)
            async with session.get(url) as response:
                response = await response.read()
    with open(fname, 'wb') as fp:
        #await shutil.copyfileobj(response, fp)
        fp.write(response)
    asyncio.sleep(0.05 + random.uniform(0,0.1))
tasks = []
def fetch_pdf():
  global numok,numtot
  semaphore = asyncio.Semaphore(30) # 限制并发量为500
  x=0
  for pid,j in db.items():
    x+=1
    pdfs = [x['href'] for x in j['links'] if x['type'] == 'application/pdf']
    assert len(pdfs) == 1
    pdf_url = pdfs[0] + '.pdf'
    pdf_url = pdf_url.replace("http://arxiv.org","http://cn.arxiv.org")
    basename = pdf_url.split('/')[-1]
    #fname = os.path.join(Config.pdf_dir, basename)
    fname = os.path.join(pdf_dir, basename)

    # try retrieve the pdf
    numtot += 1
    try:
        if not basename in have:
            print('fetching %s into %s' % (pdf_url, fname))
            task = asyncio.ensure_future(fetch(pdf_url,timeout_secs,fname,semaphore))
            tasks.append(task)
            #time.sleep(0.05 + random.uniform(0,0.1))
        else:
            print('%s exists, skipping' % (fname, ))
        numok+=1
    except Exception as e:
        print('error downloading: ', pdf_url)
        print(e)
    if x>3:
        break
  
  print('%d/%d of %d downloaded ok.' % (numok, numtot, len(db)))
loop = asyncio.get_event_loop()
fetch_pdf()
loop.run_until_complete(asyncio.wait(tasks))
print('final number of papers downloaded okay: %d/%d' % (numok, len(db)))

