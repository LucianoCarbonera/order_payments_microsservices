from locust import HttpUser, TaskSet, task, between
import random

class UserBehavior(TaskSet):

    def on_start(self):
        """Essa função é executada quando um usuário simulado inicia."""
        self.order_id = None

    @task(1)
    def create_order(self):
        response = self.client.post("/orders/create/", {
            "product_name": "Produto Teste",
            "quantity": random.randint(1, 5),  # Quantidade aleatória
            "price": random.uniform(10.00, 100.00)  # Preço aleatório
        })

        # Salva o ID do pedido recém-criado para ser usado no pagamento
        if response.status_code == 302:  # Verifica se a criação foi bem-sucedida
            self.order_id = response.headers["Location"].split("/")[-2]

    @task(2)
    def create_payment(self):
        if self.order_id:
            self.client.post("/payments/create/", {
                "order_id": self.order_id,  # Usa o ID do pedido criado
                "amount": random.uniform(10.00, 100.00)  # Valor aleatório
            })
        else:
            # Caso nenhum pedido tenha sido criado, tenta criar um novo pedido
            self.create_order()

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
    host = "http://localhost:8000"