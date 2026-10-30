from artifact_tool import Workbook, SpreadsheetFile
import random, math, csv, json, os
from datetime import datetime
random.seed(20261029)
OUT='/mnt/data'
months=[f'2025-{m:02d}' for m in range(1,13)]
cats=['Home Essentials','Personal Care','Office Supplies','Lifestyle Accessories']
products=[]
for c,cat in enumerate(cats):
 for k in range(5):
  i=c*5+k+1
  products.append([f'AT-{i:03d}',cat,f'{cat} Product {k+1}',round(12+c*8+k*3.5,2),round(.49+c*.035+k*.012,3),int(1350-c*90+k*120)])
season=[.81,.84,.96,.97,1.02,.99,1.05,1.08,1.04,1.13,1.23,1.42]
rows=[]
for mi,month in enumerate(months):
 for sku,cat,name,price,cost_ratio,base_units in products:
  bp=round(price*(1+.025*mi/11),2)
  bq=round(base_units*season[mi]*(1+random.uniform(-.025,.025)))
  ap=round(bp*(1+random.uniform(-.055,.03)+(0.013 if mi>=7 else 0)),2)
  aq=max(1,round(bq*(1+random.uniform(-.14,.15)+(.055 if mi>=8 else 0))))
  bc=round(bp*cost_ratio,2)
  ac=round(bc*(1+.035+random.uniform(-.022,.065)+(.038 if mi>=6 else 0)),2)
  rows.append([month,sku,cat,name,bq,bp,bc,aq,ap,ac,round(bq*bp,2),round(aq*ap,2),round(bq*bc,2),round(aq*ac,2)])
expense_types=[('Payroll',135000,'Fixed'),('Rent & Facilities',38000,'Fixed'),('Marketing',45000,'Variable'),('Logistics',60000,'Variable'),('Technology',20000,'Fixed'),('General & Administrative',32000,'Fixed')]
expenses=[]
for mi,month in enumerate(months):
 for ex,amount,kind in expense_types:
  bud=round(amount*(1+.012*mi)*(1.18 if ex=='Marketing' and mi in [10,11] else 1),2)
  drift=(.09 if ex in ['Logistics','Marketing'] else .025)+random.uniform(-.085,.075)
  act=round(bud*(1+drift),2)
  expenses.append([month,ex,kind,bud,act])
