
# Delivery Service

The Delivery Service is one of the three independent microservices in the **Food Delivery Microservices** application.

It is responsible for managing delivery records, assigning delivery personnel, and tracking delivery status.

---

## 1. Overview

The Delivery Service handles the delivery-related operations of the food delivery application.

It provides REST APIs for:

- Creating delivery records
- Retrieving delivery details
- Assigning delivery personnel
- Updating delivery status
- Checking the current delivery status

The service runs independently and communicates with the **Order Service** as part of the complete order-processing workflow.

---

## 2. Responsibilities

The Delivery Service is responsible for the following operations:

- Create a new delivery
- Store delivery information
- Retrieve delivery details
- Assign a delivery person
- Update delivery status
- Track the current status of a delivery
- Provide delivery information to other services through REST APIs

---

## 3. Technology Used

| Technology | Purpose |
|---|---|
| Python | Service implementation |
| Flask | REST API framework |
| REST API | Service communication |
| Docker | Containerization |
| Docker Compose | Multi-service deployment |

---

## 4. Service Port

The Delivery Service runs on:

```text
5001
````

When running locally:

```text
http://localhost:5001
```

---

## 5. API Endpoints

| Method | Endpoint                  | Description                          |
| ------ | ------------------------- | ------------------------------------ |
| GET    | `/`                       | Returns Delivery Service information |
| POST   | `/deliveries`             | Creates a new delivery               |
| GET    | `/deliveries/<id>`        | Retrieves delivery details           |
| PUT    | `/deliveries/<id>/assign` | Assigns delivery personnel           |
| PUT    | `/deliveries/<id>/status` | Updates delivery status              |
| GET    | `/deliveries/<id>/status` | Retrieves current delivery status    |

---

## 6. Delivery Status

The Delivery Service supports the following delivery states:

```text
PENDING
ASSIGNED
PICKED_UP
OUT_FOR_DELIVERY
DELIVERED
```

The delivery status is updated through the status API according to the supported status transitions.

### Delivery Flow

```text
PENDING
   ↓
ASSIGNED
   ↓
PICKED_UP
   ↓
OUT_FOR_DELIVERY
   ↓
DELIVERED
```

---

## 7. API Testing

The Delivery Service was tested using its REST API endpoints.

### 7.1 Delivery Service Running

The Delivery Service was started successfully on port `5001`.

![Delivery Service Running](../screenshots/Delivery%20Service%20Running.png)

---

### 7.2 Create Delivery

A new delivery record can be created using:

```text
POST /deliveries
```

The following screenshot shows the successful creation of a delivery record.

![Create Delivery](../screenshots/Create%20Delivery.png)

---

### 7.3 Delivery Data

The delivery information returned by the service can be viewed through the API response.

![Delivery Data](../screenshots/Delivery%20Data.png)

---

### 7.4 Delivery Status

The current delivery status can be retrieved using:

```text
GET /deliveries/<id>/status
```

The following screenshot shows the delivery status response.

![Delivery Status](../screenshots/Delivery%20Status.png)

---

## 8. Running the Service Locally

### Step 1: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 2: Start the Service

Run:

```bash
python app.py
```

The service will start on:

```text
http://localhost:5001
```

---

## 9. Running with Docker

The Delivery Service contains its own `Dockerfile`, allowing it to be built and executed independently.

### 9.1 Build the Docker Image

```bash
docker build -t delivery-service .
```

The Docker image was successfully built for the Delivery Service.

![Build the Docker Image](../screenshots/Build%20the%20Docker%20Image%20of%20delivery%20service.png)

---

### 9.2 Run the Container

```bash
docker run -p 5001:5001 delivery-service
```

The service will then be accessible at:

```text
http://localhost:5001
```

---

## 10. Docker Compose Deployment

The Delivery Service is also deployed together with the Restaurant Service and Order Service using Docker Compose.

The three services are connected through a common Docker network.

```text
food-delivery-network
```

### Service Communication

```text
                    Food Delivery Application
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
      Restaurant         Order Service    Delivery Service
       Service              :5002             :5001
        :5000                 │
                              │
                    Creates Delivery
                              │
                              ▼
                     Delivery Service
```

---

## 11. Role in the Overall System

The Delivery Service works with the **Order Service** during order processing.

When a new order is created:

1. The Order Service receives the order request.
2. The Order Service validates the restaurant and menu item using the Restaurant Service.
3. The Order Service creates the order.
4. The Order Service requests the Delivery Service to create a delivery.
5. The Delivery Service creates a delivery record.
6. The delivery starts with the `PENDING` status.
7. The delivery status can then be updated through the Delivery Service APIs.

### Interaction Flow

```text
Customer
   │
   ▼
Order Service
   │
   ├──────────────► Restaurant Service
   │                Validate Restaurant/Menu
   │
   ▼
Create Order
   │
   └──────────────► Delivery Service
                    Create Delivery
                         │
                         ▼
                      PENDING
```

---

## 12. Inter-Service Communication

When the application is deployed using Docker Compose, the Order Service communicates with the Delivery Service using the Docker service name.

```text
Order Service
     │
     │ HTTP Request
     ▼
http://delivery-service:5001
     │
     ▼
Delivery Service
```

This allows the services to communicate through the Docker network without depending on container IP addresses.

---

## 13. Delivery Data

A delivery record contains information required for tracking the delivery.

Example:
![Delivery Data](../screenshots/Delivery%20Data.png)

T

---

## 14. Project Structure

```text
delivery-service/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
│
└── tests/
    └── test_delivery.py
```

---

## 15. Testing

The Delivery Service includes tests for validating its functionality.

Test file:

```text
tests/test_delivery.py
```

The tests are used to verify the behaviour of the Delivery Service APIs.

---

## 16. Docker Integration

The Delivery Service is integrated into the complete application using Docker Compose.

The application contains three independent services:

```text
Restaurant Service
       │
       │
       ▼
   Order Service
       │
       │
       ▼
 Delivery Service
```

Each service has:

* Its own application code
* Its own dependencies
* Its own Dockerfile
* Its own API endpoints
* Independent service responsibilities

---

## 17. Key Features

* Independent delivery management service
* REST API based communication
* Delivery creation and retrieval
* Delivery personnel assignment
* Delivery status tracking
* Docker containerization
* Docker Compose integration
* Inter-service communication with Order Service
* API testing
* Automated testing support

---

## 18. Conclusion

The Delivery Service provides an independent component for managing delivery operations in the Food Delivery Microservices application.

It demonstrates how a specific business responsibility can be separated into an independent microservice with its own APIs, Docker container, and service logic.

The service also participates in inter-service communication with the Order Service, demonstrating the interaction between multiple microservices in the complete application.

````
