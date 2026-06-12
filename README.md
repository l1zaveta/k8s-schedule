# Лабораторная работа №7: Развёртывание приложения в Kubernetes

**Выполнили:** Грищук Е.Д., Красноперова Е.Д., Лаузер Я.П.  

---

## Описание

Развёртывание информационной системы управления расписанием учебных занятий (ИС «Расписание») с использованием Kubernetes (minikube). В рамках работы настроено автомасштабирование подов (HPA) и мониторинг кластера через Prometheus + Grafana.

---

## Требования
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)

Установка инструментов (macOS):
```bash
brew install minikube kubectl helm
```

---

## Шаг 1 — Запуск minikube

```bash
minikube start --driver=docker --cpus=2 --memory=4096
minikube status
kubectl get nodes
```

---

## Шаг 2 — Сборка Docker-образа

```bash
eval $(minikube docker-env)

cd app
docker build -t schedule-app:latest .

docker images | grep schedule-app
```

---

## Шаг 3 — Создание Deployment (3 пода)

```bash
kubectl apply -f k8s/deployment.yaml

kubectl get pods
kubectl get deployments
```

---

## Шаг 4 — Установка Metrics Server

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

kubectl patch deployment metrics-server -n kube-system \
  --type=json \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'

kubectl get pods -n kube-system | grep metrics-server
kubectl top nodes
```

---

## Шаг 5 — Настройка HPA

```bash
kubectl autoscale deployment my-app --cpu-percent=50 --min=2 --max=5

# Проверка
kubectl get hpa
```

HPA автоматически масштабирует количество подов от 2 до 5 при превышении 50% CPU.

---

## Шаг 6 — Установка Prometheus + Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

kubectl get pods -n monitoring
```

---

## Шаг 7 — Открытие Grafana

```bash
# Получаем пароль
kubectl get secret -n monitoring prometheus-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode

# Пробрасываем порт
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

Открываем в браузере: [http://localhost:3000](http://localhost:3000)  
Логин: `admin`  
Пароль: из команды выше

### Импорт дашборда

1. Dashboards - Import
2. В поле ввести ID: `15661`
3. Нажать **Load**
4. Выбрать datasource: `prometheus`
5. Нажать **Import**

---
### Демонстрация работы - https://drive.google.com/drive/folders/1pJozq_o3FdjUWlFWS180h9YnjyFQsQux?usp=sharing    


