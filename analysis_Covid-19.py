#importing necessary libraries
import pandas as pd   #importing pandas for data analysis
import matplotlib.pyplot as plt  #importing maatplotlib for creating visualizatiions
import re #importing re modeule for regular expressions
import numpy as np   #importing numpyy for numerical and mathematical operations on arrays 
import seaborn as sns  #importing seaborn for statistical visualization
#reading necessary files
agegroup=pd.read_csv('C://Users//500062294//Desktop//New folder//AgeGroupDetails.csv')   #agegroups w.r.t percentages
covid_19_india=pd.read_csv("C://Users//500062294//Desktop//New folder//covid_19_india.csv")   #covid 19 dataset comprising confirmed, cured and deaths reportd in various states
hospital_beds=pd.read_csv("C://Users//500062294//Desktop//New folder//HospitalBedsIndia.csv")   #Hospital beds occupied in different states
individual_details=pd.read_csv("C://Users//500062294//Desktop//New folder//IndividualDetails.csv")   #individual cases details

#General preprocessing of data 

#print(agegroup.head()) 
#print(agegroup.info())
#print(hospital_beds)
hospital_beds=hospital_beds[:-1]
hospital_beds.fillna(0,inplace=True)

# Converting object data type to float
for i in hospital_beds.columns[2:]:
    if hospital_beds[i].dtype=='object':
        hospital_beds[i]=hospital_beds[i].astype('int64')
#print(hospital_beds)
#Coverting Date to appropriate date time format
covid_19_india['Date']=pd.to_datetime(covid_19_india['Date'])
#print(covid_19_india.head())


#function to get gender_Based_analysis
df1=covid_19_india.groupby('Date')[['Cured','Deaths','Confirmed']].sum() #Grouping total number of cured, deaths and confirmed cases based on dates
df2=covid_19_india.groupby('State/UnionTerritory')[['Cured','Deaths','Confirmed']].sum()
state_cases=covid_19_india.groupby("State/UnionTerritory")['Confirmed','Deaths','Cured'].sum()

def genderBasedAnalysis():
    print("1. Gender Based Analysis") 
    gender=individual_details.gender #result in a dataframe consisting of gender information
    gender.dropna(inplace=True)  #results in dropping missing gender data and saves it then and there
    gender=gender.value_counts()  #counts total occurences of M and F
    per=[]  #empty list
    for i in gender:  
        perc=i/gender.sum()   #calculating percentage of M and F
        per.append(format(perc,'.2f'))  #changes the format to two float points and appends to the per list
    plt.figure(figsize=(5,5))    #specifying size of the figure
    plt.title('Comparison of cases acording to gender',fontsize=20)   #Speifying title of the visualization or pie chart
    plt.pie(per,autopct='%1.2f%%') #displaying percent values after string formatting
    plt.legend(gender.index,loc='upper right',title='Gender',fontsize=15) #displaying legend
def ageBasedAnalysis(): 
    print("2. Age Based analysis")
    perc=[] #empty list
    for i in agegroup['Percentage']:
        per=float(re.findall("\d+\.\d+",i)[0])  #checking for percentage in the column
        perc.append(per)  #apending the percentage into the empty list
    agegroup['Percentage']=perc #equating
    plt.figure(figsize=(5,5))  #specifying figure size
    plt.title('Age group wise analysis',fontsize=14)  #specifying title of graph
    plt.pie(agegroup['Percentage'],autopct='%1.2f%%')  #displaying percent values after string formatting
    plt.legend(agegroup['AgeGroup'],loc='upper right',title='Age Group')  #specifying legend
    plt.subplots(figsize=(8,7)) #specifying size of plot
    sns.pointplot(x=agegroup['AgeGroup'], y=agegroup['Percentage'])  #using seaborn to visualize using pointplot
def confirmedCasesBasedOnAgeGroup():
    print("3. Confirmed Cases to the Age group analysis")
    plt.figure(figsize=(5,5)) #specifying size of the plot
    plt.title('Comparing Total cases in different age group',fontsize=15) #specifying title of the plot
    plt.xticks(fontsize=10)  #specifying x axis font size
    plt.yticks(fontsize=10) #specifying y axis font size
    plt.xlabel('Age Group') #Specifying x label
    plt.ylabel('Confirmed Cases')#specifying y label
    plt.bar(agegroup['AgeGroup'],agegroup['TotalCases']) #taking x axis as agegroup and y axis as TotalCases
    #for i, v in enumerate(agegroup['TotalCases']):
     #   plt.text(i-.15, v,agegroup['TotalCases'][i], fontsize=15 )

