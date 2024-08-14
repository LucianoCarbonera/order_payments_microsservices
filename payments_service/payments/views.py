from django.shortcuts import render, redirect
from django.views import View
from .models import Payment

class CreatePaymentView(View):
    def get(self, request):
        return render(request, 'payments/payment_form.html')

    def post(self, request):
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')

        if not order_id or not amount:
            # Caso algum campo esteja vazio, retornar um erro ou uma mensagem ao usuário
            return render(request, 'payments/payment_form.html', {
                'error_message': 'Por favor, preencha todos os campos.'
            })

        try:
            # Tenta converter o valor para um Decimal, para evitar erros de entrada
            amount = float(amount)
        except ValueError:
            return render(request, 'payments/payment_form.html', {
                'error_message': 'Por favor, insira um valor válido para o pagamento.'
            })

        # Cria e salva o pagamento no banco de dados
        payment = Payment(order_id=order_id, amount=amount)
        payment.save()

        return redirect('payments_list')

class PaymentsListView(View):
    def get(self, request):
        payments = Payment.objects.all()
        return render(request, 'payments/payments_list.html', {'payments': payments})
