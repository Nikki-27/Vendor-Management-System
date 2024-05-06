from datetime import timezone
from rest_framework import generics, permissions
from .models import vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Define a class-based view for creating and listing vendors
class VendorListCreate(generics.ListCreateAPIView):
    # Specify authentication and permission classes
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Define the queryset and serializer class
    queryset = vendor.objects.all()
    serializer_class = VendorSerializer

# Define a class-based view for retrieving, updating, and deleting vendors
class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # Specify authentication and permission classes
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Define the queryset and serializer class
    queryset = vendor.objects.all()
    serializer_class = VendorSerializer

# Define a class-based view for creating and listing purchase orders
class PurchaseOrderListCreate(generics.ListCreateAPIView):
    # Specify authentication and permission classes
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Define the queryset and serializer class
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

# Define a class-based view for retrieving, updating, and deleting purchase orders
class PurchaseOrderRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    # Specify authentication and permission classes
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Define the queryset and serializer class
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

# Define a class-based view for retrieving vendor performance metrics
class VendorPerformance(generics.RetrieveAPIView):
    # Specify authentication and permission classes
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Define the queryset and serializer class
    queryset = vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'pk'

    # Override the retrieve method to return vendor performance metrics
    def retrieve(self, request, *args, **kwargs):
        # Get the vendor instance
        instance = self.get_object()
        # Get the serializer instance
        serializer = self.get_serializer(instance)
        # Calculate and return vendor performance metrics
        performance_metrics = {
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating_avg': instance.quality_rating_avg,
            'response_time_avg': instance.average_response_time,
            'fulfillment_rate': instance.fulfillment_rate
        }
        return Response(performance_metrics)

# Define a class-based view for updating purchase order acknowledgment dates
class AcknowledgePurchaseOrder(generics.UpdateAPIView):
    # Specify authentication and permission classes
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Define the queryset and serializer class
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'pk'

    # Override the update method to update acknowledgment dates and calculate average response time
    def update(self, request, *args, **kwargs):
        # Get the purchase order instance
        instance = self.get_object()
        # Get the acknowledgment date from the request data
        acknowledgment_date = request.data.get('acknowledgment_date')
        # Update the acknowledgment date if provided, otherwise set it to the current time
        if acknowledgment_date:
            instance.acknowledgment_date = acknowledgment_date
        else:
            instance.acknowledgment_date = timezone.now()
        # Save the updated purchase order instance
        instance.save()
        
        # Calculate the average response time for the vendor
        response_times = PurchaseOrder.objects.filter(
            vendor=instance.vendor, 
            acknowledgment_date__isnull=False
        ).values_list('acknowledgment_date', 'issue_date')
        
        total_seconds = sum((ack_date - issue_date).total_seconds() for ack_date, issue_date in response_times)
        average_response_time = total_seconds / len(response_times) if response_times else 0
        
        # Update the vendor's average response time
        instance.vendor.average_response_time = average_response_time
        instance.vendor.save()
        
        # Return the updated acknowledgment date
        return Response({'acknowledgment_date': instance.acknowledgment_date})