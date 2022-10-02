from collections import defaultdict

while (
        station := input("Which station do you want to predict snow for the 2022-2023 year?: ").lower()
) not in ("dca", "iad", "bwi"):
    print("Invalid input. The station must either be DCA, BWI, or IAD (case insensitive)")

oni = {}

with open("oceanic_nino_index/oni.txt") as file:
    for line in file.readlines():
        line = line.split()
        oni[int(line[0])] = list(map(float, line[1:]))

snowfall = {}
snowfall_total = {}

with open(f"snowfall_data/snowfall_{station}.txt") as file:
    for line in file.readlines():
        line = line.split()
        if line[0] != "1999-00":
            snowfall[int(line[0][:2] + line[0].split("-")[-1])] = list(map(lambda x: float(x) if x != "T" else 0.01, line[6:12]))
        else:
            snowfall[2000] = list(map(lambda x: float(x) if x != "T" else 0.01, line[6:12]))

        snowfall_total[line[0]] = float(line[-1])

temperature = {}
with open(f"temperature_data/temperature_{station}.txt") as file:
    for line in file.readlines():
        line = line.split()
        temperature[int(line[0])] = list(map(float, line[1:]))

nao = {}
with open("teleconnections/nao.txt") as file:
    for line in file.readlines():
        line = line.split()
        nao[int(line[0])] = list(map(float, line[1:]))

ao = {}
with open("teleconnections/ao.txt") as file:
    for line in file.readlines():
        line = line.split()
        ao[int(line[0])] = list(map(float, line[1:]))

pdo = {}
with open("teleconnections/pdo.txt") as file:
    for line in file.readlines():
        line = line.split()
        pdo[int(line[0])] = list(map(float, line[1:]))


def get_analog(year: int):
    analogs = defaultdict(int)
    cur_year = oni[year]

    def calculate_analog_score(factor: dict, raise_to: int):
        for key, value in factor.items():
            if year > key > min(snowfall.keys()):
                score = 0
                for month_fac, cur_month_fac in zip(cur_year, value[:len(cur_year)]):
                    score += (max((cur_month_fac, month_fac)) - min((cur_month_fac, month_fac))) ** raise_to

                analogs[key] += score

    # calculate score for oni
    calculate_analog_score(oni, 3)

    # calculate score for snowfall
    calculate_analog_score(snowfall, 2)

    # calculate score for temperatures
    calculate_analog_score(temperature, 1)

    # calculate score based off of NAO teleconnections
    calculate_analog_score(nao, 2)

    # calculate score based off of AO teleconnections
    calculate_analog_score(ao, 2)

    # calculate score based off of PDO teleconnections
    calculate_analog_score(pdo, 2)

    return analogs, cur_year


def average(iterable):
    return sum(iterable) / len(iterable)


analogs = get_analog(2022)[0]
result = sorted(analogs, key=analogs.__getitem__)
avg = 0
for year in result[:10]:
    avg += snowfall_total[f"{year}-{str(year + 1)[-2:]}"]

formatted_years = [
    f"\t\n⚫ {year}-{year + 1}: {snowfall_total[f'{year}-{str(year + 1)[-2:]}']:.3f}\""
    for year in result[:10]
]

print(
    f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
    f"Total snowfall for the 2022-2023 year at {station.upper()} predicted to be: {avg / 10:.1f}\""
)
print(f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\nTop analogs for {station.upper()} are: {''.join(formatted_years)}")