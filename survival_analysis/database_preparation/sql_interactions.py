import sqlite3
import logging 
import pandas as pd
import numpy as np
import os
from ..logger import CustomFormatter

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

class SqlHandler:

    def __init__(self, dbname:str,table_name:str) -> None:
        self.cnxn=sqlite3.connect(f'{dbname}.db')
        self.cursor=self.cnxn.cursor()
        self.dbname=dbname
        self.table_name=table_name

    def close_cnxn(self)->None:

        logger.info('commiting the changes')
        self.cnxn.close()
        logger.info('the connection has been closed')

    def insert_one()->None:
        pass

    def get_table_columns(self)->list:
        self.cursor.execute(f"PRAGMA table_info({self.table_name});")
        columns = self.cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        logger.info(f'the list of columns: {column_names}')
        # self.cursor.close()

        return column_names
    
    def truncate_table(self)->None:
        

        query=f"DROP TABLE IF EXISTS {self.table_name};"
        self.cursor.execute(query)
        logging.info(f'the {self.table_name} is truncated')
        self.cursor.close()

    def drop_table(self):
        
        query = f"DROP TABLE IF EXISTS {self.table_name};"
        logging.info(query)

        self.cursor.execute(query)

        self.cnxn.commit()

        logging.info(f"table '{self.table_name}' deleted.")
        logger.debug('using drop table function')

    def insert_many(self, df: pd.DataFrame) -> str:
        
        df=df.replace(np.nan, None) # for handling NULLS
        df.rename(columns=lambda x: x.lower(), inplace=True)
        columns = list(df.columns)
        logger.info(f'BEFORE the column intersection: {columns}')
        sql_column_names = [i.lower() for i in self.get_table_columns()]
        columns = list(set(columns) & set(sql_column_names))
        logger.info(f'AFTER the column intersection: {columns}')
        ncolumns=list(len(columns)*'?')
        data_to_insert=df.loc[:,columns]
    
        values=[tuple(i) for i in data_to_insert.values]
        logger.info(f'the shape of the table which is going to be imported {data_to_insert.shape}')
        # if 'geometry' in columns: #! This block is usefull in case of geometry/geography data types
        #     df['geometry'] = df['geometry'].apply(lambda geom: dumps(geom))
        #     ncolumns[columns.index('geometry')]= 'geography::STGeomFromText(?, 4326)'
        
        if len(columns)>1:
            cols,params =', '.join(columns), ', '.join(ncolumns)
        else:
            cols,params =columns[0],ncolumns[0]

        logger.info(f'insert structure: colnames: {cols} params: {params}')
        logger.info(values[0])
        query=f"""INSERT INTO  {self.table_name} ({cols}) VALUES ({params});"""
        
        logger.info(f'QUERY: {query}')

        self.cursor.executemany(query, values)
        try:
            for i in self.cursor.messages:
                logger.info(i)
        except:
            pass


        self.cnxn.commit()
      
        
        logger.warning('the data is loaded')

    def from_sql_to_pandas(self, )-> pd.DataFrame:
        pass
        #TODO: do it by yourself

    def from_sql_to_pandas(self, chunksize:int, id_value:str) -> pd.DataFrame:
        """

        Parameters
        ----------
        chunksize : int
            the chunksize for the extract
        id_value : char
            the values by which it should be sorted, 'MSISDN, DATE_ID'
        dbname : char
            (Default value = 'CVM')
        tablename : char
            (Default value = 'DIM_ARMENIA_MSISDNS')
        chunksize:int :
            
     
        Returns
        -------

        """
        
        offset=0
        dfs=[]
       
        
        while True:
            query=f"""
            SELECT * FROM {self.table_name}
                ORDER BY {id_value}
                OFFSET  {offset}  ROWS
                FETCH NEXT {chunksize} ROWS ONLY  
            """
            data = pd.read_sql_query(query,self.cnxn) 
            logger.info(f'the shape of the chunk: {data.shape}')
            dfs.append(data)
            offset += chunksize
            if len(dfs[-1]) < chunksize:
                logger.warning('loading the data from SQL is finished')
                logger.debug('connection is closed')
                break
        df = pd.concat(dfs)

        return df


    def update_table(self,condition):
        pass
        # TODO: complete on your own

   
        



