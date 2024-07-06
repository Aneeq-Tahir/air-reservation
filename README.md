<h1 align="center">Air Reservation System</h1>

## Overview

The Air Reservation System is a RESTful API built with FastAPI for managing customers, flight tickets, flight schedules, and reservations. It allows users to perform CRUD (Create, Read, Update, Delete) operations on the following entities:

-  Customers
-  Flight Tickets
-  Schedules
-  Reservations

## Features

-  **Customer Management**: Create, read, update, and delete customer records.
-  **Flight Ticket Management**: Manage flight tickets, including creating new tickets, updating existing ones, and deleting tickets.
-  **Schedule Management**: Handle flight schedules by adding, updating, and removing schedules.
-  **Reservation Management**: Manage reservations, allowing users to book and manage their flight reservations.

## Endpoints

### Customers

-  **Create Customer**: `POST /customers/`
-  **Get All Customers**: `GET /customers/`
-  **Update Customer**: `PUT /customers/{customer_id}`
-  **Delete Customer**: `DELETE /customers/{customer_id}`

### Flight Tickets

-  **Create Flight Ticket**: `POST /flight_tickets/`
-  **Get All Flight Tickets**: `GET /flight_tickets/`
-  **Update Flight Ticket**: `PUT /flight_tickets/{ticket_id}`
-  **Delete Flight Ticket**: `DELETE /flight_tickets/{ticket_id}`

### Schedules

-  **Create Schedule**: `POST /schedules/`
-  **Get All Schedules**: `GET /schedules/`
-  **Update Schedule**: `PUT /schedules/{schedule_id}`
-  **Delete Schedule**: `DELETE /schedules/{schedule_id}`

### Reservations

-  **Create Reservation**: `POST /reservations/`
-  **Get All Reservations**: `GET /reservations/`
-  **Update Reservation**: `PUT /reservations/{reservation_id}`
-  **Delete Reservation**: `DELETE /reservations/{reservation_id}`

## Error Handling

All API endpoints include error handling to manage exceptions and provide meaningful error messages. If an error occurs during any operation, the transaction is rolled back, and an appropriate HTTP error response is returned.
