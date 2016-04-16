import sys
import csv
import json
import urllib
import os

from pyquery import PyQuery as pq

nav = pq("""<ul>        <li><a href="/elections/2016/primaries/democrat/alabama/">Alabama</a></li>
<li><a href="/elections/2016/primaries/democrat/alaska/">Alaska</a></li>
<li><a href="/elections/2016/primaries/democrat/arizona/">Arizona</a></li>
<li><a href="/elections/2016/primaries/democrat/arkansas/">Arkansas</a></li>
<li><a href="/elections/2016/primaries/democrat/california/">California</a></li>
<li><a href="/elections/2016/primaries/democrat/colorado/">Colorado</a></li>
<li><a href="/elections/2016/primaries/democrat/connecticut/">Connecticut</a></li>
<li><a href="/elections/2016/primaries/democrat/delaware/">Delaware</a></li>
<li><a href="/elections/2016/primaries/democrat/washington-dc/">District of Columbia</a></li>
<li><a href="/elections/2016/primaries/democrat/florida/">Florida</a></li>
<li><a href="/elections/2016/primaries/democrat/georgia/">Georgia</a></li>
<li><a href="/elections/2016/primaries/democrat/guam/">Guam</a></li>
<li><a href="/elections/2016/primaries/democrat/hawaii/">Hawaii</a></li>
<li><a href="/elections/2016/primaries/democrat/idaho/">Idaho</a></li>
<li><a href="/elections/2016/primaries/democrat/illinois/">Illinois</a></li>
<li><a href="/elections/2016/primaries/democrat/indiana/">Indiana</a></li>
<li><a href="/elections/2016/primaries/democrat/iowa/">Iowa</a></li>
<li><a href="/elections/2016/primaries/democrat/kansas/">Kansas</a></li>
<li><a href="/elections/2016/primaries/democrat/kentucky/">Kentucky</a></li>
<li><a href="/elections/2016/primaries/democrat/louisiana/">Louisiana</a></li>
<li><a href="/elections/2016/primaries/democrat/maine/">Maine</a></li>
<li><a href="/elections/2016/primaries/democrat/maryland/">Maryland</a></li>
<li><a href="/elections/2016/primaries/democrat/massachusetts/">Massachusetts</a></li>
<li><a href="/elections/2016/primaries/democrat/michigan/">Michigan</a></li>
<li><a href="/elections/2016/primaries/democrat/minnesota/">Minnesota</a></li>
<li><a href="/elections/2016/primaries/democrat/mississippi/">Mississippi</a></li>
<li><a href="/elections/2016/primaries/democrat/missouri/">Missouri</a></li>
<li><a href="/elections/2016/primaries/democrat/montana/">Montana</a></li>
<li><a href="/elections/2016/primaries/democrat/nebraska/">Nebraska</a></li>
<li><a href="/elections/2016/primaries/democrat/nevada/">Nevada</a></li>
<li><a href="/elections/2016/primaries/democrat/new-hampshire/">New Hampshire</a></li>
<li><a href="/elections/2016/primaries/democrat/new-jersey/">New Jersey</a></li>
<li><a href="/elections/2016/primaries/democrat/new-mexico/">New Mexico</a></li>
<li><a href="/elections/2016/primaries/democrat/new-york/">New York</a></li>
<li><a href="/elections/2016/primaries/democrat/north-carolina/">North Carolina</a></li>
<li><a href="/elections/2016/primaries/democrat/north-dakota/">North Dakota</a></li>
<li><a href="/elections/2016/primaries/democrat/ohio/">Ohio</a></li>
<li><a href="/elections/2016/primaries/democrat/oklahoma/">Oklahoma</a></li>
<li><a href="/elections/2016/primaries/democrat/oregon/">Oregon</a></li>
<li><a href="/elections/2016/primaries/democrat/pennsylvania/">Pennsylvania</a></li>
<li><a href="/elections/2016/primaries/democrat/puerto-rico/">Puerto Rico</a></li>
<li><a href="/elections/2016/primaries/democrat/rhode-island/">Rhode Island</a></li>
<li><a href="/elections/2016/primaries/democrat/south-carolina/">South Carolina</a></li>
<li><a href="/elections/2016/primaries/democrat/south-dakota/">South Dakota</a></li>
<li><a href="/elections/2016/primaries/democrat/tennessee/">Tennessee</a></li>
<li><a href="/elections/2016/primaries/democrat/texas/">Texas</a></li>
<li><a href="/elections/2016/primaries/democrat/utah/">Utah</a></li>
<li><a href="/elections/2016/primaries/democrat/vermont/">Vermont</a></li>
<li><a href="/elections/2016/primaries/democrat/virginia/">Virginia</a></li>
<li><a href="/elections/2016/primaries/democrat/washington/">Washington</a></li>
<li><a href="/elections/2016/primaries/democrat/west-virginia/">West Virginia</a></li>
<li><a href="/elections/2016/primaries/democrat/wisconsin/">Wisconsin</a></li>
<li><a href="/elections/2016/primaries/democrat/wyoming/">Wyoming</a></li>
        </ul>""")

for el in nav.find('a'):
    url = "http://www.cbsnews.com" + pq(el).attr('href')
    data = urllib.urlopen(url).read()
    dom = pq(data)
    for el in dom.find("*[data-electionfeed]"):
        url = json.loads(pq(el).attr('data-electionfeed'))['src']
        basename = os.path.basename(url)
        url = "http://www.cbsnews.com" + url
        urllib.urlretrieve(url, 'cbsrip/%s'%basename)

"""
for row in csv.DictReader(open('usa-states.csv')):
    state = row['StateCode']
    #url = "http://data.cnn.com/ELECTION/2016primary/%s/county/D.json"%state
    url = "http://www.cbsnews.com/election-results-data/2016-Primaries/xmlData/County_%s_P_D_0.xml"%state
    basename = os.path.basename(url)
    #print >>sys.stderr, url, basename
    try:
        data = urllib.urlretrieve(url, 'cbsrip/%s'%basename)
    except Exception, e:
        print >>sys.stderr, "Failed to read %s"%state
        continue
    print >>sys.stderr, "Loaded %s"%state
"""
