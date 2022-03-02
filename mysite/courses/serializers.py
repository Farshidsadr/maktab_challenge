from rest_framework import serializers

from .models import Course, Teacher, Review
from accounts.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    review_avg = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    def get_review_avg(self, obj):
        return obj.review_avg

    def get_review_count(self, obj):
        return obj.review_count

    class Meta:
        model = Course
        fields = "__all__"

    def validate(self, attrs):
        price = attrs.get("price", None)

        if not price:
            raise serializers.ValidationError("no-price")
        if price < 100000:
            raise serializers.ValidationError("low-price")
        return attrs


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = "__all__"


# ToDo: Add review and courselist serializers
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # if we don't need expanded version of course we can remove this line
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


# for courseList we can use courseSerializer in view with many=True, because serializer is responsible for serializing
# the data, so we can control data amount in view
class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ('teacher', )
