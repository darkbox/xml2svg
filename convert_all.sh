#!/bin/bash
echo "Android XML to SVG"
for xml_file in *.xml 
do
    echo "Converting: $xml_file"
    python xml2svg.py $xml_file
done
echo "DONE!"
