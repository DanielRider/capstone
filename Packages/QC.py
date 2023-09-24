import pandas as pd
import random
import os

class QC():
    def __init__(self,df,save_to=None,filename='QC'):
        self.df = df
        self.save_to = save_to
        self.filename = filename
        
                
        
    def qc(self):
               
        description_dict={i:self.df[i].describe() for i in self.df.columns }
        qc=pd.DataFrame(description_dict)
        try:
            qc_df1=qc.loc[['25%','50%','75%','max','min','std']].T
            qc_df1=qc_df1.rename(columns={'25%':'25th percentile','50%':'50th percentile','75%':'75th percentile',
                        'max':'Maximum value','min':'Minimum value','std':'Standard deviation'})

        except:
            qc_df1=[] 
                
        def var(df):
            l=[]
            for i in df.columns:
                l.append(i)
            return l

        def ex(df):
            l=[]
            for i in self.df.columns:
                l.append(self.df[i].iloc[random.randint(0,len(self.df[i])-1)])
            return l

        def tp(df):
            l=[]
            for i in self.df.columns:
                l.append(df[i].dtype)
            return l

        def N(df):
            l=[]
            for i in self.df.columns:
                l.append(len(df[i]))
            return l

        def missing(df):
            l=[]
            for i in self.df.columns:
                l.append(len(df[i]) - df[i].count())
            return l

        def unique(df):
            l=[]
            for i in self.df.columns:
                l.append(df[i].nunique())
            return l

        def m_freq(df):
            l=[]
            for i in self.df.columns:
                if df[i].nunique()!=df[i].count():    
                    try:
                        l.append(df[i].value_counts().idxmax())
                    except:
                        l.append('NaN')
                else:
                    l.append('All unique values')
            return l
            
        
        def m_freq2(df):
            l=[]
            for i in self.df.columns:
                if df[i].nunique()!=df[i].count():
                    try:
                        df_val=pd.DataFrame(df[i].value_counts())
                        l.append(df_val.index[1])
                    except:
                        l.append('NaN')
                else:
                    l.append('All unique values')
            return l

        def m_freq3(df):
            l=[]
            for i in self.df.columns:
                if df[i].nunique()!=df[i].count():
                    try:
                        df_val=pd.DataFrame(df[i].value_counts())
                        l.append(df_val.index[2])
                    except:
                        l.append('NaN')
                else:
                    l.append('All unique values')
            return l
            
        
        
        
        dict_qc={'Variables':var(self.df),'Example':ex(self.df),'Type':tp(self.df),'N_rows':N(self.df),'Missing values':missing(self.df),
                'Unique values':unique(self.df),'Most frequent':m_freq(self.df),'Second most frequent':m_freq2(self.df),'Third most frequent'                      :m_freq3(self.df)}
        qc_df2=pd.DataFrame(dict_qc)
        qc_df2=qc_df2.set_index('Variables')   
        
        if len(qc_df1)> 0:
            df_final=pd.concat([qc_df2,qc_df1],axis=1,sort=True)
        else:
            df_final=qc_df2

        if self.save_to!=None:
            try:
                df_final.to_csv(f'{self.save_to}/{self.filename}.csv')
            except:
                os.mkdir(self.save_to)
                df_final.to_csv(f'{self.save_to}/{self.filename}.csv')
        return df_final