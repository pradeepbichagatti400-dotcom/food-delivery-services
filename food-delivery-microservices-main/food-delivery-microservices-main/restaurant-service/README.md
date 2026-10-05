
# Restaurant Service

The Restaurant Service is one of the three independent microservices in the **Food Delivery Microservices** application.

It is responsible for managing restaurant information, menu details, and availability information.

---

## 1. Overview

The Restaurant Service handles the restaurant-related operations of the food delivery application.

It provides REST APIs for:

- Retrieving restaurant information
- Listing restaurants
- Retrieving restaurant details
- Retrieving restaurant menus
- Retrieving individual menu items
- Checking restaurant availability
- Checking menu item availability

The service runs independently and provides restaurant and menu information required during order processing.

---

## 2. Responsibilities

The Restaurant Service is responsible for the following operations:

- Provide restaurant information
- List restaurants
- Retrieve restaurant details
- Provide restaurant menu information
- Retrieve individual menu items
- Check restaurant availability
- Check menu item availability
- Return appropriate error responses when a restaurant or menu item is not found

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

The Restaurant Service runs on:

```text
5000
````

When running locally:

```text
http://localhost:5000
```

---

## 5. API Endpoints

| Method | Endpoint                                        | Description                            |
| ------ | ----------------------------------------------- | -------------------------------------- |
| GET    | `/`                                             | Returns Restaurant Service information |
| GET    | `/restaurants`                                  | Lists all restaurants                  |
| GET    | `/restaurants/<id>`                             | Retrieves restaurant details           |
| GET    | `/restaurants/<id>/menu`                        | Retrieves the restaurant menu          |
| GET    | `/restaurants/<id>/menu/<item_id>`              | Retrieves a specific menu item         |
| GET    | `/restaurants/<id>/availability`                | Checks restaurant availability         |
| GET    | `/restaurants/<id>/menu/<item_id>/availability` | Checks menu item availability          |

---

## 6. Restaurant and Menu Data

The Restaurant Service maintains sample restaurant and menu information.

### Restaurant 101

```text
Restaurant ID : 101
Name          : Pizza House
Location      : Hubli
Available     : Yes
```

Menu:

| Item ID | Name             | Price | Availability |
| ------: | ---------------- | ----: | ------------ |
|       1 | Margherita Pizza |  ₹250 | Available    |
|       2 | Farmhouse Pizza  |  ₹300 | Available    |
|       3 | Garlic Bread     |  ₹150 | Unavailable  |

### Restaurant 102

```text
Restaurant ID : 102
Name          : South Indian Kitchen
Location      : Hubli
Available     : Yes
```

Restaurant 102 currently has an empty menu.

---

## 7. API Testing

The Restaurant Service was tested using its REST API endpoints.

### 7.1 Restaurant Service Running

The Restaurant Service was started successfully on port `5000`.

![Restaurant Service Running](../screenshots/Restaurant%20Service%20Running.png)

---

### 7.2 Restaurant Menu

A restaurant menu can be retrieved using:

```text
GET /restaurants/<id>/menu
```

For example:

```text
GET /restaurants/101/menu
```

The following screenshot shows the restaurant menu returned by the service.

![Restaurant Menu](../screenshots/Restaurant%20Menu.png)

---

### 7.3 Item Availability

The availability of an individual menu item can be checked using:

```text
GET /restaurants/<id>/menu/<item_id>/availability
```

For example:

```text
GET /restaurants/101/menu/1/availability
```

The following screenshot shows the item availability response.

![Item Availability](../screenshots/Item%20Availability.png)

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
http://localhost:5000
```

---

## 9. Running with Docker

The Restaurant Service contains its own `Dockerfile`, allowing it to be built and executed independently.

### 9.1 Build the Docker Image

```bash
docker build -t restaurant-service .
```

The Docker image can be built independently for the Restaurant Service.

### 9.2 Run the Container

```bash
docker run -p 5000:5000 restaurant-service
```

The service will then be accessible at:

```text
http://localhost:5000
```

---

## 10. Docker Compose Deployment

The Restaurant Service is deployed together with the Order Service and Delivery Service using Docker Compose.

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
        Service              :5002              :5001
         :5000
             │
             │
             ▼
      Restaurant Data
      Menu Information
      Availability
```

---

## 11. Role in the Overall System

The Restaurant Service provides restaurant and menu information during order processing.

When a new order is created:

1. The Order Service receives the order request.
2. The Order Service contacts the Restaurant Service.
3. The Restaurant Service validates the requested restaurant.
4. The Restaurant Service validates the requested menu item.
5. The Restaurant Service provides availability information.
6. The Order Service continues processing when the requested item is valid and available.

### Interaction Flow

```text
Customer

   │

   ▼

Order Service

   │

   │ Request Restaurant/Menu Information

   ▼

Restaurant Service

   │

   ├──────────────► Restaurant Details
   │
   ├──────────────► Menu Details
   │
   └──────────────► Availability

   │

   ▼

Order Service
```

---

## 12. Inter-Service Communication

When the application is deployed using Docker Compose, the Order Service communicates with the Restaurant Service using the Docker service name.

```text
Order Service

     │

     │ HTTP Request

     ▼

http://restaurant-service:5000

     │

     ▼

Restaurant Service
```

This allows the services to communicate through the Docker network without depending on container IP addresses.

---

## 13. Restaurant Data

A restaurant record contains information such as restaurant ID, name, location, and availability.

Example:

```json
{
    "restaurant_id": 101,
    "name": "Pizza House",
    "location": "Hubli",
    "available": true
}
```

---

## 14. Project Structure

```text
restaurant-service/

│

├── app.py

├── Dockerfile

├── requirements.txt

├── README.md

│

└── tests/

    └── test_restaurant.py
```

---

## 15. Testing

The Restaurant Service includes tests for validating its functionality.

Test file:

```text
tests/test_restaurant.py
```

The tests are used to verify the behaviour of the Restaurant Service APIs.

---

## 16. Docker Integration

The Restaurant Service is integrated into the complete application using Docker Compose.

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

* Independent restaurant management service
* REST API based communication
* Restaurant information retrieval
* Restaurant listing
* Restaurant menu retrieval
* Individual menu item retrieval
* Restaurant availability checking
* Menu item availability checking
* Docker containerization
* Docker Compose integration
* Inter-service communication with Order Service
* API testing
* Automated testing support

---

## 18. Conclusion

The Restaurant Service provides an independent component for managing restaurant and menu-related operations in the Food Delivery Microservices application.

It demonstrates how restaurant functionality can be separated into an independent microservice with its own APIs, Docker container, and service logic.

The service also participates in inter-service communication with the Order Service, providing restaurant, menu, and availability information during order processing.

---
