from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, CalendarMainSerializer
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
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'DELETE', 'PUT'])
def detail_post(request, date):
    post = get_object_or_404(Post, expenses_date=date)
    print(date)

    if request.method == 'GET':
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # if is_post_owner(request.user, post.user):
    #     if request.method == 'PUT':
    #         serializer = PostSerializer(post, data=request.data, partial=True)

    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save(user=request.user)

    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #     elif request.method == 'DELETE':
    #         post.delete()
    #         return Response({'msg' : '게시글 삭제 완료'}, status=status.HTTP_200_OK)
    # else:
    #     return Response({'msg': '게시글 주인이 아님'})

@api_view(['GET'])
def post_list(request):
    year_month = request.query_params.get('yearMonth')
    user_post = Post.objects.filter(user=request.user, expenses_date__startswith=year_month)

    serializer = CalendarMainSerializer(user_post, many=True)

    return Response(serializer.data)


def is_post_owner(login_user, post_owner):
    if login_user == post_owner:
        return True
    else:
        return False