class ExamException(Exception):
    pass


class CSVFile:
    def __init__(self, name):
        if type(name) != str:
            raise ExamException("Il nome del file deve essere una stringa")
        self.name = name

    def validate_date(self, date):
        return date[:4].isdigit() and date[4:5] == "-" and date[5:7].isdigit()

    def validate_value(self, value):
        return value.isdigit()

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
            if self.validate_date(sliced[0]) and self.validate_value(sliced[1]): #controlla valitidtà della riga
                if((data and data[-1][0] < sliced[0]) or not data): #valutare una lista come booleano torna false se è vuota
                    data.append(sliced)
                elif(data and data[-1][0] >= sliced[0]):
                    raise ExamException('Trovato valore fuori posto o valore duplicato')


        file.close()

        return data


class CSVTimeSeriesFile(CSVFile):
    pass


time_series_file = CSVTimeSeriesFile(name="data.csv")

time_series = time_series_file.get_data()

print(time_series)

# compute_increments(time_series, first_year, last_year)
#    “1949-1950”: 6.6,
