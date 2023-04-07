import csv

def parseBleeperParking():
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
    
    with open('bleeperPermittedParking.csv', 'w') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerows(newStations)
    

def parseBleeperData():
  parsedDown = [["id","date","lat","long"]]
  with open('bleeperjune21.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in list(reader):
      parsedDown.append([row["id"],row["harvest_time"][:-5]+"00:00",row["latitude"],row["longitude"]])

  
  with open('bleeperjune21parsed.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(parsedDown)