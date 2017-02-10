#!/usr/bin/python

from chalice import Chalice, BadRequestError, NotFoundError
import json, os, os.path

app = Chalice(app_name='precincts')
# Ok, apparently we need to leave debug on for 400s to propagate correctly...
app.debug = True

libdir = 'chalicelib'

@app.route('/precincts/{id}', methods=['GET'], cors=True)
def getById(id):
    try:
        with open(os.path.join(libdir, id + '.json')) as jsonfile:
            return json.load(jsonfile)
    except:
        raise NotFoundError("No precinct found with id {}".format(id))

@app.route('/precincts', methods=['GET'], cors=True)
def getAll():
    files = [f for f in os.listdir(libdir) if os.path.isfile(os.path.join(libdir, f))]
    allP = {}
    for f in files:
        (ident, ext) = os.path.splitext(f)
        with open(os.path.join(libdir, f)) as jsonfile:
            allP[ident] = json.load(jsonfile)

    return allP

if __name__ == '__main__':
    print json.dumps(getAll())
    # print json.dumps(getById('1481'))
