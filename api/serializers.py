from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'stock',
        )

        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError("Price must be greater than 0.")
            return value


class OrderItemSerializer(serializers.ModelSerializer):
    # This will work out of the box because it is named the same as field in the OrderItem model
    # product = ProductSerializer()

    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        model = OrderItem
        fields = (
            # "product",
            'product_name',
            'product_price',
            "quantity",
            # refer the @property on the model OrderItem
            'item_subtotal'
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    # the name mus be the same as the SerializerMethodField field or pass method_name
    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            "order_id",
            "created_at",
            'user',
            'status',
            'items',
            'total_price',
        )


class ProductInfoSerializer(serializers.Serializer):
    # serializer that is not linked to model
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
