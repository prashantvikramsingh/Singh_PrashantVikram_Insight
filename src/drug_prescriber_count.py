# Importing the required built in libraries

import operator
import csv
import sys

# Defining a function to get all records from the source file

def getSourceFileContent(sourceFileLocation):
    
    list_of_rows = []
    final_list_rows = []
    
    with open(sourceFileLocation, 'r') as source:
        list_of_rows = [line.split(',') for line in source]
        for line in list_of_rows:
            temp_list = [element.strip() for element in line]
            final_list_rows.append(temp_list)
        return final_list_rows
		
# Defining a function to compute the total cost for a particular prescribed drug
		
def getTotalDrugCost(sourceFileContent):

    drug_cost = list(map(lambda x: {x[3]: x[4]}, sourceFileContent[1:]))

    drug_cost_total = {}
    for d in drug_cost:
        for k, v in d.items():
            if not k in drug_cost_total:
                drug_cost_total[k] = 0
            drug_cost_total[k] += int(v)
            
    return drug_cost_total
	
# Defining a function to compute the total number of unique prescribers of a particular drug

def getUniqueDrugPrescriberCount(sourceFileContent):

    drug_prescriber = list(map(lambda x: {x[3]: [x[1], x[2]]}, sourceFileContent[1:]))

    unique_drug_prescriber_count = {}
    for d in drug_prescriber:
        for k, v in d.items():
            if not k in unique_drug_prescriber_count:
                unique_drug_prescriber_count[k] = [1, v]
            if v[0] not in unique_drug_prescriber_count[k][1] and v[1] not in unique_drug_prescriber_count[k][1]:
                unique_drug_prescriber_count[k][0] += 1
                unique_drug_prescriber_count[k][1].append(v[0])
                unique_drug_prescriber_count[k][1].append(v[1])

    unique_drug_prescriber_count = dict((x, y[0]) for x, y in unique_drug_prescriber_count.items())
        
    return unique_drug_prescriber_count
	
# Defining a function to combine the output of getUniqueDrugPrescriberCount() and getTotalDrugCost() function
	
def getUnsortedDrugPrescriberCountAndDrugCost(uniqueDrugPrescriberCount, totalDrugCost):

    unsorted_output = dict((k, [uniqueDrugPrescriberCount[k], totalDrugCost.get(k)]) for k in uniqueDrugPrescriberCount)
    
    return unsorted_output

# Defining a function to sort the result based on the total_cost of a drug
	
def getSortedDrugPrescriberCountAndDrugCost(unsortedDrugPrescriberCountAndDrugCost):

    sorted_output = sorted(unsortedDrugPrescriberCountAndDrugCost.items(), key=operator.itemgetter(0), reverse = True)

    sorted_output = [[x[0], x[1][0], x[1][1]] for x in sorted_output]

    sorted_output = [['drug_name', 'num_prescriber', 'total_cost']] + sorted_output
    
    return sorted_output
	
	
# Defining a function to write the output to a file
	
def writeOutputFile(sortedDrugPrescriberCountAndDrugCost, targetFileLocation):

    with open(targetFileLocation,"w", newline='\n') as f:
        wr = csv.writer(f)
        wr.writerows(sortedDrugPrescriberCountAndDrugCost)
		

# Defining a main() function which reads the input and output directory from the command line
# and calls all the above functions in sequence and creates output file
		
def main():
    
    user_input = sys.argv[1:]
    print("----Process Started----", '\n')
    counter = 0
    if len(user_input) == 0:
        print('No Input provided. Process is exiting!!')
        exit(0)
    for ip in user_input:
        if counter == 0:
            sourceFileLocation = str(ip)
        else:
            targetFileLocation = str(ip)
        counter += 1
    
    print('Reading the source file!!!', '\n')
    sourceFileContent = getSourceFileContent(sourceFileLocation)
    
    print('Getting the total cost of each prescribed drug!!!', '\n')
    totalDrugCost = getTotalDrugCost(sourceFileContent)
    
    print('Getting the count of unique prescribers of each drug!!!', '\n')
    uniqueDrugPrescriberCount = getUniqueDrugPrescriberCount(sourceFileContent)
    
    print('Consolidating the Drug, it\'s unique prescriber count and total cost of the drug!!!', '\n')
    unsortedDrugPrescriberCountAndDrugCost = getUnsortedDrugPrescriberCountAndDrugCost(uniqueDrugPrescriberCount, totalDrugCost)
    
    print('Sorting the content based on total cost of the drug in descending order!!!', '\n')
    sortedDrugPrescriberCountAndDrugCost = getSortedDrugPrescriberCountAndDrugCost(unsortedDrugPrescriberCountAndDrugCost)
    
    print('Writing the content to the output file!!!', '\n')
    writeOutputFile(sortedDrugPrescriberCountAndDrugCost, targetFileLocation)
    
    print('Process finished!!!')
	

if __name__ == '__main__':
    main()


