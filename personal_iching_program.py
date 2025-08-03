
import sqlite3
import random
import json
from datetime import datetime

connect = sqlite3.connect('savedhexagrams.db')
cursor = connect.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS saved_hexagrams (
    id INTEGER PRIMARY KEY UNIQUE,
    reading_name TEXT NOT NULL,
    query TEXT DEFAULT "No query entered",
    primary_hexagram TEXT NOT NULL,
    changing_lines TEXT DEFAULT 0,
    secondary_hexagram TEXT DEFAULT 0,
    query_context TEXT,
    date_time TEXT
);
""")

with open('hexagramKey.json') as hexagramKey:
    try:
        data_hex = json.load(hexagramKey)
        print('\nHexagram data loaded!\n')
    except json.JSONDecodeError as e:
        print(f'Invalid JSON: {e}\n')

io_data = {
        "reading_name": "",
        "query": "",
        "primary_hexagram": [],
        "changing_lines": [],
        "secondary_hexagram": [],
        "query_context": ""
        "date_time:" ""
    }

primary_hexagram = []
secondary_hexagram = []
changing_lines = []

def save_reading():
    while True:        
        ans = input('What is the name of this reading?\n')
        if ans == '':
            print('Invalid Entry: Name is required')
        else:
            io_data["reading_name"] = ans
            date_time = datetime.now()
            date_now = date_time.strftime("%d-%m-%Y")
            io_data["date_time"] = date_now
            hex_value_convert(primary_hexagram, secondary_hexagram, changing_lines)
            if save_sql_mechanic() == 'S':
                print('\nReading saved successfully\n')
                return
            else:
                print("\nError saving. Please try again\n")
                return

def retrieve_reading_mechanism(ans_2):
    match ans_2:
        case '1':
            pass
        case '2':
            try:
                sql_1 = """SELECT * FROM saved_hexagrams ORDER BY id ASC LIMIT 10"""
                cursor.execute(sql_1)
                connect.commit
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                connect.close()
            except Exception as e:
                print(f"\nError: {e}\n")
                connect.close()
   
def hex_value_convert(primary_hexagram, secondary_hexagram, changing_lines):
    a = 0
    while a != 3:
        for key, value in data_hex.items():
            if value["lineValues"] == primary_hexagram and a == 0:
                primary_hexagram = value["hexagram"]
                a += 1
            if secondary_hexagram and a == 1:
                if value["lineValues"] == secondary_hexagram:
                    secondary_hexagram = value["hexagram"]
                    a += 1
            if not secondary_hexagram and a == 1:
                a += 1
            if a == 2:
                io_data["primary_hexagram"] = json.dumps(primary_hexagram)
                io_data["secondary_hexagram"] = json.dumps(secondary_hexagram)
                io_data["changing_lines"] = json.dumps(changing_lines)
                a += 1
                    
def save_sql_mechanic():
    new_io = {k: v for k, v in io_data.items() if v != '' and v != []}
    columns = ', '.join(new_io.keys())
    placeholders = ', '.join(['?'] * len(new_io))
    values = tuple(new_io.values())
    sql = f"INSERT INTO saved_hexagrams ({columns}) VALUES ({placeholders})"
    try:
        cursor.execute(sql, values)
        connect.commit()
        return 'S'
    except Exception as e:
        print(f"Error: {e}")

def position_calculator():
    changing_lines.insert(0, 0) 
    x = 0
    while 0 in changing_lines:
        for index, i in enumerate(changing_lines):
            if x <= 6:
                if index != 0 and i != 0:
                    changing_lines[index] = index
                    x += 1
                else:
                    x += 1
            if x > 6 and 0 in changing_lines:
                changing_lines.remove(0)
            if 0 not in changing_lines:
                io_data["changing_lines"] = changing_lines

def changing_lines_expand():
    a = 0
    b = 0
    while a <= len(changing_lines):
        for key, value in data_hex.items():
            if value["lineValues"] == primary_hexagram:
                matching_line = [line for line in value["lines"] if line["position"] in changing_lines]
                for line in matching_line:
                    print(f'Line: {line["position"]}:\n{line["meaning"]}\n')
                else:
                    return 'Error: No match found.'

def iodata_wipe():
    io_data["reading_name"] = None
    io_data["query"] = None
    io_data["primary_hexagram"] = None
    io_data["changing_lines"] = None
    io_data["secondary_hexagram"] = None
    io_data["query_context"] = None

def set_wipe():
    primary_hexagram.clear()
    secondary_hexagram.clear()
    changing_lines.clear()
    print('\nHexagram memory reset.\n')

def main_menu(): 
    while True:
        print('Select an option\n1) Cast a Hexagram\n2) Retrieve a reading\n3) Exit')
        try:
            ans = str(input(''))
        except:
            print('Please choose a valid option')
        match ans:
            case '1':
                while True:
                    print('What is your query?')
                    prompt = input('')
                    context = input("What is the query's context?\n")
                    print(f'"{prompt}"')
                    io_data["query"] = prompt 
                    io_data["query_context"] = context
                    prompt = ''
                    if cast_mechanism() == 'y':
                        continue
                    else:
                        print('Returning to main menu...\n')
                        break
            case '2':
                ans_2 = input("What would you like to do?\n1) Retrieve reading by name or id\n2) Display first 10 and last 10\n3) Return to main menu\n")
                match ans_2:
                    case '1':
                        pass
                    case '2':
                        retrieve_reading_mechanism(ans_2)
                    case '3':
                        continue
            case '3': 
                print('Exiting...')
                break
            case _:
                print('Please choose a valid option\n')

def cast_menu():
    while True:
        print('1) Save reading\n2) Expand reading\n3) Make another casting\n4) Return to main menu\n')
        ans = input('Please select an option\n')
        match ans:
            case '1':
                save_reading()
            case '2':
                if 0 not in changing_lines:
                    match primary_secondary_expand():
                        case 'y':
                            continue
                        case 'n':
                            set_wipe()
                            iodata_wipe()
                            return 'n'
                if 0 in changing_lines:
                    match primary_unchanging_expand():
                        case 'y':
                            continue
                        case 'n':
                            set_wipe()
                            iodata_wipe()
                            return 'n'
            case '4':
                set_wipe()
                iodata_wipe()
                return 'n'
            case '3':
                set_wipe()
                iodata_wipe()
                return 'y'

def primary_secondary_expand():
    count = 0
    while count != 2:
        for key, value in data_hex.items():
            if value["lineValues"] == primary_hexagram and count == 0:
                print(f'\nPrimary Hexagram {value["hexagram"]} | {value["name"]["english"]} {value["unicode"]}\n')
                print(f'Judgement:\n{value["judgement"]}\nImage:\n{value["images"]}\n')
                count += 1
            if value["lineValues"] == secondary_hexagram and count != 0:
                print(f'Secondary Hexagram {value["hexagram"]} | {value["name"]["english"]} {value["unicode"]}\n')
                print(f'Judgement:\n{value["judgement"]}\nImage:\n{value["images"]}\n')
                changing_lines_expand()
                count += 1
    if count == 2:
        ans = input('Select an option\n1) Return to Cast Menu\n2) Return to Main menu\n')
        match ans:
            case '1':
                return 'y'
            case '2':
                return 'n'

def primary_unchanging_expand():
    a = 0      
    for key, value in data_hex.items():
        if value["lineValues"] == primary_hexagram and a != 1:
            print(f'\nPrimary Hexagram {value["hexagram"]} | {value["name"]["english"]} {value["unicode"]}\n')
            print(f'Judgement:\n{value["judgement"]}\nImage:\n{value["images"]}')
            ans = input('Select an option\n1) Return to Cast Menu\n2) Return to Main menu\n')
            match ans:
                case '1':
                    return 'y'
                case '2':
                    return 'n'

def casting_caclulator(hexagram):
    def secondary_calc(hexagram):    
        for i in hexagram:
            if i == 7:
                primary_hexagram.append(1)
                secondary_hexagram.append(1)
                changing_lines.append(0)
            if i == 8:
                primary_hexagram.append(0)
                secondary_hexagram.append(0)
                changing_lines.append(0)
            if i == 6:
                primary_hexagram.append(0)
                secondary_hexagram.append(1)
                changing_lines.append(6)
            if i == 9:
                primary_hexagram.append(1)
                secondary_hexagram.append(0)
                changing_lines.append(9)
    secondary_calc(hexagram)
    a = 0
    while a != 2:
        if sum(changing_lines) != 0:
            for key, value in data_hex.items():
                if value["lineValues"] == primary_hexagram and a == 0:
                    print(f'You have casted Hexagram {value["hexagram"]} | {value["unicode"]}')
                    a += 1
                    io_data["primary_hexagram"] = value["hexagram"]
                    position_calculator()
                if value["lineValues"] == secondary_hexagram and a != 0:
                    print(f'Changing to\nHexagram {value["hexagram"]} | {value["unicode"]}\n')
                    a += 1
                    io_data["secondary_hexagram"] = value["hexagram"]
        elif sum(changing_lines) == 0 and a == 0:
            for key, value in data_hex.items():
                if value["lineValues"] == primary_hexagram:
                    print(f'You have casted {value["hexagram"]} unchanged.\n')
                    a += 2
                    io_data["primary_hexagram"] = value["hexagram"]
                    position_calculator()
                    secondary_hexagram.clear()

def cast_mechanism():
    hexagram = []
    while True:
        cast_n = 0
        while cast_n != 6:
            coin_value = 0
            if cast_n == 0:
                print('Press enter to cast')
            if input('') != '':
                print('Invalid entry')
            coin_value = random.choice([6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9])
            print(cast_print(coin_value))
            hexagram.append(coin_value)
            cast_n += 1
            coin_value = 0 
            if cast_n == 6:
                print('\n')
                casting_caclulator(hexagram)
                if cast_menu() == 'y':
                    return 'y'
                else:
                    return 'n'

def cast_print(coin_value):
    if coin_value == 6:
        return '-x-'
    if coin_value == 7:
        return '---'
    if coin_value == 8: 
        return '- -'
    if coin_value == 9: 
        return '-o-'

main_menu()