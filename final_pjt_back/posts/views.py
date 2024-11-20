from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Post
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'DELETE', 'PUT'])
def detail_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if is_post_owner(request.user, post.user):
        if request.method == 'PUT':
            serializer = PostSerializer(post, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)

                return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            post.delete()
            return Response({'msg' : '게시글 삭제 완료'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': '게시글 주인이 아님'})


def is_post_owner(login_user, post_owner):
    if login_user == post_owner:
        return True
    else:
        return False