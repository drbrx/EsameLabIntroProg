class ExamException(Exception):
    pass


class CSVFile:
    def __init__(self, name):
        if type(name) != str:
            raise ExamException("Il nome del file deve essere una stringa")
        self.name = name

    def validate_date(self, date):
        return date[:4].isdigit() and date[4:5] == "-" and date[5:7].isdigit() and int(date[5:7])

    def validate_value(self, value):
        return value.isdigit()


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
            try:
                sliced[1] = sliced[1].replace("\n", "")
            except:
                pass
            if self.validate_date(sliced[0]) and self.validate_value(
                sliced[1]
            ):  # check if row is valid
                if (
                    data and data[-1][0] < sliced[0] or not data
                ):  # eval of a list as bool gives false if list is empty
                    sliced[1] = int(sliced[1])
                    data.append([sliced[0], sliced[1]]) #not using .append(sliced) to ignore any erroneous additional values as per request
                elif data and data[-1][0] >= sliced[0]:
                    print(
                        "Trovato valore fuori posto o valore duplicato all'indice: {}".format(
                            sliced[0]
                        )
                    )
                    # raise ExamException("Trovato valore fuori posto o valore duplicato all'indice: {}".format(sliced[0]))

        file.close()

        return data


def compute_increments(time_series, first_year, last_year):

    # validate params
    if isinstance(first_year, str) and first_year.isdigit():
        pass
    elif isinstance(first_year, int):
        first_year = str(first_year)
    else:
        raise ExamException(
            "first_year non è un numero intero positivo o una stringa che ne rappresenti uno"
        )

    if isinstance(last_year, str) and last_year.isdigit():
        pass
    elif isinstance(last_year, int):
        last_year = str(last_year)
    else:
        raise ExamException(
            "last_year non è un numero intero positivo o una stringa che ne rappresenti uno"
        )
        
    #don't check for first < last because it will just return [] without causing any issues
        
    averages = {}
    # group the values
    for item in time_series:
        if first_year <= item[0][:4] <= last_year:
            if item[0][0:4] not in averages:
                averages[item[0][0:4]] = []
            averages[item[0][0:4]].append(item[1])

    # calculate the avgs
    for year in averages:
        averages[year] = sum(averages[year]) / len(averages[year])

    print("Averages:")
    print(averages)

    variations = {}
    # calculate variations
    if len(averages) <= 1:
        return []

    for year in list(averages.keys())[
        1:
    ]:  # need to use a list because dicts don't support slicing due to being unordered
        # find first valid previous year
        prev_year = int(year) - 1
        while str(prev_year) not in averages:
            prev_year -= 1
        prev_year = str(prev_year)

        variations[prev_year + "-" + year] = averages[year] - averages[prev_year]

    print("Increments:")
    return variations

#TESTING
time_series_file = CSVTimeSeriesFile(name="data.csv")

time_series = time_series_file.get_data()

print("Data:")
print(time_series)

print(compute_increments(time_series, 1953, 1956))
