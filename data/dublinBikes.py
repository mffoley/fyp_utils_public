import csv

def parseDublinBikeStations():
    # isolates dublin bike stations to just id and coordinates
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



# Some instances where the stations are closed, but do not need to be removed since we will be calculating the departure numbers
# Gets the number of stands and bikes available at each point in time for june, middle step for parsing that would allow for multiple ways of parsing later
def parseJuneDBData():
  parsedDown = [["id","date","time","lat","long","standsAvail","bikesAvail"]]
  with open('dublinBikesQ2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in list(reader)[1:]:
      month = int(row[1].split("-")[1])
      #month has to be cast to an int as some entries have the month as "06" while others just have "6"
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

      #generate hourly lists of the number of available bikes
      #the differences of these would give the total number of departures
      #data was sorted by time, so list order did not have to be checked

      #available bikes is used instead of available stations since there are other reasons why a station may be out of order

  parsedDown = [["id","lat","long","date","departures"]]
  for id in dataReformatted:
    for date in dataReformatted[id].keys()-["lat","long"]:
      for hour in dataReformatted[id][date].keys():
        # each row in the final data will include the id, lat, long
        # the date stays the same, but the hour is formatted to ensure it has two characters
        # departures is calculated by getting the differences between elements of the hour list using a zip 

        # zip works by creating tuples out of elements with the same index of two lists
        # if given [1,2,3] and [4,5,6], the zip would return [(1,4), (2,5), (3,6)]

        # for this, the two zipped lists are the number of bikes available excluding the last and excluding the first
        # this means the tuples, with the times representing the  departures are [(:00, :05),(:05, :10) ... (:50,:55)]
        

        parsedDown.append([id,dataReformatted[id]["lat"],dataReformatted[id]["long"],
                           date + " "+'{:0>2}'.format(hour)+":00",
                           sum([(i-j if j-i < 0 else 0) for i, j in zip(dataReformatted[id][date][hour][:-1], dataReformatted[id][date][hour][1:])])])

  with open('dublinBikesJuneHourly.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(parsedDown)
