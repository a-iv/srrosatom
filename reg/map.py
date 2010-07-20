# -*- coding: cp1251 -*-

import Image

MOVE = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
MAPS = ['che', 'irc', 'kal', 'kir', 'kry', 'len', 'msk', 'mur',  'niz', 'nov',
  'pen', 'sar', 'sta', 'sve', 'tom', 'udm', 'uly', 'vla', 'zab', #'pri',
  'chu', 'kan', 'kur', 'smo', 'ros', 'tve', 'vor', ]

def next(russia, point, prev):
    #print point, prev
    delta = (prev[0] - point[0], prev[1] - point[1])
    index = MOVE.index(delta)
    found = russia.getpixel(prev) == (255, 0, 0, 255)
    #print delta, index, found
    while True:
        index = index + 1
        if (index >= 8):
            index = 0
        check = (point[0] + MOVE[index][0], point[1] + MOVE[index][1])
        #print check, index, found, russia.getpixel(prev) == (255, 0, 0, 255)
        if check == prev:
            raise Exception()
        if not found and russia.getpixel(check) == (255, 0, 0, 255):
            found = True
        if found and russia.getpixel(check) != (255, 0, 0, 255):
            return check

def go(out, name):
    print name
    russia = Image.open('%s.png' % name)
    out.write('<area shape="poly" href="#%s" coords="' % name)
    prev = None
    point = None
    start = None
    for x in xrange(russia.size[0]):
        for y in xrange(russia.size[1]):
            if russia.getpixel((x, y)) == (255, 0, 0, 255):
                point = (x, y)
                prev = (x - 1, y)
                break
        else:
            continue
        break
    first = True
    while True:
      point, prev = next(russia, point, prev), point
      if start is None:
          start = point
      elif point == start:
          break
      check = next(russia, point, prev)
      if (check[0] - point[0], check[1] - point[1]) != (point[0] - prev[0], point[1] - prev[1]):
          if first:
              first = False
          else:
              out.write(',')
          out.write('%s,%s' % point)

    out.write('" />\n')

out = open('out.html', 'w')
out.write('''
<body>
<img border="0" usemap="#Map" src="http://srrosatom.ru/sites/default/filesfile/map.png" class="map" />
<map name="Map" id="Map">
''')
for name in MAPS:
    go(out, name)
out.write('''</map>
<div style="display: none;">
''')
for name in MAPS:
    out.write('''<ul id="%s">
<li><a href="/node/111">Organization %s-1</a></li>
<li><a href="/node/112">Organization %s-2</a></li>
<li><a href="/node/112">Organization %s-3</a></li>
<li><a href="/node/112">Organization %s-4</a></li>
</ul>
''' % (name, name, name, name, name))
out.write('''</ul>
</div>
</body>''')
out.close()
