class ExamException(Exception):
    pass


class CSVFile:
    def __init__(self, name):
        if type(name) != str:
            raise ExamException("Il nome del file deve essere una stringa")
        self.name = name

    def validate_date(self, date):
        return (
            date
            #check the year
            and date[:4].isdigit() # we don't check if the year is out of the 1949-01/1960-12 range for flexibility
            #check the separator
            and date[4:5] == "-"
            #check the month
            and date[5:7].isdigit()
            and int(date[5:7]) in range(1, 13)
        )

    def validate_value(self, value):
        return (
            value
            #check the value
            and value.isdigit() 
            and int(value) > 0 #not accepting 0 asp per request
        )


class CSVTimeSeriesFile(CSVFile):
    def get_data(self):

        try:
            fileTest = open(self.name, "r")
            fileTest.readline()
        except Exception as e:
            raise ExamException('Errore in apertura del file: "{}"'.format(e))

        file = open(self.name, "r")

        data = []
        for line in file:
            sliced = line.split(",")
            #try/except block is required since we don't know if the data can actually be split yet
            try:
                sliced[1] = sliced[1].replace("\n", "") #clean the value
            except:
                pass #continue operation could have been used but since the alternative is a single if eval I prefer it for readability
            if self.validate_date(sliced[0]) and self.validate_value(sliced[1]):  # check if row is valid
                if data and data[-1][0] < sliced[0] or not data:  # eval of a list as bool gives false if list is empty, so short circuit logic prevents errors in that case
                    sliced[1] = int(sliced[1])
                    data.append([sliced[0], sliced[1]])  # not using .append(sliced) to ignore any erroneous additional values as per request
                    
                elif data and data[-1][0] >= sliced[0]:
                    raise ExamException("Trovato valore fuori posto o valore duplicato all'indice: {}, dopo {}".format(sliced[0], data[-1][0]))

        file.close()

        return data


def compute_increments(time_series, first_year, last_year): #not using defaults for ease of update and flexibility

    # validate params, both strings and ints for flexibility
    if isinstance(first_year, str) and first_year.isdigit():
        pass
    elif isinstance(first_year, int):
        first_year = str(first_year)
    else:
        raise ExamException("first_year non è un numero intero positivo o una stringa che ne rappresenti uno")

    if isinstance(last_year, str) and last_year.isdigit():
        pass
    elif isinstance(last_year, int):
        last_year = str(last_year)
    else:
        raise ExamException("last_year non è un numero intero positivo o una stringa che ne rappresenti uno")

    # we don't check for first < last because it will just return [] without causing any issues
    # we don't check if first and/or last are out of the 1949-01/1960-12 range for the same reason

    averages = {}
    # group the values
    for item in time_series:
        if first_year <= item[0][:4] <= last_year:
            if item[0][0:4] not in averages:
                averages[item[0][0:4]] = [] #init list if key doesn't exist yet
            averages[item[0][0:4]].append(item[1])

    # transform each set into it's avg
    for year in averages:
        averages[year] = sum(averages[year]) / len(averages[year])

    variations = {}
    # calculate variations
    if len(averages) <= 1:
        #will return an empty set whenever not enough data is found as this can only be due to input error but we don't want to raise unnecessary exceptions
        return []

    # need to use a list because dicts don't support slicing due to being unordered, equal to for year in averages
    for year in list(averages.keys())[1:]:  #[1:] skips first since every iteration works on current and previous find first valid previous year
        prev_year = int(year) - 1
        while str(prev_year) not in averages: #find previous year. Casts are needed since we know the years are saved as strings
            prev_year -= 1
            
        prev_year = str(prev_year)

        variations[prev_year + "-" + year] = averages[year] - averages[prev_year] #add new value to list creating index

    return variations
