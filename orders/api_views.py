from rest_framework  import viewsets
from .models import Category, Sub_Category, Product, ProductLine, Customer, Order, OrderDetail, Payment, Comment, Attribute, AttributeValue
from .serializers import CategorySerializer, Sub_CategorySerializer, ProductSerializer, ProductLineSerializer, CustomerSerializer, OrderSerializer, OrderDetailSerializer, PaymentSerializer, CommentSerializer, AttributeSerializer, AttributeValueSerializer
##########################################################
#######                APIS                ###############
##########################################################
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Sub_CategoryViewSet(viewsets.ModelViewSet):
    queryset = Sub_Category.objects.all()
    serializer_class = Sub_CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductLineViewSet(viewsets.ModelViewSet):
    queryset = ProductLine.objects.all()
    serializer_class = ProductLineSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

class AttributeValueViewSet(viewsets.ModelViewSet):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
##########################################################