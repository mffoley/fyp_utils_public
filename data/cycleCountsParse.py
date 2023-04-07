import csv

def reformatDateOrder(dateInput):
  date,time = dateInput.split(" ")
  return "-".join(date.split("-")[::-1])+" "+time

#summing up and mapping the in/out data for each cycle station
#locations missing!!!  only 5 out of 10 stations have coords
def hourlyCycleCount():
  locs = {}
  with open("locationsForCycleCounts.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in list(reader)[1:]:
      #For each of the locations, add the location name to the dictonary as a key with the coordinates as the value
      locs[row[0]] = [row[1],row[2]]
  
  dataUnzip = [["Date", "Station","count", "Lat", "Long"]]
  # create initial list that will be written csv with headers 
  with open('cycle-counts-2021.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in list(reader):
      for key in row.keys():
        # For each location in each row there are 3 entries, "Location", "Location IN", and "Location OUT", where the first is the sum of the other 2
        if key in locs.keys() and row["Date & Time"].split("-")[1]=="06":
          # Grab only june, and only the essential fields
          dataUnzip.append([reformatDateOrder(row["Date & Time"]),key,row[key],locs[key][0],locs[key][1]])
  
  with open('cycle-counts-June2021.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(dataUnzip)
