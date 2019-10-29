from django.shortcuts import redirect, get_object_or_404
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests, json
from .serializers import UserSerializer,FollowSerializer
from .models import User, payInfo, Follow

@api_view(['GET','POST'])
def follow_list(request):
    # follow 명단 조회 기능
    if request.method == 'GET':
        queryset = Follow.objects.all()
        serializer = FollowSerializer(queryset, many = True)
        return Response(serializer.data)
    
    # follow 연결기능
    elif request.method == 'POST':
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATE)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def follow_detail(request, pk):
    follow = get_object_or_404(Follow, pk=pk)
    # 특정 follow 조회 기능
    if request.method == 'GET':
        serializer = FollowSerializer(follow)
        return Response(serializer.data)
    # 특정 follow 수정 기능
    elif request.method == 'PUT':
        serializer = FollowSerializer(follow, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    # 특정 follow 삭제 기능
    elif request.method == 'DELETE':
        follow.delete()
        return Response(status=status.HTTP_204_NOT_CONTENT)
    
class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter    

class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter

@api_view(['POST'])
def userInfo(request):
    userId = request.data.get('id')
    if userId[0] == "k" or userId[0] == "n":
        userSet = User.objects.get(userId=userId)
    else:
        userSet = User.objects.get(pk=userId)
    serializer = UserSerializer(userSet)
    return Response(serializer.data)

@api_view(['POST'])
def userSave(request):
    ## 수정
    ### 프론트와 카카오가 통신
    ### 프론트는 백하고 통신
    userName = request.data.get('userName')
    userNickName = request.data.get("nickname")
    userId = request.data.get('userId')
    userSex = request.data.get('userSex')
    userAge = request.data.get("userAge")
    userImage = request.data.get('userImage')
    try: 
        userSet = User.objects.get(userId=userId)
    except:
        User.objects.create(
            userName=userName, userNickName=userName, userSex=userSex, userAge=userAge, userImage=userImage, userId=userId
        )
    return Response("database save")


@api_view(['POST'])
def editUser(request, id):
    user = User.objects.get(id=id)

    # 유저 프로필 수정
    ## 이미지
    ## 주소
    ## 선호 카테고리
    ## 닉네임
    pass
 
@api_view(['GET'])
def Naver_Login(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    clientId = 'IaquHgHTmPlf_gc_a8es'
    secretId = 'nUsvfl0B6c'
    apiUrl = "https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&"
    apiUrl += "client_id=" + clientId + "&client_secret=" + secretId + "&code=" + str(code) + "&state=" + str(state)
    response = requests.get(apiUrl)
    response = json.loads(response.text)
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    body = {
        'access_token': access_token,
        'code': code,
    }
    auth_response = requests.post("http://127.0.0.1:8000/accounts/rest-auth/naver/", data=body)
    auth_response = json.loads(auth_response.text)
    redirect_url = "http://localhost:8080"
    redirect_url += "?jwt=" + auth_response.get('token')

    headers = {
        'Authorization':'Bearer ' + access_token
    }
    profile_url = "https://openapi.naver.com/v1/nid/me"
    profile_response = requests.get(profile_url, headers=headers)
    profile_response = json.loads(profile_response.text)
    userName = profile_response.get("response").get("name")
    userNickName = profile_response.get("response").get("nickname")
    userId = "naver_" + str(profile_response.get("response").get("id"))
    userSex = profile_response.get("response").get("gender")
    userAge = profile_response.get("response").get('age')
    userImage = profile_response.get("response").get("profile_image")
    try: 
        userSet = User.objects.get(userId=userId)
    except:
        User.objects.create(
            userName=userName, userNickName=userName, userSex=userSex, userAge=userAge, userImage=userImage, userId=userId
        )
    userSet = User.objects.values().filter(userId=userId)
    serializer = UserSerializer(userSet)
    ids = userSet.get().get('id')
    redirect_url += "&id="+str(ids)
    return redirect(redirect_url)
    



@api_view(['POST'])
def kakaoPay(request):
    # request에 회원 id, 결제가격을 같이 보내줘야 함 : db에 결제정보를 저장하기 위해서
    url = "https://kapi.kakao.com"
    headers = {
        'Authorization': "KakaoAK " + "25f3b072b7bff63ee9a201aa1f5dc9d6",
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }
    params = {
        'cid': "TC0ONETIME",
        'partner_order_id': '1001',
        # 주문자 정보 id
        'partner_user_id': '',
        'item_name': '포인트',
        'quantity': 1,
        # 결제 금액
        'total_amount': 0,
        'vat_amount': 200,
        'tax_free_amount': 0,
        'approval_url': 'http://localhost:8080',
        'fail_url': 'http://localhost:8080',
        'cancel_url': 'http://localhost:8080',
    }
    params['partner_user_id'] = reqeust.data.get('userId')
    params['total_amount'] = request.data.get('amount')
    response = requests.post(url+"/v1/payment/ready", params=params, headers=headers)
    response = json.loads(response.text)
    if response.get('code'):
        # 에러일때 
        pass
    else:
        # 에러가 아닐 때
        # db저장
        # payInfo.objects.create(
        #     user=request.data.get('userId'), payNum=response.get('tid'), 
        #     payAmount=request.data.get('amount'), payDate=response.get('created_at')
        # )
        
        return Response(response)
    