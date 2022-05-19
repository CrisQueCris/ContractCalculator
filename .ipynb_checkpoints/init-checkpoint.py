import sqlite3
import pandas as pd
import os.path

# 




def init_db():
    '''Create Database structure'''
    con = sqlite3.connect('contrcalc.db')
    cur = con.cursor()
    cur.execute('''
        PRAGMA writable_schema = 1;''')
    cur.execute('''
        delete from sqlite_master where type in ('table', 'index', 'trigger');''')
    cur.execute('''
        PRAGMA writable_schema = 0;''')
    con.commit() 
    cur.execute('VACUUM;')
    cur.execute('''
        PRAGMA INTEGRITY_CHECK;
        ''')

    con.commit() 
    cur.execute('''
    CREATE TABLE IF NOT EXISTS price_table(
        price_id INTEGER PRIMARY KEY,
        commodity_id INTEGER NOT NULL,
        date_fullfillment DATE NOT NULL,
        date_price DATE NOT NULL,
        price REAL NOT NULL,
        currency TEXT NOT NULL
        );
    ''')    
    con.commit() 
    cur.execute('''    
    CREATE TABLE IF NOT EXISTS price_commodities(
        price_id INTEGER,
        commodity_id INTEGER,
        PRIMARY KEY (price_id),
        FOREIGN KEY (price_id)
            REFERENCES price_table (price_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (commodity_id)
            REFERENCES commodities (commodity_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
        );  
    ''')    
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS contracts
        (contract_id INTEGER PRIMARY KEY,
        commodity_id INTEGER NOT NULL,
        price_per_to REAL NOT NULL,
        amount_to REAL NOT NULL,
        date_closure DATE NOT NULL,
        date_fullfillment DATE NOT NULL
        );
    ''')
    con.commit()  
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS contracts_commodities(
        contract_id INTEGER,
        commodity_id INTEGER,
        PRIMARY KEY (contract_id, commodity_id),
        FOREIGN KEY (contract_id)
            REFERENCES contracts (contract_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (commodity_id)
            REFERENCES commodities (commodity_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
    );
    ''')
    con.commit()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS commodities(
        commodity_id INTEGER PRIMARY KEY UNIQUE,
        name TEXT UNIQUE NOT NULL,
        harvest_month INTEGER NOT NULL,
        sowing_month INTEGER NOT NULL,
        reference_harvest_to REAL NOT NULL,
        estimate_harvest_to REAL,
        area_planted REAL        
    );
    
    ''')
    con.commit()
    con.close()
    return

def populate_commodities():
    '''enteres values into commodities'''
    commodities = [ 'barley', 'wheat', 'corn', 'rapeseed']
    harvest_month= [6, 8, 9, 7]
    sowing_month= [8, 9, 4, 8]
    reference_harvest_to = [7.88, 6.4, 8.2, 3.69]
    con = sqlite3.connect('contrcalc.db')
    cursor = con.cursor()
    for i in range(0, len(commodities)):
        cursor.execute("""
    INSERT INTO commodities (name, harvest_month, sowing_month, reference_harvest_to)
        VALUES(?,?,?,?)
        """, (commodities[i], harvest_month[i], sowing_month[i], reference_harvest_to[i]))
    con.commit()
    con.close()
    return


def get_table_df(table_name, database_path='contrcalc.db'):
    """Returns (table, connection). table is a pandas DataFrame."""
    #BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #db_path = os.path.join(BASE_DIR, database_path)
    con = sqlite3.connect(database_path)
    try:
        df = pd.read_sql("SELECT * FROM %s" %table_name, con)
        #  print("\nLoading %s table from SQLite3 database." % table_name)
    except DatabaseError as e:
        if 'no such table' in e.args[0]:
            print("\nNo such table: %s" % table_name)
            print("Create the table before loading it. " +
                  "Consider using the create_sqlite_table function")
            raise DatabaseError
        else:
            print(e)
            raise Exception("Failed to create %s table. Unknown error." %
                            table_name)
    return df, con



def simulate_price_data():
    '''Simulate random wheat price in the future'''
    # for i in range(0,9):
    #     for day in range(200):
    #         ts = future_df.iloc[i]["date_price"] - timedelta(days=day)
    #         price = future_df.iloc[i]['price'] + randint(-60, 60)
    #         series = future_df.iloc[i].copy()
    #         series["date_price"] = ts    
    #         series["price"] = price
    #         future_df = pd.concat([future_df, pd.DataFrame(series).transpose()], axis=0)
    # future_df 
    return

init_db()
populate_commodities()