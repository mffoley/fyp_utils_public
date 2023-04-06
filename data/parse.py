import csv
import json
import requests

def parseBleeperStations():
    newStations = []
    with open('bleeperStations.csv', 'r') as csvfile:
      reader = csv.reader(csvfile)
      l=0
      for row in reader:
        if l==0:
          newStations.append(["id","lat","long"])
        else:
          newStations.append([row[0]]+row[7:9])
        l+=1
    
    with open('bleeperStationsLoc.csv', 'w') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerows(newStations)
    
def parseDublinBikeStations():
    newStations = []
    with open('dublinBikeStations.csv', 'r') as csvfile:
      reader = csv.reader(csvfile)
      l=0
      for row in reader:
        if l==0:
          newStations.append(["id","lat","long"])
        else:
          newStations.append([row[0]]+row[3:])
        l+=1
    
    with open('dublinBikeStationsLoc.csv', 'w') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerows(newStations)


def chooseMonth():
  months = dict((m,0) for m in range(1,13))
  with open('cycle-counts-2022.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in list(reader)[1:]:
      month = int(row[0].split("/")[1])
      months[month]+=sum([int(x) if len(x)>0 else 0 for x in row[1:]])
  return months
  #{1: 464192, 2: 398058, 3: 573797, 4: 566137, 5: 626104, 6: 597648, 7: 649246, 8: 639390, 9: 528660, 10: 505762, 11: 483226, 12: 299800}

def chooseMonth2021():
  # to account for formatting changes from 2021 to 2022
  months = dict((m,0) for m in range(1,13))
  with open('cycle-counts-2021.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in list(reader)[1:]:
      month = int(row[0].split("-")[1])
      months[month]+=sum([int(x) if len(x)>0 else 0 for x in row[1:]])
  print( months)
  #results: {1: 245177, 2: 268598, 3: 390079, 4: 453919, 5: 681103, 6: 769834, 7: 746836, 8: 619677, 9: 639530, 10: 567974, 11: 527445, 12: 382158}

# accoring to the data, the month with the most ridership in 2021/2022 was June 2021 (769834 total recordered instances from cycle counts)


# Some instances where the stations are closed, but do not need to be removed since we will be calculating the departure numbers
def combineDBStationData():
  parsedDown = [["id","date","time","lat","long","standsAvail","bikesAvail"]]
  with open('dublinBikesQ2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in list(reader)[1:]:
      month = int(row[1].split("-")[1])
      if month==6:
        parsedDown.append([row[0]]+row[1].split(" ")+row[9:]+row[5:7])

  with open('dublinBikesJuneLess.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(parsedDown)



def hourlyDBData():
  #bikeData = {id: {date: {hour: []} }, lat:, long:}}
  dataReformatted = {}
  with open('dublinBikesJuneLess.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in list(reader)[1:]:
      id = row[0]
      if id not in dataReformatted:
        dataReformatted[id] = {"lat":row[3],"long":row[4]}
      date = row[1]
      if row[1] not in dataReformatted[id]:
        dataReformatted[id][row[1]] = {}
      hour = int(row[2].split(":")[0])
      if hour not in dataReformatted[id][date]:
        dataReformatted[id][date][hour] = []
      dataReformatted[id][date][hour].append(int(row[-1]))

  parsedDown = [["id","lat","long","date","departures"]]
  for id in dataReformatted:
    for date in dataReformatted[id].keys()-["lat","long"]:
      for hour in dataReformatted[id][date].keys():
        parsedDown.append([id,dataReformatted[id]["lat"],dataReformatted[id]["long"],date + " "+'{:0>2}'.format(hour)+":00",
                           sum([((j-i)*-1 if j-i < 0 else 0) for i, j in zip(dataReformatted[id][date][hour][:-1], dataReformatted[id][date][hour][1:])])])

  with open('dublinBikesJuneHourly.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(parsedDown)

#summing up and mapping the in/out data for each cycle station
#locations missing!!! talk about in methods (only 5 out of 10 stations have coords)
def hourlyCycleCount():
  locs = {}
  with open("locationsForCycleCounts.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in list(reader)[1:]:
      locs[row[0]] = [row[1],row[2]]
  
  dataUnzip = [["Date", "Station","count", "Lat", "Long"]]
  with open('cycle-counts-2021.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in list(reader):
      for key in row.keys():
        if key in locs.keys() and row["Date & Time"].split("-")[1]=="06":
          dataUnzip.append([reformatDates(row["Date & Time"]),key,row[key],locs[key][0],locs[key][1]])
  
  with open('cycle-counts-June2021Unzipped.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(dataUnzip)

def reformatDates(dateInput):
  date,time = dateInput.split(" ")
  return "-".join(date.split("-")[::-1])+" "+time

def parseBleeperData():
  parsedDown = [["id","date","lat","long"]]
  with open('bleeperjune21.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in list(reader):
      parsedDown.append([row["id"],row["harvest_time"][:-5]+"00:00",row["latitude"],row["longitude"]])

  
  with open('bleeperjune21parsed.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(parsedDown)


#get route locs based on ids from geojson for votes
def getRouteLocs():
  routes = json.loads(open("gj_br.geojson").read())
  routeLocs = []
  for route in routes["features"]:
    center = (len(route["geometry"]["coordinates"])//2)
    routeLocs.append({"id": route["id"], "long": route["geometry"]["coordinates"][center][0], "lat": route["geometry"]["coordinates"][center][1] })
  url = "http://finalyearproject-b132e.web.app/api/votes"
  req = requests.post(url, json = routeLocs)
  print(req)
  

def main():
  #parseBleeperStations()
  #parseDublinBikeStations()
  print(chooseMonth())
  #chooseMonth2021()
  #combineDBStationData()
  #hourlyDBData()
  #hourlyCycleCount()
  #parseBleeperData()
  #getRouteLocs()


if __name__ == "__main__":
  main()

