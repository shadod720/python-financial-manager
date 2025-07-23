import pandas as pd
import sqlite3 as sq

#expenses.csv: date:DD/MM/YYYY, description: string, values: dollars int or float, importance: int 0-5.
def read_csv():
    try:
        data = pd.read_csv("expenses.csv")
        return data
    except:
        with open ("expenses.csv", mode='w') as csv:
            csv.write("date,description,value,importance")
        data = pd.read_csv("expenses.csv")
        return data

#v1: mode (0=date, 1=value, 2=importance, 3=description, 4=modify options, 5=description for search,
#          6=index selection, 7=main.py options, 8=changes confirmation)
def get_values(v1):
    print("---")
    match v1:
        case 0:
            while True:
                try:
                    v2 = input("Date (DD/MM/YYYY): ")
                    v2 = pd.to_datetime(v2, dayfirst=True, format="%d/%m/%Y")
                    v2 = v2.date()
                    return v2
                except:
                    print("----- Invalid date -----")
        case 1:
            while True:
                try:
                    v2 = float(input("Expense value: "))
                    return v2
                except:
                    print("----- Invalid value -----")
        case 2:
            while True:
                try:
                    v2 = int(input("Importance (0-5): "))
                    if v2 in (0, 1, 2, 3, 4, 5):
                        return v2
                    else:
                        print("----- Invalid value -----")
                except:
                    print("----- Invalid value -----")
        case 3:
            print("write carefully, description is used to find data, both for deletion and modification")
            while True:
                v2 = input("Expense description (not empty): ")
                if v2.strip() == "":
                    print("----- Invalid description -----")
                else:
                    return v2.strip().lower()
        case 4:
            while True:
                try:
                    v2 = int(input("0=date, 1=description, 2=value, 3=importance: "))
                    match v2:
                        case 0:
                            return "date", 0
                        case 1:
                            return "description", 3
                        case 2:
                            return "value", 1
                        case 3:
                            return "importance", 2
                        case _:
                            print("----- Invalid value -----")
                except:
                    print("----- Invalid value -----")
        case 5:
            while True:
                v2 = input("Expense description (not empty): ")
                if v2.strip() == "":
                    print("----- Invalid description -----")
                else:
                    return v2.strip().lower()
        case 6:
            while True:
                try:
                    v2 = int(input("Index selection: "))
                    if v2>=0:
                        return v2
                    else:
                        print("----- Invalid index -----")
                except:
                    print("----- Invalid index -----")
        case 7:
            while True:
                try:
                    v2 = int(input("choose a option: "))
                    if v2 in (0, 1, 2, 3, 4, 5, 6):
                        return v2
                    else:
                        print("----- Invalid option -----")
                except:
                    print("----- Invalid option -----")
        case 8:
            while True:
                try:
                    v2 = int(input("0=confirm, 1=cancel: "))
                    if v2==0 or v2==1:
                        return v2
                    else:
                        print("----- Invalid option -----")
                except:
                    print("----- Invalid option -----")

#get data line in that order: date, description, value, importance 
def get_dataline():
    v1 = get_values(0)
    v2 = get_values(3)
    v3 = get_values(1)
    v4 = get_values(2)
    print(f"------------------------------\nadd this data? {v1}, {v2}, {v3}, {v4}")
    aux = input("1=add, 2=dont add: ").strip()
    while aux!="1" and aux!="2":
        aux = input("Invalid option, 1=add, 2=dont add: ").strip()
    if aux=="1":
        return v1, v2, v3, v4
    else:
        return True
    
#adds data, if the user gives up the addition, it returns the same DF without changes
def add_data(data):
    print("------------------------------\nAdd data")
    aux = ['date', 'description', 'value', 'importance']
    v1 = get_dataline()
    if v1==True:
        return data
    else:
        v1 = pd.DataFrame([v1], columns=aux)
        data = pd.concat([data, v1], ignore_index=True)
        return data

#saves the changes made to the csv file
def save_changes(data):
    with open ("expenses.csv", mode="w", newline='') as csv:
        data.to_csv(csv, index=False)

#search for specific data and data lines through their description
def search_data(data):
    print("------------------------------\nData search")
    while True:
        searchID = get_values(5)
        foundID = data["description"].str.contains(searchID, case=False, na=False)
        if not data[foundID].empty:
            print("---\n", data[foundID])
            return data[foundID]
        else:
            print("---\nno data found")
            aux = input("search again? (1=yes): ")
            if aux!="1":
                return data[foundID]

#delete rown in csv archive
def delete_data(data):
    aux = search_data(data) 
    while True:
        if aux.empty:
            return
        aux1 = get_values(6)
        if aux1 in aux.index:
            confirmation = get_values(8)
            if confirmation==0:
                data = data.drop(index=aux1)
                aux = aux.drop(index=aux1)
                aux2 = input("delete more? (1=yes): ")
                if aux2.strip()!="1":
                    return data
                else:
                    print("------------------------------\n", aux)
            else:
                return data
        else:
            print("----- Invalid index -----")
            aux2 = input("try again? (1=yes): ")
            if aux2.strip()!="1":
                return data
            else:
                print("------------------------------\n", aux)

#modify rows and columns in csv archive
def modify_data(data):
    aux = search_data(data)
    while True:
        if aux.empty:
            return
        aux1 = get_values(6)
        if aux1 in aux.index:
            aux2 = get_values(4)
            aux3 = get_values(aux2[1])
            confirmation = get_values(8)
            if confirmation==0:
                data.at[aux1, aux2[0]] = aux3
                aux.at[aux1, aux2[0]] = aux3
                aux2 = input("modify more? (1=yes): ")
                if aux2.strip()!="1":
                    return data
                else:
                    print("------------------------------\n", aux)
            else:
                return data
        else:
            print("----- Invalid index -----")
            aux2 = input("try again? (1=yes): ")
            if aux2.strip()!="1":
                return data
            else:
                print("------------------------------\n", aux)


#saves the file in .db format, to be used in other programs, such as Power BI for example
def save_sql(data):
    conecction = None
    if data.empty:
        print("empty data, not saved")
        return 1
    try:
        connection = sq.connect("expenses.db")
        data.to_sql(name="expenses", con=connection, if_exists="replace", index=False)
        print("saved successfully")
    except:
        print("error")
    finally:
        if connection:
            connection.close()
            return 1
        
#show the rows count in csv
def rows_count(data):
    v1 = len(data)
    print(f"rows in expenses.csv: {v1}")
