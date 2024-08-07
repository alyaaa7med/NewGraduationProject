from itertools import chain
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings


from rest_framework import viewsets, pagination
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from .serializers import *
from .models import *
from accounts.models import *
from .permissons import UserPermission

class MessagesView(viewsets.ModelViewSet):
    search_fields = ['content']
    pagination.PageNumberPagination.page_size = 50 
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = MessageSerializer

    def get_queryset(self):
        curr_user = self.request.user

        if self.kwargs.get('user_id'):
            other_user = self.kwargs['user_id']
            criteria1 = Q(sender=curr_user) & Q(receiver=other_user)
            criteria2 = Q(sender=other_user) & Q(receiver=curr_user)
            latest = Message.objects.filter(criteria2)
            if latest.exists():
                latest = latest.last()
                latest.seen = True
                latest.save()
            return Message.objects.filter(Q(criteria1) | Q(criteria2))
        return Message.objects.all()

    def relatedUsers(self, request):
        curr_user = request.user
        
        # Get all users the current user has sent or received messages from
        related_users = User.objects.filter(
            Q(sent_messages__receiver=curr_user) | Q(received_messages__sender=curr_user)
        ).distinct()

        result_list = []

        for user in related_users:
            # Get the last message between the current user and the related user
            last_message = Message.objects.filter(
                Q(sender=curr_user, receiver=user) | Q(sender=user, receiver=curr_user)
            ).latest('created_at')

            # Get the profile image for the user
            profile_image_url = None
            profile_image = ProfileImage.objects.filter(user=user).first()
            if profile_image:
                profile_image_url = request.build_absolute_uri(profile_image.image.url)


            # Determine role and role ID of the related user
            user_role = 'guest'
            user_role_id = None

            if hasattr(user, 'doctor'):
                user_role = 'doctor'
                user_role_id = user.doctor.id
            elif hasattr(user, 'patient'):
                user_role = 'patient'
                user_role_id = user.patient.id
            
            # Create a dictionary containing user details, last message content, sender ID, and profile image URL
            user_data = {
                "id": user.id,
                "name": user.name,
                "last_message": last_message.content if last_message else None,
                "last_message_sender_id": last_message.sender.id if last_message else None,
                "last_message_seen": last_message.seen if last_message else None,
                "profile_image_url": profile_image_url,
                "user_role": user_role,
                "user_role_id": user_role_id
            }
            result_list.append(user_data)

        return JsonResponse(result_list, safe=False)
    
    def check(self, request):
        curr_user = request.user
        latestMessage = curr_user.received_messages.last()
        return JsonResponse({'new': not latestMessage.seen if latestMessage else False})

    def perform_create(self, serializer):
        receiver = User.objects.filter(id=self.kwargs['user_id']).first()
        serializer.save(sender=self.request.user, receiver=receiver)
        
        