def DateWiseAnalysis():
    print("4. Overtime analysis of Cured, Deaths and Confirmed cases")
    df1=covid_19_india.groupby('Date')[['Cured','Deaths','Confirmed']].sum()  #making a dataframe df1, which contains total number of deaths, cured and confirmed cases
    plt.figure(figsize=(10,10)) #specifying size of plot
    plt.title('Observed Cases',fontsize=20)  #specifying title
    plt.xticks(fontsize=8,rotation=70) #specifying rotaion of x scale and its font size
    plt.yticks(fontsize=8)   #specifying font_size of y label
    plt.xlabel('Date',fontsize=15) #specifying x label and its size
    plt.ylabel('Number of cases',fontsize=15) #specfying y label and its size
    plt.plot(df1.index,df1['Confirmed'],label='Confirmed',color='black') #plotting distribution of confirmed cases date wise
    plt.plot(df1.index,df1['Cured'],label='Cured',color='green') #plotting distribution of cured cases date wise
    plt.plot(df1.index,df1['Deaths'],label='Death',color='red')  #plotting distribution of deaths date wise
    plt.legend(fontsize=12)  #specifying size of the legend
def Top15Cases():
    print("5. The top 15 states with most confirmed cases")  
    df2=covid_19_india.groupby('State/UnionTerritory')[['Cured','Deaths','Confirmed']].sum() #dataframe consisting of total of confirmed, deaths and cured cases state wise
    df2=df2.nlargest(15,'Confirmed') #updating dataframe df2
    plt.figure(figsize=(5,5)) #specifying size of plot
    plt.title('Top 15 states with confirmed cases',fontsize=15)  #specifying title of the plot
    plt.xticks(fontsize=8,rotation=70) #specifying rotation and size of x scale
    plt.yticks(fontsize=8)  #specifying size of y scale
    plt.xlabel('State',fontsize=8)#specifying x label and its size
    plt.ylabel('Cases',fontsize=8)  #specifying y label and its size
    plt.plot(df2.index,df2.Confirmed,label='Confirmed') #plotting deaths, confirmed cases and deaths
    plt.plot(df2.index,df2.Deaths,label='Deaths')
    plt.plot(df2.index,df2.Cured,label='Cured')
    plt.legend(fontsize=12)
    
def Top15StatesWithOutbreak():
    print("7. Pie chart distribution of Most affected States")
    perc=[]  #empty list
    df2=covid_19_india.groupby('State/UnionTerritory')[['Cured','Deaths','Confirmed']].sum() #dataframe consisting of total of confirmed, deaths and cured cases state wise
    df2=df2.nlargest(20,"Confirmed") #takes the top 15 states on the basis of confirmed cases
    for i in df2.Confirmed: 
        perc.append(i)  #appending all the values in the empty list
    plt.figure(figsize=(10,10))  #specifying size of the figure
    plt.xticks(rotation=60,fontsize=10)  #specifying rotation and fontsize of x scale
    plt.yticks(fontsize=10)  #specifying font size of y scale
    plt.title('Pie chart distribution of most affected states',fontsize=15)  #specifying size and title of plot
    plt.pie(perc,autopct='%1.2f%%') #speifying string formatting of upto 2 digits of float
    plt.legend(df2.index,loc='upper left')  #specifying legend of the plot
def StateWiseInsights():
    print("6. State Wise Insights")
    state_cases=covid_19_india.groupby("State/UnionTerritory")['Confirmed','Deaths','Cured'].max().reset_index()
    state_cases['Active'] = state_cases['Confirmed'] - (state_cases['Deaths']+state_cases['Cured'])
    state_cases["Death Rate (per 100)"] = np.round(100*state_cases["Deaths"]/state_cases["Confirmed"],2)
    state_cases["Cure Rate (per 100)"] = np.round(100*state_cases["Cured"]/state_cases["Confirmed"],2)
    state_cases = state_cases.sort_values(by='Confirmed', ascending=False)[:15]
    print(state_cases.info())
    state_cases.to_csv('State_Cases.csv')
    print(state_cases.head())
    plt.figure(figsize=(8,8)) #specifying size of plot
    plt.title('Death Rate, and Cure Rate analysis',fontsize=15)  #specifying title of the plot
    plt.xticks(fontsize=8,rotation=70) #specifying rotation and size of x scale
    plt.yticks(fontsize=8)
    plt.xlabel("States")
    plt.ylabel("deaths and cured /100")
  #  plt.plot(state_cases["State/UnionTerritory"],state_cases['Active'],label='Active') #plotting deaths, confirmed cases and deaths
    plt.plot(state_cases["State/UnionTerritory"],state_cases['Death Rate (per 100)'],label='Death Rate (per 100)') #plotting deaths, confirmed cases and deaths
    plt.plot(state_cases["State/UnionTerritory"],state_cases['Cure Rate (per 100)'],label='Cure Rate (per 100)') #plotting deaths, confirmed cases and deaths
    plt.legend(fontsize=12)

    
