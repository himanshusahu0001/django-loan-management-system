from django.db.models import Sum
from .models import User,Transactions,Loan,EMI
import csv
import os
import datetime

def calculateCreditScore(user_id):
    addTrasactions()
    user = User.objects.get(id=user_id)
    user_adhar_id = user.adhar_id

    debited = Transactions.objects.filter(adhar_id = user_adhar_id, transaction_type='DEBIT').aggregate(Sum("amount"))
    credited = Transactions.objects.filter(adhar_id = user_adhar_id, transaction_type='CREDIT').aggregate(Sum("amount"))
    debited = debited['amount__sum']
    credited = credited['amount__sum']

    if debited==None: debited = 0
    if credited==None: credited = 0

    account_balance = int(credited-debited)
    print(account_balance)
    credit_score_calculated = 300

    if(account_balance <= 100000):
        credit_score_calculated = 300
    elif(account_balance >= 1000000):
        credit_score_calculated = 900
    else:
        credit_score_calculated = 300 + (round((account_balance-100000)/15000) * 10)

    user.credit_score = credit_score_calculated    
    user.save()



def addTrasactions():
    if len(Transactions.objects.all()) == 0:
        current_path = os.path.dirname(__file__)
        csv_path = os.path.join(current_path, 'data.csv')
        with open( csv_path ,"r") as csv_file:
            next(csv_file)
            reader = csv.reader(csv_file)
            for row in reader:
                transaction = Transactions(
                    adhar_id = row[0],
                    transaction_type = row[2] ,
                    amount = row[3]
                )
                transaction.save()
    

def calculateEMIs(cur_loan_id):
    loan = Loan.objects.get(pk=cur_loan_id)
    loanAmount = loan.loan_amount
    intrestRate = loan.intrest_rate
    monthlyIntrest = intrestRate/12/100
    months = loan.term_period

    current_datetime = datetime.datetime.combine((loan.disbursement_date),datetime.time())
    print(loan.disbursement_date)
    current_year = current_datetime.year
    current_month = current_datetime.month

    installment_amount = round(loanAmount*monthlyIntrest * ( (1+monthlyIntrest)**months)/(((1+monthlyIntrest)**months)-1) ) 
    
    for i in range(0,months):
        current_month+=1
        if current_month > 12 :
            current_month= current_month%12
            current_year = current_year+1
        emi = EMI(
            loan_id = loan,
            emi_date=  datetime.datetime(current_year,current_month,1),
            emi_amount=  installment_amount,
        )
        emi.save()

def makePayment(cur_loan_id, paidAmount):
    emis = EMI.objects.filter(loan_id=cur_loan_id, isPaid=False).order_by('emi_date')
    emi = emis[0]
    emi.isPaid = True
    emi.paid_amount = paidAmount
    if(len(emis) > 1):
        diffrence  = (int(emi.emi_amount) - int(paidAmount))/(len(emis)-1) 
    else:
        emi.isPaid = False
        emi.paid_amount = 0
        emi.emi_amount = int(emi.emi_amount) - int(paidAmount)
    emi.save()
    for i in range(1,len(emis)):
        emis[i].emi_amount += diffrence
        emis[i].save()   
    
    
