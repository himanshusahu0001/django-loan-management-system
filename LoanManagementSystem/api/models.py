from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    name = models.CharField(max_length=50)
    adhar_id = models.CharField(max_length=50,unique=True)
    email = models.EmailField()
    anual_income = models.BigIntegerField()
    credit_score = models.IntegerField(default=300)

    # def __str__(self):
    #     # return str(self.__dict__)
    #     return f"adhar_id: {self.adhar_id}"

class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    adhar_id = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=10)
    amount = models.IntegerField()

class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=30)
    loan_amount = models.IntegerField()
    intrest_rate = models.IntegerField()
    term_period = models.IntegerField(default=0)
    disbursement_date = models.DateField()

class EMI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    loan_id = models.ForeignKey(Loan,on_delete=models.CASCADE)
    emi_date = models.DateField()
    emi_amount = models.IntegerField()
    paid_amount = models.IntegerField(default=0)
    isPaid = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.emi_date}'