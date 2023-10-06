from rest_framework import views
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

from .utils import calculateCreditScore, calculateEMIs, makePayment
from .serializers import UserSerializer,LoanSerializer
from .models import User,Loan,EMI
import threading


class IndexView(views.APIView):
    def get(self, request):
        return render(template_name='api/index.html',request=request)    



class UserRegisterView(views.APIView):
    serializer_class = UserSerializer

    def post(self,request):
        serializer = UserSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # calculateCreditScore(user.id)
        t1 = threading.Thread(target=calculateCreditScore,args=(user.id,))
        t1.start()
        
        return HttpResponse(f'unique_user_id: f{user.id}')


class LoanView(views.APIView):
    serializer_class = LoanSerializer

    def post(self,request):
        serializer = LoanSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        # print(serializer.data)
        
        user = User.objects.get(pk=request.POST['user_id'])
        # print(UserSerializer(user).data)
        if user.credit_score < 450 or user.anual_income < 150000:
            return HttpResponse("Error: Credit Score < 450  or anual_income < 150000")
        
        loanAmount = int(request.POST['loan_amount'])
        loanType = request.POST['loan_type']
        if(loanType == 'Personal' and loanAmount > 1000000) or (loanType == 'Home' and loanAmount > 8500000) or (loanType == 'Education' and loanAmount > 5000000) or(loanType == 'Car' and loanAmount > 750000):
            return HttpResponse("Error: Loan Amount Very High for the Type of Loan!")

        intrestRate = int(request.POST['intrest_rate'])/100
        months = int(request.POST['term_period'])
        if (loanAmount + (loanAmount*intrestRate)) / months > (0.60*(user.anual_income/12)) :
            return HttpResponse("EMI is more than 60 percent of the monthly income of the User")



        loan = serializer.save()
        calculateEMIs(loan.id)
        return HttpResponse(f'{loan.id}')


class StatementsView(views.APIView):
    serilizer_class = EMI

    def get(self,request):
        try:
            loan_id = request.GET['loan_id']
            loan = Loan.objects.get(pk = loan_id)    
            emis = EMI.objects.filter(loan_id=loan.id)
        except :
            return HttpResponse("Loan ID Does Not Exist")

        return render(
            request,
            'api/loan_statements.html',
            {
                "loan":loan,
                "emis" : emis,
            },
        )   


class PayView(views.APIView):
    def post(self,request):
        loan_id = request.POST['loan_id']
        amount = request.POST['amount']
        makePayment(loan_id,amount)
        return HttpResponse("EMI Payment Was Successfull")