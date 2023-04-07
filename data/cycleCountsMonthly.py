import csv

def monthlyCounts2022():
  months = dict((m,0) for m in range(1,13))
  with open('cycle-counts-2022.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in list(reader)[1:]:
      month = int(row[0].split("/")[1])
      months[month]+=sum([int(x) if len(x)>0 else 0 for x in row[1:]])
  return months
  #{1: 464192, 2: 398058, 3: 573797, 4: 566137, 5: 626104, 6: 597648, 7: 649246, 8: 639390, 9: 528660, 10: 505762, 11: 483226, 12: 299800}

def monthlyCounts2021():
  # to account for formatting changes from 2021 to 2022
  months = dict((m,0) for m in range(1,13))
  with open('cycle-counts-2021.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in list(reader)[1:]:
      month = int(row[0].split("-")[1])
      months[month]+=sum([int(x) if len(x)>0 else 0 for x in row[1:]])
  return months
  #{1: 245177, 2: 268598, 3: 390079, 4: 453919, 5: 681103, 6: 769834, 7: 746836, 8: 619677, 9: 639530, 10: 567974, 11: 527445, 12: 382158}

def cycleCounts():
  return {2021:monthlyCounts2021(),2022:monthlyCounts2022()}


# accoring to the data, the month with the most ridership in 2021/2022 was June 2021 (769834 total recordered instances from cycle counts)
