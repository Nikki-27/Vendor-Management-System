# Vendor-Management-System

Develop a Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics.

## Setup Instructions:

**Clone the repository:**

```
git clone https://github.com/Nikki-27/Vendor-Management-System
```

**Install dependencies:**

```
pip install -r requirements.txt
```

**Apply migrations:**

```
python manage.py migrate
```

**Create a superuser:**

```
python manage.py createsuperuser

```

**Run the development server:**

```
python manage.py runserver

```

**Token generation:**

```
curl -X POST -d "username=your_superuser_username&password=your_superuser_password" http://localhost:8000/api-token-auth/
```

## **Testing API Endpoints:**

1. **Vendor Profile Management Endpoints:**

   ```
   # Create a new vendor
   curl -H "Authorization: Token <token>" -X POST http://localhost:8000/api/vendors/ -d "name=Vendor1&contact_details=Contact1&address=Address1"

   # List all vendors
   curl -H "Authorization: Token <token>" -X GET http://localhost:8000/api/vendors/

   # Retrieve a specific vendor's details
   curl -H "Authorization: Token <token>" -X GET http://localhost:8000/api/vendors/<vendor_id>/

   # Update a vendor's details
   curl -H "Authorization: Token <token>" -X PUT http://localhost:8000/api/vendors/<vendor_id>/ -d "name=NewVendorName"

   # Delete a vendor
   curl -H "Authorization: Token <token>" -X DELETE http://localhost:8000/api/vendors/<vendor_id>/

   ```
2. **Purchase Order Tracking Endpoints:**

   ```
   # Create a purchase order
   curl -H "Authorization: Token <token>" -X POST http://localhost:8000/api/purchase_orders/ -d "po_number=01&vendor=<vendor_id>&order_date=2023-01-01T12:00:00&delivery_date=2023-01-10T12:00:00&items=[{\"item_name\":\"Item1\",\"quantity\":10},{\"item_name\":\"Item2\",\"quantity\":10}]&status=completed&acknowledgment_date=2024-01-02T12:00:00"

   # List all purchase orders
   curl -H "Authorization: Token <token>" -X GET http://localhost:8000/api/purchase_orders/

   # List all purchase orders for a specific vendor
   curl -H "Authorization: Token <token>" -X GET http://localhost:8000/api/purchase_orders/?vendor=<vendor_id>

   # Retrieve details of a specific purchase order
   curl -H "Authorization: Token <token>" -X GET http://localhost:8000/api/purchase_orders/<po_id>/

   # Update a purchase order
   curl -H "Authorization: Token <token>" -X PUT http://localhost:8000/api/purchase_orders/<po_id>/ -d "status=canceled"

   # Delete a purchase order
   curl -H "Authorization: Token <token>" -X DELETE http://localhost:8000/api/purchase_orders/<po_id>/

   ```


3. **Vendor Performance Evaluation Endpoint:**

   ```
   # Retrieve a vendor's performance metrics
   curl -H "Authorization: Token <token>" -X GET http://localhost:8000/api/vendors/<vendor_id>/performance
   ```
4. ## Update acknowledgment_data


   ```
   curl -H "Authorization: Token your_obtained_token" -X PATCH http://127.0.0.1:8000/api/purchase_orders/{po_id}/acknowledge/ --data "acknowledgment_date=2023-12-30T12:00:00Z"
   ```
