import sys
import re

size_multiplier = 2
fill_color = '#000000'

def convert(file):
    with open(file, 'r') as f:
        data = f.read()

        # Remove android prefixes, schema, tags, etc
        data = data.replace('android:fillColor', 'fill')
        data = data.replace('android:pathData', 'd')
        data = data.replace('android:', '')
        data = data.replace(':android', '')
        data = data.replace('vector', 'svg')
        data = data.replace('dp"', '"')
        data = data.replace('http://schemas.android.com/apk/res/android', 'http://www.w3.org/2000/svg')
        
        # ViewBox Attribute
        pattern = re.compile('viewportHeight="([0-9]+\.?[0-9]*)"')
        vHeight = int(float(pattern.search(data).group(1)))
        pattern = re.compile('viewportWidth="([0-9]+\.?[0-9]*)"')
        vWidth = int(float(pattern.search(data).group(1)))
        viewBoxAttrStr = "".join(['viewBox=\"0 0 ', str(vHeight), ' ', str(vWidth), '\"'])

        data = re.sub(r'viewportHeight="([0-9]+\.?[0-9]*)"', '', data)
        data = re.sub(r'viewportWidth="([0-9]+\.?[0-9]*)"', viewBoxAttrStr, data)

        # Width and Height Attributes
        pattern = re.compile('width="([0-9]+\.?[0-9]*)"')
        width = int(float(pattern.search(data).group(1)))
        pattern = re.compile('height="([0-9]+\.?[0-9]*)"')
        height = int(float(pattern.search(data).group(1)))

        data = re.sub(r'height="([0-9]+\.?[0-9]*[0-9]+\.?[0-9]*)"', "".join(['height=\"', str(height * size_multiplier), '\"']), data)
        data = re.sub(r'width="([0-9]+\.?[0-9]*)"', "".join(['width=\"', str(width * size_multiplier), '\"']), data)

        # Replace fill color
        data = re.sub(r'fill=\"#([0-9A-F]{8})\"', "".join(['fill="', fill_color, '"']), data)

    # print data

    with open(file.replace('xml', 'svg'), 'w') as f:
        f.write(data)

# Entry point
if sys.argv[1].lower().endswith('.xml'):
    convert(sys.argv[1])
else:
    print 'Invalid file format!'