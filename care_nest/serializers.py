from rest_framework import serializers
from .models import (
    Child, 
    ChildAchievements,
    Attendance,
    Section
    )

# ------ Child  ----------#

class ChildSerializer(serializers.ModelSerializer): 
    owner_username = serializers.CharField(source='owner.username', read_only=True) # to get the username of the parent from User => owner
    class Meta:
        model = Child
        fields = '__all__'

    def create(self, validated_data):
        owner = validated_data.get('owner') # in adding for if the admin add a child and assign it to a parent it will assign it in the post, to avoid geeting the admin as owner
        if not owner:
            raise serializers.ValidationError({'owner': 'Please select a parent'})
        return Child.objects.create(**validated_data)
        
class ChildNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id', 'first_name', 'last_name']

# ------ Child Achivements  ----------#

class ChildAchievementsSerializer(serializers.ModelSerializer): 
    child = ChildNameSerializer(read_only=True)  # Nested relations: https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    child_id = serializers.PrimaryKeyRelatedField( # PrimaryKeyRelatedField may be used to represent the target of the relationship using its primary key: https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield
        queryset=Child.objects.all(), #https://www.django-rest-framework.org/api-guide/relations/#the-queryset-argument
        write_only=True 
    )

    class Meta:
        model = ChildAchievements
        fields = '__all__'
        
    #https://www.django-rest-framework.org/api-guide/serializers/#writing-create-methods-for-nested-representations
    def create(self, validated_data):
        child = validated_data.pop('child_id')
        return ChildAchievements.objects.create(child=child, **validated_data)

    def update(self, instance, validated_data):
        child = validated_data.pop('child_id', None)
        if child:
            instance.child = child

        instance.achievement_type = validated_data.get(
            'achievement_type',
            instance.achievement_type
            )
        instance.title = validated_data.get(
            'title', 
            instance.title
            )
        instance.description = validated_data.get(
            'description', 
            instance.description
        )
        instance.image_url = validated_data.get(
            'image_url', 
            instance.image_url
            )

        instance.save()
        return instance
    
# ------ Attendance ----------#

class AttendanceSerializer(serializers.ModelSerializer): 
    child_full_name = serializers.SerializerMethodField() #https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    section = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = ['id', 'child', 'child_full_name', 'date', 'enter_time', 'exit_time', 'status', 'section']
    
    def get_child_full_name(self, obj):
        return f"{obj.child.first_name} {obj.child.last_name}"
    
    def get_section(self, obj):
        return obj.child.section.id if obj.child and obj.child.section else None

# ------ sections ----------#
class SectionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Section
        fields = '__all__'
