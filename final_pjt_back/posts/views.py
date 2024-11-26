from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, CalendarMainSerializer, PostDetailSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Post, Comment, Category
from accounts.models import Budget
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth
from datetime import datetime, timedelta

User = get_user_model()

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
    # GET 요청으로 전달받은 yearMonth 값
    year_month = request.query_params.get('yearMonth')
    # print("현재 날짜!!!!!!!!!!!!! ", year_month)
    if not year_month:
        return Response({"error": "yearMonth parameter is required"}, status=400)

    # 현재 유저의 Post 중 expenses_date가 year_month로 시작하는 데이터 필터링
    user_posts = Post.objects.filter(user=request.user, expenses_date__startswith=year_month)

    # 전체 price 칼럼 값 합산
    total_price = user_posts.aggregate(total_price=Sum('price'))['total_price'] or 0

    # 모든 카테고리를 가져옴
    all_categories = Category.objects.all()

    # 카테고리별 price 합산 (없으면 기본값 0)
    category_totals = []
    for category in all_categories:
        category_total = user_posts.filter(category=category).aggregate(total_price=Sum('price'))['total_price'] or 0
        category_totals.append({
            "category_name": category.category_name,
            "total_price": category_total
        })

    # 직렬화된 데이터 반환
    serializer = CalendarMainSerializer(user_posts, many=True)

    response_data = {
        "posts": serializer.data,
        "total_price": total_price,  # 전체 합산된 가격 추가
        "category_totals": category_totals,  # 모든 카테고리 포함한 합계 추가
    }
    
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    # print(request.data)
    
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


def category_list(request):
    categories = Category.objects.all().values('id', 'category_name')  # 필요한 필드만 가져오기
    return JsonResponse(list(categories), safe=False)  # JSON 데이터 반환


def is_owner(login_user, post_owner):
    if login_user == post_owner:
        return True
    else:
        return False
    

def graph_data(request):
    date_param = request.GET.get('date')
    login_user_id = request.GET.get('loginUser')

    if not date_param or not login_user_id:
        return JsonResponse({'error': 'Both date and loginUser parameters are required'}, status=400)

    try:
        end_year, end_month = map(int, date_param.split('-'))
        end_date = datetime(end_year, end_month, 1)
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM.'}, status=400)

    try:
        user = get_object_or_404(User, pk=login_user_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid user ID format.'}, status=400)

    six_months_ago = end_date - timedelta(days=30 * 5)
    start_year, start_month = six_months_ago.year, six_months_ago.month


    post_data = (
        Post.objects
        .filter(user=user)
        .annotate(year=ExtractYear('expenses_date'), month=ExtractMonth('expenses_date'))
        .filter(
            expenses_date__year__gte=start_year,
            expenses_date__month__gte=start_month,
            expenses_date__year__lte=end_year,
            expenses_date__month__lte=end_month
        )
        .values('year', 'month')
        .annotate(total_expenses=Sum('price'))
    )

    budget_data = (
        Budget.objects
        .filter(user=user)
        .filter(
            year__gte=start_year,
            month__gte=start_month,
            year__lte=end_year,
            month__lte=end_month
        )
        .values('year', 'month')
        .annotate(total_budget=Sum('amount'))
    )

    result = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if (year == start_year and month < start_month) or (year == end_year and month > end_month):
                continue

            post_total = next((p['total_expenses'] for p in post_data if p['year'] == year and p['month'] == month), 0)

            budget_total = next((b['total_budget'] for b in budget_data if b['year'] == year and b['month'] == month), 0)

            result.append({
                'date': f"{year}-{month:02d}",
                'budget': budget_total,
                'total_value': post_total,
            })

    return JsonResponse(result, safe=False)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, post_id):
    # print(request.data)
    try:
        # 게시글 가져오기
        post = get_object_or_404(Post, id=post_id)

        # 작성자 확인 (is_owner 함수 활용)
        if not is_owner(request.user, post.user):
            return Response({'error': '게시글 작성자만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        # 데이터 검증 및 업데이트
        serializer = PostSerializer(post, data=request.data, partial=True)  # partial=True로 일부 필드만 업데이트 가능
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': '게시글이 수정되었습니다.', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)