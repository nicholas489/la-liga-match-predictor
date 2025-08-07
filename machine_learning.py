import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score

def readMatchData(filename):
    try:
        matches = pd.read_csv(filename, index_col=0)
    except FileNotFoundError:
        print(f"Match data file {filename} not found")
        quit()
    return matches

def createPredictors(matches):
    matches["venue_code"] = matches["venue"].astype("category").cat.codes
    matches["opp_code"] = matches["opponent"].astype("category").cat.codes
    matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
    matches["day_code"] = matches["date"].dt.day_of_week
    matches["target"] = (matches["result"] == "W").astype("int")
    return matches

def rollingAverages(group, columns, newColumns):
    group = group.sort_values("date")
    rollingStats = group[columns].rolling(3, closed="left").mean()
    group[newColumns] = rollingStats
    group = group.dropna(subset=newColumns)
    return group

def makePredictions(data, predictors):
    train = data[data["date"] < "2025-01-01"]
    test = data[data["date"] > "2025-01-01"]
    rf.fit(train[predictors], train["target"])
    
    predictions = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], prediction=predictions), index=test.index)
    precision = precision_score(test["target"], predictions)
    return combined, precision
    
if __name__ == "__main__":
    dataFileName = "matches.csv"
    matchData = readMatchData(dataFileName)
    
    matchData["date"] = pd.to_datetime(matchData["date"])
    matchData = createPredictors(matchData)
    
    rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)
    predictorColumns = ["venue_code", "opp_code", "hour", "day_code"]
    
    groupedBy = matchData.groupby("team")
    rollingAverageColumns = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
    newColumns = [f"{column}_rolling" for column in rollingAverageColumns]
    matchesRolling = groupedBy.apply(lambda group: rollingAverages(group, rollingAverageColumns, newColumns))
    matchesRolling = matchesRolling.droplevel("team")
    matchesRolling.index = range(matchesRolling.shape[0])
    
    combined, precision = makePredictions(matchesRolling, predictorColumns + newColumns)
    combined = combined.merge(matchesRolling[["date", "team", "opponent", "result"]], left_index=True, right_index=True)
    print(precision)
    print(pd.crosstab(index=combined["actual"], columns=combined["prediction"]))
    
    