import json
import requests

def postRouteLocs():
  routes = json.loads(open("gj_br.geojson").read())
  # geojson bike routes
  routeLocs = []
  for route in routes["features"]:
    center = (len(route["geometry"]["coordinates"])//2)
    routeLocs.append({"id": route["id"], "long": route["geometry"]["coordinates"][center][0], "lat": route["geometry"]["coordinates"][center][1] })
  url = "http://finalyearproject-b132e.web.app/api/votes"
  req = requests.post(url, json = routeLocs)
  print(req)
  