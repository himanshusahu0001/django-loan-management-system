# Loan Management System in Django 
 

## Create a Virtual Envoirnment  

```sh
$ python -m venv .venv
```
```sh
$ .venv/scripts/activate
```  
commands for linux,mac are diffrent. 

## Install all dependencies
```sh
$ pip install -r requirements.txt
```

## Create DataBase  and Run App

```sh
$ cd LoanManagementSystem
```
```sh
$ python manage.py makemigrations
```
```sh
$ python manage.py migrate 
```
```sh
$ python manage.py runserver
```
  
## API END-PONTS  
  
http://localhost:8000/

### Home  (access all functionalities from here)   
[GET req]
-  api/ -- Home for app  
  
### Register User For a Valid Adhar ID in Transactions.csv  
[POST req]
-  api/register-user/ -- User-Register-API  

### Apply For Loan by valid User ID
[POST req]
-  api/apply-loan/ -- Loan-Application-API   

### Get All Statements For a Loan ID  
[GET req]
-  api/get-statement/ -- Get-Loan-Statements-API   

### Make EMI Payment For a Loan ID  
[POST req]
-  api/make-payment/ -- EMI-Payment-API    
  



## DataBase Schema

an overview of the Django models defined in the project.

### User Model

- id
- name
- adhar_id
- email
- annual_income
- credit_score

### Transactions Model

- id
- adhar_id
- transaction_type
- amount

### Loan Model

- id
- user_id
- loan_type
- loan_amount
- interest_rate
- term_period
- disbursement_date

### EMI Model

- id
- loan_id
- emi_date
- emi_amount
- paid_amount
- isPaid
