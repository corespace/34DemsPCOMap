# 34DemsPCOMap

## API Design

### GET by precinct id

GET /precincts/{id}

Should return entire json doc generated above.

### GET precinct by latlong

GET /precincts?lat={latitude}&long={longitude}

Will return the precinct that includes the given latlongs or 404 if there is no such precinct.

### GET nearest precints by latlong

GET /precincts?lat={latitude}&long={longitude}&dist={distance}

Will return the precincts within {distance} of the given latlongs or 404 if there is no such precinct. TODO: Should provide ability to exclude the precinct if it would have been returned by the previous API?


## Data processing

Map data is in KML format: https://en.wikipedia.org/wiki/Keyhole_Markup_Language

Example entry:

```xml
<Placemark>
  <name>SEA 34-1481</name>
  <Style><LineStyle><color>ff0000ff</color></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style>
  <ExtendedData><SchemaData schemaUrl="#votdst">
    <SimpleData name="votdst">1481</SimpleData>
    <SimpleData name="SUM_VOTERS">497.00000000</SimpleData>
    <SimpleData name="Shape_area">1350586.43359000000</SimpleData>
    <SimpleData name="Shape_len">5324.39152041000</SimpleData>
  </SchemaData></ExtendedData>
      <Polygon><outerBoundaryIs><LinearRing>
        <coordinates>-122.38709093827448,47.550300841307376 -122.38562974370181,47.550281741597658 -122.38433050497751,47.550264682697964 -122.38438217677493,47.548455582964863 -122.38443362581575,47.546655723492258 -122.38444828339964,47.545405547540497 -122.38444677403359,47.545342355407733 -122.38445347129016,47.544836706964844 -122.38575244690485,47.544853711329118 -122.38721482549489,47.544872749810139 -122.38720991613448,47.545342423675194 -122.38720232913239,47.546034163347294 -122.38720051620609,47.546203561607406 -122.38719498663245,47.546707645459335 -122.38718461512866,47.547066546279495 -122.38715553698052,47.548072645601728 -122.38714516618106,47.548431543700922 -122.38714342971255,47.548491604556922 -122.38711598149773,47.54943764174547 -122.38710557296302,47.549796540347849 -122.38709093827448,47.550300841307376</coordinates>
      </LinearRing></outerBoundaryIs></Polygon>
</Placemark>
```

Merge this with data from pco.csv.

Calculate "middle" point of polygon. Ex code: https://github.com/manuelbieh/Geolib#geolibgetcenterarray-coords

TODO: Some precints are defined as 'multipolygons' - figure out how to calculate the centroid for them...
* 2802
* 3290
* 315
* 339
* 2959
* 3219
* 411
* 416
* 3626
* 3380
* 709
* 2659
* 3444
* 1091
* 1097
* 1216
* 2680

Ok, it seems like elasticsearch is post-filtering, so may not be helpful. I've filtered out all non-34th in the munger, so this _should_ work, but I've only tested locally. Will deploy to lambda later.

TODO: Throw all this into elasticsearch.
https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-queries.html
https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-distance-query.html
https://www.elastic.co/guide/en/elasticsearch/reference/1.4/mapping-geo-shape-type.html

TODO: Then on query, can use geo_shape to find person's precinct + geo_distance to find all within x distance.