# deterministic quality assertions
assert len(rows)==240 and len(expenses)==72
assert all(r[10]==round(r[4]*r[5],2) and r[11]==round(r[7]*r[8],2) for r in rows)
# write CSV reusable data
for file,headers,data in [('atlas_products.csv',['SKU','Category','Product','Base Price (USD)','Base Cost Ratio','Base Monthly Units'],products),('atlas_sales_monthly.csv',['Month','SKU','Category','Product','Budget Units','Budget Unit Price USD','Budget Unit Cost USD','Actual Units','Actual Unit Price USD','Actual Unit Cost USD','Budget Revenue USD','Actual Revenue USD','Budget COGS USD','Actual COGS USD'],rows),('atlas_opex_monthly.csv',['Month','Expense Category','Cost Type','Budget USD','Actual USD'],expenses)]:
 with open(f'{OUT}/{file}','w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(data)
wb=Workbook.create()
navy='#17243A'; blue='#215C89'; teal='#007F7D'; faint='#EAF3F6'
def sheet(name,headers,data,widths=None):
 s=wb.worksheets.add(name)
 n=len(headers); k=len(data)
 s.get_range_by_indexes(0,0,k+1,n).values=[headers]+data
 s.get_range_by_indexes(0,0,1,n).format={'fill':navy,'font':{'bold':True,'color':'#FFFFFF'},'row_height':31,'wrap_text':True}
 s.freeze_panes.freeze_rows(1)
 for j,w in enumerate(widths or [18]*n): s.get_range_by_indexes(0,j,k+1,1).format.column_width=w
 return s
readme=[['ATLAS CONSUMER GOODS | Synthetic FP&A Data Pack',''],['Dataset Version','1.0 | 2026-10-29'],['Company','Atlas Consumer Goods (fictional)'],['Industry','Consumer goods distribution (fictional)'],['Currency','USD | all numbers nominal'],['Period','2025 monthly | 12 months'],['Granularity','Month x SKU for sales; Month x expense category for OPEX'],['Origin','100% generated data. NO company records; NO UCI transaction rows copied.'],['Public inspiration','Online Retail II (UCI): general transactional structure and seasonal variation only'],['Source URL','https://archive.ics.uci.edu/dataset/502/online+retail+ii'],['Source attribution','Chen, D. (2012). Online Retail II, UCI. DOI: 10.24432/C5CG6D'],['Source license','CC BY 4.0 applies to original UCI dataset; this workbook uses no reproduced records'],['Model definition','Revenue = units x unit price; COGS = units x unit cost'],['Gross profit','Revenue - COGS'],['EBITDA proxy','Gross profit - operating expenses (excludes D&A, taxes, interest)'],['Sign convention','Revenue and costs positive in source; costs subtracted in P&L'],['Variance sign','Actual minus Budget; positive expense variance = unfavorable'],['Scenario rule','Budget is an independent synthetic baseline, not derived from Actual'],['Random seed','20261029 | deterministic generator'],['Caution','Illustrative education/portfolio project, not investment or commercial analysis'],['Future work','Forecast, price/volume/mix bridge, SKU profitability, scenario simulations'],['Model data URLs','Source URL is reference for methodology, not source of simulated numerical parameters']]
s=sheet('README',['Field','Description'],readme,[31,112]);s.get_range('B2:B23').format.wrap_text=True
p=sheet('Products',['SKU','Category','Product','Base Price USD','Base Cost Ratio','Base Monthly Units'],products,[13,25,37,19,20,23]);p.get_range('D2:D21').set_number_format('#,##0.00;[Red](#,##0.00);-');p.get_range('E2:E21').set_number_format('0.0%')
sales=sheet('Sales_Data',['Month','SKU','Category','Product','Budget Units','Budget Price USD','Budget Cost USD','Actual Units','Actual Price USD','Actual Cost USD','Budget Revenue USD','Actual Revenue USD','Budget COGS USD','Actual COGS USD'],rows,[13,13,26,36,18,19,19,18,19,19,23,23,22,22]);sales.get_range('E2:N241').set_number_format('#,##0.00;[Red](#,##0.00);-')
e=sheet('OPEX_Data',['Month','Expense Category','Cost Type','Budget USD','Actual USD'],expenses,[14,32,18,23,23]);e.get_range('D2:E73').set_number_format('#,##0;[Red](#,##0);-')
# DRE formula-driven aggregation monthly
DRE=['Month','Budget Revenue','Actual Revenue','Revenue Var','Budget COGS','Actual COGS','Budget Gross Profit','Actual Gross Profit','Budget OPEX','Actual OPEX','Budget EBITDA','Actual EBITDA','EBITDA Var','Budget GM %','Actual GM %']
d=sheet('Monthly_PnL',DRE,[[m]+[None]*14 for m in months],[16]+[19]*14)
fr=[]
for i in range(2,14):
 fr.append([None,
 f'=SUMIF(Sales_Data!$A$2:$A$241,A{i},Sales_Data!$K$2:$K$241)',
 f'=SUMIF(Sales_Data!$A$2:$A$241,A{i},Sales_Data!$L$2:$L$241)',
 f'=C{i}-B{i}',
 f'=SUMIF(Sales_Data!$A$2:$A$241,A{i},Sales_Data!$M$2:$M$241)',
 f'=SUMIF(Sales_Data!$A$2:$A$241,A{i},Sales_Data!$N$2:$N$241)',
 f'=B{i}-E{i}',f'=C{i}-F{i}',
 f'=SUMIF(OPEX_Data!$A$2:$A$73,A{i},OPEX_Data!$D$2:$D$73)',
 f'=SUMIF(OPEX_Data!$A$2:$A$73,A{i},OPEX_Data!$E$2:$E$73)',
 f'=G{i}-I{i}',f'=H{i}-J{i}',f'=L{i}-K{i}',f'=IFERROR(G{i}/B{i},0)',f'=IFERROR(H{i}/C{i},0)'])
d.get_range('B2:O13').formulas=[x[1:] for x in fr]
d.get_range('B2:M14').set_number_format('#,##0;[Red](#,##0);-');d.get_range('N2:O14').set_number_format('0.0%')
d.get_range('A14').values=[['FY 2025']]
for j in range(1,13):
 col=chr(65+j);d.get_range(f'{col}14').formulas=[[f'=SUM({col}2:{col}13)']]
d.get_range('N14').formulas=[['=IFERROR(G14/B14,0)']];d.get_range('O14').formulas=[['=IFERROR(H14/C14,0)']]
d.get_range('A14:O14').format={'fill':faint,'font':{'bold':True,'color':navy}}
# summary formulas and editable assumptions named in notes
summary=[['Metric','Budget FY25','Actual FY25','Variance','Interpretation'],['Revenue',None,None,None,'Actual - Budget (positive favorable)'],['Cost of Goods Sold',None,None,None,'Actual - Budget (positive unfavorable)'],['Gross Profit',None,None,None,'Actual - Budget (positive favorable)'],['Operating Expenses',None,None,None,'Actual - Budget (positive unfavorable)'],['EBITDA (proxy)',None,None,None,'Actual - Budget (positive favorable)'],['Gross Margin %',None,None,None,'Actual - Budget (percentage points)']]
a=sheet('Executive_Summary',summary[0],summary[1:],[28,24,24,24,60]);refs=[('B','C'),('E','F'),('G','H'),('I','J'),('K','L'),('N','O')]
for row,(b,c) in enumerate(refs,2):
 a.get_range(f'B{row}:D{row}').formulas=[[f'=Monthly_PnL!{b}14',f'=Monthly_PnL!{c}14',f'=C{row}-B{row}']]
a.get_range('B2:D6').set_number_format('#,##0;[Red](#,##0);-');a.get_range('B7:D7').set_number_format('0.0%')
a.get_range('A9').values=[['Quality checks']]
a.get_range('A10:B13').values=[['Sales rows',len(rows)],['OPEX rows',len(expenses)],['Number of SKUs',len(products)],['Periods',len(months)]]
a.get_range('A15').values=[['Model integrity: FY Revenue reconciles sales source']]
a.get_range('B15').formulas=[['=IF(ABS(C2-SUM(Sales_Data!L2:L241))<0.01,"PASS","FAIL")']]
a.get_range('A16').values=[['Model integrity: FY OPEX reconciles source']]
a.get_range('B16').formulas=[['=IF(ABS(C5-SUM(OPEX_Data!E2:E73))<0.01,"PASS","FAIL")']]
# model assumptions and data dictionary
assumptions=[['Currency','USD','Synthetic','All values generated, not converted from UCI GBP'],['Period','2025','Synthetic','Illustrative year not equal to reference dataset year'],['Product count',20,'Synthetic','4 categories x 5 products'],['Demand seasonal pattern','0.81–1.42x','Synthetic / UCI-inspired','Illustrative seasonal multipliers, NOT estimated UCI coefficients'],['Actual unit volume variation','-14% to +15% plus late-year adjustment','Synthetic','Per SKU-month seeded randomness'],['Actual pricing deviation','-5.5% to +3% plus midyear adjustment','Synthetic','Per SKU-month seeded randomness'],['Actual unit cost shock','+3.5% plus variable shocks','Synthetic','Higher after June, constructed for profitability analysis'],['Operating expense categories',6,'Synthetic','Fixed/variable classification is illustrative'],['Random seed',20261029,'Synthetic','Reproducibility of generator'],['Public reference','https://archive.ics.uci.edu/dataset/502/online+retail+ii','Source','General structure/sales seasonality inspiration; no empirical extraction']]
s=sheet('Assumptions',['Assumption','Value','Type','Notes'],assumptions,[31,65,28,85]);s.get_range('B2:B11').format.font.color='#0000FF'
dictrows=[['Products','SKU','Product identifier','Text','Synthetic'],['Products','Category','Merchandising category','Text','Synthetic'],['Sales_Data','Month','YYYY-MM month key','Text','Synthetic'],['Sales_Data','Budget Units / Actual Units','Units sold; budget and realized','Integer','Synthetic'],['Sales_Data','Budget Price / Actual Price USD','Selling price per unit','USD','Synthetic'],['Sales_Data','Budget Cost / Actual Cost USD','Cost of goods per unit','USD','Synthetic'],['Sales_Data','Budget Revenue / Actual Revenue USD','Quantity multiplied by selling unit price','USD','Calculated during source generation'],['Sales_Data','Budget COGS / Actual COGS USD','Quantity multiplied by unit cost','USD','Calculated during source generation'],['OPEX_Data','Expense Category','Operating cost grouping','Text','Synthetic'],['OPEX_Data','Budget USD / Actual USD','Positive expense values','USD','Synthetic'],['Monthly_PnL','Gross Profit','Revenue less COGS','USD','Calculated formula'],['Monthly_PnL','EBITDA','Gross Profit less OPEX; proxy','USD','Calculated formula']]
s=sheet('Data_Dictionary',['Sheet','Field','Meaning','Unit','Provenance'],dictrows,[22,37,68,18,43]);s.get_range('C2:C13').format.wrap_text=True
try:
 chart=d.charts.add('line',d.get_range('A1:C13'));chart.title_text='Monthly Budget vs Actual Revenue';chart.set_position('A17','H34')
except Exception as exc: print('Chart omitted:',repr(exc))
path=f'{OUT}/Atlas_Consumer_Goods_FP&A_Dataset_v1.xlsx'
SpreadsheetFile.export_xlsx(wb).save(path)
print('saved',path,os.path.getsize(path))
print('budget revenue',round(sum(r[10] for r in rows),2),'actual revenue',round(sum(r[11] for r in rows),2))
try:
 print('inspect',wb.inspect({'kind':'table','range':'Executive_Summary!A1:E7','include':'values,formulas','table_max_rows':8,'table_max_cols':5}).ndjson[:2200])
except Exception as ex: print('inspect failed',str(ex)[:500])
