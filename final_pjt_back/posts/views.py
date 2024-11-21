from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, CalendarMainSerializer, PostDetailSerializer, CommentSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Post, Comment
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        # print(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def detail_post(request):
    date = request.GET.get('date')
    post = get_list_or_404(Post, expenses_date=date)

    if request.method == 'GET':
        serializer = PostDetailSerializer(post, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    if is_owner(request.user, post.user):
        if request.method == 'PUT':
            serializer = PostDetailSerializer(post, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)

                return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            post.delete()
            return Response({'msg' : '게시글 삭제 완료'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': '게시글 주인이 아님'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list(request):
    year_month = request.query_params.get('yearMonth')
    user_post = Post.objects.filter(user=request.user, expenses_date__startswith=year_month)

    serializer = CalendarMainSerializer(user_post, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    print(request.data)
    
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request):
    # GET 요청에서 쿼리 파라미터 추출
    expenses_date = request.query_params.get('expenses_date')
    author_user_pk = request.query_params.get('author_user_pk')

    if not expenses_date or not author_user_pk:
        return Response({'error': '필수 파라미터가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        comments = Comment.objects.filter(expenses_date=expenses_date, author_user_pk=author_user_pk)
        
        if not comments.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = CommentSerializer(comments, many=True)
        # print(comments)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    new_content = request.data.get('content')

    if not comment_id or not new_content:
        return Response({'error': '댓글 ID와 수정할 내용이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        comment = get_object_or_404(Comment, id=comment_id)

        if not is_owner(request.user, comment.user):
            return Response({'error': '댓글 작성자만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        comment.content = new_content
        comment.save()

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    if not comment_id:
        return Response({'error': '댓글 ID가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        comment = get_object_or_404(Comment, id=comment_id)

        if not is_owner(request.user, comment.user):
            return Response({'error': '댓글 작성자만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({'msg': '댓글 삭제 완료'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)

        if not is_owner(request.user, post.user):
            return Response({'error': '게시글 작성자만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({'message': '게시글이 삭제되었습니다.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def is_owner(login_user, post_owner):
    if login_user == post_owner:
        return True
    else:
        return False