def stateWiseConfirmedCases():
    print("8. ToP States with Active cases")
    state_cases['Active'] = state_cases['Confirmed'] - (state_cases['Deaths']+state_cases['Cured']) #Calculating Active cases in each state
    df3=state_cases.sort_values("Active",ascending=False )  #Sorting in descending order
    plt.figure(figsize=(8,8)) #specifying size of plot
    plt.subplot(311)   
    plt.title('Active cases',fontsize=15)   #specifying title of plot
    plt.xticks(rotation=60,fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel("States")
    plt.ylabel("Active cases")
    plt.bar(df3.index[:15],df3["Active"][:15],color='blue') #Taking states on x axis and active cases on y axis
    print("\n")
    print("\n")

def stateWiseCure():
    print("9. Top States with most Cures")
    df3=df2.sort_values("Cured",ascending=False )
    plt.figure(figsize=(8,8))
    plt.subplot(312)
    plt.xlabel("States")
    plt.ylabel("Cured cases")
    plt.title('Cured Cases',fontsize=15)
    plt.xticks(rotation=90,fontsize=10)
    plt.yticks(fontsize=10)
    plt.bar(df3.index[:15],df3.Cured[:15],color='green')
    print("\n")
    print("\n")

def stateWiseDeaths():
    print("10. Deaths")
    plt.figure(figsize=(8,8))
    plt.subplot(313)
    df3=df2.sort_values("Deaths",ascending=False)
    plt.xlabel("States")
    plt.ylabel("Deaths")
    plt.title('Deaths Cases',fontsize=15)
    plt.xticks(rotation=90,fontsize=10)
    plt.yticks(fontsize=10)
    plt.bar(df3.index[:15],df3.Deaths[:15],color='red')
    print("\n")
    print("\n")

def Comparison():
    print("11. Comparison of Confirmed , cured and Death Cases" )
    plt.figure(figsize=(10,10))
    plt.title('Confirmed to Cured to Deaths Comparison',fontsize=15)
    plt.xticks(rotation=60,fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel("States")
    plt.ylabel("Confirmed , cured and death cases ")
    plt.bar(df2.index,df2.Confirmed,color='blue')
    plt.bar(df2.index,df2.Cured,color='green')
    plt.bar(df2.index,df2.Deaths,color='red')
def stateWiseAnalysisTop10():
    print("12. Statewise pairplot of Cured, confirmed, and deaths")
    plt.figure(figsize=(5,5))
    df3=df2.nlargest(10,'Confirmed')
    df3['state']=df3.index
    sns.pairplot(df3,hue='state')
def ConfirmedForeignNational():
    print("13. Confirmed Foreign National")
    covid_19_india["ConfirmedForeignNational"].replace("-",0,inplace=True)
    covid_19_india['ConfirmedForeignNational']=covid_19_india['ConfirmedForeignNational'].astype('int64')
    df4=covid_19_india.groupby("State/UnionTerritory")[['ConfirmedIndianNational','ConfirmedForeignNational']].sum()
    df5=df4.nlargest(10,'ConfirmedForeignNational')
    plt.figure(figsize=(4,4))
    plt.xlabel("States")
    plt.ylabel("No of Foreign Nationals")
    plt.xticks(rotation=90,fontsize=10)
    plt.yticks(fontsize=10)
    plt.title("Confirmed Foreign National Top 10")
    plt.bar(df5.index,df5.ConfirmedForeignNational, color="pink")
def ConfirmedIndianNational():
    print("14. Confirmed Indian National")
    covid_19_india['ConfirmedIndianNational'].replace('-',0,inplace=True)
    covid_19_india['ConfirmedIndianNational']=covid_19_india['ConfirmedIndianNational'].astype('int64')
    df4=covid_19_india.groupby("State/UnionTerritory")[['ConfirmedIndianNational','ConfirmedForeignNational']].sum()
    df5=df4.nlargest(10,'ConfirmedIndianNational')
    plt.figure(figsize=(4,4))
    plt.xlabel("States")
    plt.ylabel("No of Indians")
    plt.xticks(rotation=90,fontsize=10)
    plt.yticks(fontsize=10)
    plt.title("Confirmed Indian National Top 10")
    plt.bar(df5.index,df5.ConfirmedIndianNational, color="blue")

genderBasedAnalysis()
ageBasedAnalysis()
confirmedCasesBasedOnAgeGroup()
DateWiseAnalysis()
Top15Cases()
StateWiseInsights()
Top15StatesWithOutbreak()
stateWiseConfirmedCases()
stateWiseCure()
stateWiseDeaths()
Comparison()
stateWiseAnalysisTop10()
ConfirmedForeignNational()
ConfirmedIndianNational()
