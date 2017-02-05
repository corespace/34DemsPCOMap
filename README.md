# 34DemsPCOMap

## Data processing

Map data is in KML format: https://en.wikipedia.org/wiki/Keyhole_Markup_Language

Example entry:

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

Merge this with data from pco.csv.
Calculate "middle" point of polygon. Ex code: https://github.com/manuelbieh/Geolib#geolibgetcenterarray-coords

Throw all this into elasticsearch. https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-queries.html

Then on query, can use geo_shape to find person's precinct + geo_distance to find all within x distance.
