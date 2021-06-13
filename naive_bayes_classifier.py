"""
    Implemented By: Taukirahmed Khatri
"""

# import pandas for reading the data
import pandas as pd

# get the path of the data file
file_path = input("Enter Path where data is stored: ")

# read the data with first row as header
data = pd.read_csv(file_path, header=0)

# Get all the column names
cols = data.columns.tolist()

# Get distinct classes
total_classes = data[cols[-1]].unique()

# Freqency table
fre_table = {}

# For all the columns, initializing all the unique features with all the class lables as 0
for i in range(len(cols)-1):
    fre_table[cols[i]] = {}
    unique_features = data[cols[i]].unique()
    for j in unique_features:
        fre_table[cols[i]][j] = {}
        for k in total_classes:
            fre_table[cols[i]][j][k] = 0

# Count the frequencies
for i in range(len(cols)-1):
    for j, k in zip(data[cols[i]], data[cols[-1]]):
        # print(j, " : ", k)
        fre_table[cols[i]][j][k] += 1

print("Frequency Table")
print("---------------------")
print(fre_table)
print("---------------------")
observations = {'total': 0}
total_array = {}
for i in fre_table:
    total_array[i] = {}
    for j in fre_table[i]:
        total_array[i][j] = {'total': 0}
        for k in total_classes:
            current_value = fre_table[i][j][k]
            total_array[i][j]['total'] += current_value
            total_array[i][j][k] = current_value
            observations['total'] += current_value
            if k not in observations:
                observations[k] = current_value
            else:
                observations[k] += current_value

print("Total Array")
print("---------------------")
print(total_array)
print("---------------------")
print("Observations")
print("---------------------")
print(observations)
print("---------------------")

prob_classes = {}

# finding probability of classes
for i in total_classes:
    prob_classes[i] = observations[i]/observations['total']

print("Probability of Classes (Predictor Prior Probability)")
print("---------------------")
print(prob_classes)
print("---------------------")

# finding probability of features with respect to classes
# for example : {'Weather':{'Sunny':{'No':0,'Yes':0}, 'Overcast':{'No':0, 'Yes':0}, 'Rainy':{'No':0,'Yes':0}}}
prob_features = {}
for i in range(len(cols)-1):
    prob_features[cols[i]] = {}
    unique_features = data[cols[i]].unique()
    for j in unique_features:
        prob_features[cols[i]][j] = {}
        for k in total_classes:
            prob_features[cols[i]][j][k] = total_array[cols[i]
                                                       ][j][k]/observations[k]
print("Probabilty of Features")
print("---------------------")
print(prob_features)
print("---------------------")

prob_features_individual = {}
for i in total_array:
    prob_features_individual[i] = {}
    for j in total_array[i]:
        prob_features_individual[i][j] = total_array[i][j]['total'] / \
            observations['total']

print("Probability of Features Individual (Predictor Prior Probability)")
print("---------------------")
print(prob_features_individual)
print("---------------------")

print('\nThe columns of features present in DataFrame are:',
      " | ".join(cols[:-1]), "\n")
print("The features in each column are:")
for i in cols:
    l = data[i].unique()
    print(i, ":", " | ".join(l))
print()
user_input = {}
for i in range(len(cols)-1):
    l = data[cols[i]].unique()
    print("Enter feature name for column:", cols[i])
    print("Available Choices:", " | ".join(l))
    t = input("Enter Choice here: ")
    user_input[cols[i]] = t

# print(user_input)

prob_user_input = {}
for i in user_input:
    for j in range(len(total_classes)):
        if total_classes[j] not in prob_user_input:
            prob_user_input[total_classes[j]] = 1
        numerator = prob_features[i][user_input[i]][total_classes[j]]
        denominator = prob_features_individual[i][user_input[i]]
        prob_user_input[total_classes[j]] *= (numerator/denominator)


for i in prob_classes:
    prob_user_input[i] *= prob_classes[i]
# print(prob_user_input)
m = -1
lable = ""
for i in prob_user_input:
    if m == -1:
        m = prob_user_input[i]
        lable = i
    else:
        if m < prob_user_input[i]:
            m = prob_user_input[i]
            lable = i
print("Predicted Lable:", lable)
