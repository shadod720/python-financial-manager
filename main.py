from finance_processor import *

#create and read csv arquive
data = read_csv()

#main program
while True:
    print("------------------------------\nfinancial manager\n------------------------------")
    rows_count(data)
    print("---\n0)search for data\n1)add data\n2)modify data\n3)delete data")
    print("4)save changes\n5)discard changes\n6)exit")
    option = get_values(7)
    match option:
        case 0:
            aux = search_data(data)
            if not aux.empty:
                aux2 = input("press any key to continue: ")
        case 1:
            data = add_data(data)
        case 2:
            data = modify_data(data)
        case 3:
            data = delete_data(data)
        case 4:
            save_changes(data)
            aux = save_sql(data)
            if aux==1:
                aux2 = input("press any key to continue: ")
        case 5: 
            data = read_csv()
        case 6: 
            break
