#!/usr/bin/python

import xml.etree.ElementTree as ET
import csv, json

def convert_pco(row):
    result = {}
    for key in ['nick', 'first', 'm', 'last', 'suffix', 'status', 'approved', 'start']:
        result[key] = row[key]
    return result

def build_precinct_dict(path) :
    pcos = {}
    with open(path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pcos[int(row['p_number'])] = convert_pco(row)
    return pcos

# Method borrowed from https://github.com/brandonxiang/POI_Finder under MIT license
def area(poly):
    poly_area = 0
    # TODO: polygon holes at coordinates[1]
    points = poly['coordinates'][0]
    j = len(points) - 1
    count = len(points)

    for i in range(0, count):
        p1_x = points[i][1]
        p1_y = points[i][0]
        p2_x = points[j][1]
        p2_y = points[j][0]

        poly_area += p1_x * p2_y
        poly_area -= p1_y * p2_x
        j = i

    poly_area /= 2
    return poly_area

# Method borrowed from https://github.com/brandonxiang/POI_Finder under MIT license
def centroid(poly):
    f_total = 0
    x_total = 0
    y_total = 0
    # TODO: polygon holes at coordinates[1]
    points = poly['coordinates'][0]
    j = len(points) - 1
    count = len(points)

    for i in range(0, count):
        p1_x = points[i][1]
        p1_y = points[i][0]
        p2_x = points[j][1]
        p2_y = points[j][0]

        f_total = p1_x * p2_y - p2_x * p1_y
        x_total += (p1_x + p2_x) * f_total
        y_total += (p1_y + p2_y) * f_total
        j = i

    six_area = area(poly) * 6
    return {'type': 'Point', 'coordinates': [y_total / six_area, x_total / six_area]}

# machinations to convert the string that looks like "lat,long lat,long..."
# to [['lat','long'],['lat','long'],...]
def convert_string_to_coordinate_list(coords_str):
    latlong_list = coords_str.split(' ')
    # now this looks like ['lat,long','lat,long',...]
    coordinates = []
    for item in latlong_list:
        latlong = item.split(',')
        coordinates.append([
            float(latlong[0]),
            float(latlong[1])
        ])
    # now this looks like [[lat,long],[lat,long],...]
    assert coordinates[0] == coordinates[-1]
    return coordinates

# polygons can have holes like BEL 41-3583
def convert_polygon(polygon_item):
    coordinates = []
    for item in polygon_item:
        latlongs_text = item[0][0].text
        coordinates.append(convert_string_to_coordinate_list(latlongs_text))
    return coordinates

pcos = build_precinct_dict('../34dems/pco.csv')
path = '../34dems/votdst_area/votdst_area.kml'
tree = ET.parse(path)
folder = tree.getroot()[0][1]
for placemark in folder:
    if placemark.tag != '{http://www.opengis.net/kml/2.2}Placemark':
        continue
    name = placemark[0].text
    # style = placement[1]
    ident = int(placemark[2][0][0].text)
    # count is stored as a float for some reason.
    voter_count = int(float(placemark[2][0][1].text))
    area_val = float(placemark[2][0][2].text)
    # https://tools.ietf.org/html/rfc7946
    geometry_item = placemark[3]
    geometry = {}
    center = None
    if geometry_item.tag.endswith('Polygon'):
        geometry = {'type':'polygon', 'coordinates':convert_polygon(geometry_item)}
        center = centroid(geometry)
    elif geometry_item.tag.endswith('MultiGeometry'):
        coordinates = []
        for polygon in geometry_item:
            coordinates.append(convert_polygon(polygon))
        geometry = {'type':'multipolygon', 'coordinates':coordinates}

    precinct = {
        'id' : ident,
        'name' : name,
        'voter_count' : voter_count,
        'area' : area_val,
        'location' : geometry,
        'centroid' : center,
        'pco' : pcos.get(ident)
    }
    with open('../34dems/out/' + str(ident) + '.json', 'w') as outfile:
        json.dump(precinct, outfile, indent=2)
