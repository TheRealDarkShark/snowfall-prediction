while (
        station := input("Which station do you want to predict snow for the 2021-2022 year?: ").lower()
) not in ("dca", "iad", "bwi"):
    print("Invalid input. The station must either be DCA, BWI, or IAD (case insensitive)")

oni = {}

with open("oni.txt") as file:
    for line in file.readlines():
        line = line.split()
        oni[int(line[0])] = list(map(float, line[1:]))

snowfall = {}
with open(f"snowfall_{station}.txt") as file:
    for line in file.readlines():
        line = line.split()
        if line[0] != "1999-00":
            snowfall[int(line[0][:2] + line[0].split("-")[-1])] = list(map(lambda x: float(x) if x != "T" else 0.01, line[6:12]))
        else:
            snowfall[2000] = list(map(lambda x: float(x) if x != "T" else 0.01, line[6:12]))

temperature = {}
with open(f"temperature_{station}.txt") as file:
    for line in file.readlines():
        line = line.split()
        temperature[int(line[0])] = list(map(float, line[1:]))


def get_analog(year: int):
    analogs = {}
    cur_year = oni[year]
    snow_cur = snowfall[year]
    temp_cur = temperature[year]
    for key, value in oni.items():
        if key < year:
            score = 0
            for month_oni, cur_month_oni in zip(cur_year, value[:len(cur_year)]):
                if cur_month_oni > month_oni:
                    score += (cur_month_oni - month_oni) ** 2
                elif cur_month_oni < month_oni:
                    score += (month_oni - cur_month_oni) ** 2

            analogs[key] = score

    for key, value in snowfall.items():
        if key < year and key in analogs.keys():
            score = 0
            for month_snow, cur_month_snow in zip(snow_cur, value):
                if cur_month_snow > month_snow:
                    score += (cur_month_snow - month_snow) ** 2
                elif month_snow > cur_month_snow:
                    score += (month_snow - cur_month_snow) ** 2

            analogs[key] += score

    for key, value in temperature.items():
        if key < year and key in analogs.items():
            score = 0
            for month_temp, cur_temp in zip(temp_cur, value[:len(temp_cur)]):
                if cur_temp > month_temp:
                    score += (cur_temp - month_temp) ** 2
                elif cur_temp < month_temp:
                    score += (month_temp - cur_temp) ** 2

            analogs[key] += score

    return analogs, cur_year


def average(iterable):
    return sum(iterable) / len(iterable)


analogs = get_analog(2021)[0]
result = sorted(analogs, key=analogs.__getitem__)
avg = 0
for year in result[:10]:
    avg += sum(snowfall[year][-3:] + snowfall[year + 1][:4])

formatted_years = [
    f"\t\n⚫ {year}-{year + 1}: {sum(snowfall[year][-3:] + snowfall[year + 1][:4]):.3f}\""
    for year in result[:10]
]

print(f"Total snowfall for the 2021-2022 year at {station.upper()} predicted to be: {avg / 10:.3f}\"")
print(f"Top analogs for {station.upper()} are:{''.join(formatted_years)}")