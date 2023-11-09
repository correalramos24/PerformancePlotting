import pandas as pd
import matplotlib as plt

def read_from_txt(file_path: str, splitter=",", sort_interactive=False) -> pd.DataFrame:
    column_names = None
    records = []

    with open(file=file_path, mode='r') as result_file:
        b_found_header = False

        for line_num, line in enumerate(result_file.readlines()):
            if line.startswith('#'):
                continue # User comment -> skip
            if not b_found_header:
                print(line_num, "Found header as: ", line, end="")
                column_names = line.strip().split(splitter)
                b_found_header = True
            else:
                print(line_num, "Found record: ", line, end="")
                values = line.strip().split(splitter)
                if len(values) != len(column_names):
                    raise Exception("Incosistence record at line {}", line_num)
                
                aux_d = {key : elements for key, elements in zip(column_names, values)}
                records.append(aux_d)
                pass
    
    # Check columns:
    if column_names is None:
        raise Exception("Column names not found!")
    
    print("Found", column_names, "as columns")        
    
    # Check records:
    print("Found", len(records))
    if len(records) == 0:
        raise Exception("No records found!")
    
    # Create and return the dataFrame
    ret = pd.DataFrame(records, columns=column_names, dtype="float64")
    ret.sort_values(inplace=True, by=ret.columns[0])    

    return ret

data = read_from_txt("sampleInput/inputOmp.csv", sort_interactive=True)
print(data)
