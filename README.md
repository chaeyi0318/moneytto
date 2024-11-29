<div align="center">

<a href="" target="_blank" title="Go to our website"><img width="196px"> <h1>🐸</h1> </a>
<a name="readme-top"></a>

# 10-pjt

소비의 시각화부터 맞춤형 재정 조언까지 당신의 금융친구 머니또!

</div>

### 프로젝트 개요

- 설명 :
- 기간 : 2024.11.18(월) ~ 2024.11.26(화)

<br>
<br>

### 🦾 팀 소개

| 송지영                                      | 손채이                                       |
| ------------------------------------------- | -------------------------------------------- |
| <a href="https://github.com/xongeeuse"></a> | <a href="https://github.com/chaeyi0318"></a> |
| 팀장                                         | 팀원                              |
|                                             |                                              |

<br>
<br>

### 🦿 성과

- 삼성청년SW아카데미 1학기 관통 프로젝트

<br />

### ERD
![alt text](머니또_ERD.png)

<br>
<br>


### ⚙ 주요 기능
| **카테고리**        | **기능**           | **설명**                                                                                                                                              |
|---------------------|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| **회원**            | 회원가입          | 아이디, 비밀번호, 닉네임, 이메일 입력<br>회원가입 완료 시 생년월일, 보유자산, 월수입을 입력할 수 있는 페이지로 이동                                         |
|                     | 로그인 / 로그아웃  | 아이디와 비밀번호가 일치하지 않을 시 로그인 실패 알림<br>아이디, 비밀번호 입력 후 로그인 완료 시 메인 페이지로 이동                                            |
|                     | 마이페이지         | 프로필 이미지, 닉네임, 생년월일, 월수입, 보유 자산 수정 가능<br>프로필 이미지가 없는 경우 기본 이미지 제공<br>비밀번호 확인 후 회원 탈퇴 완료<br>적금 상품 상세보기에서 찜한 상품 목록 확인<br>풀었던 퀴즈 내역 확인 |
| **가계부**          | 가계부             | 해당 날짜에 게시글 이미지 표시<br>가계부를 기록하면 해당 날짜에 유저가 게시글을 작성할 때 첨부한 이미지 표시<br>달력에 있는 이미지 클릭 시 게시글 상세보기<br>한 날짜에 게시글을 여러 개 등록 가능<br>게시글에 댓글 작성, 수정, 삭제<br>게시글 수정, 삭제 |
|                     | 소비 분석          | 설정한 예산 대비 소비금액에 따른 경고 표시<br>카테고리별 소비 내역을 나타낸 원형 차트 제공<br>각 달의 예산 대비 총 소비 금액 분석                              |
| **적금**            | 적금 상품          | 적금 목표액, 적금 예정 기간, 이자 계산 방식, 금융 권역을 설정하여 조건에 맞는 상품 검색<br>최고 이율 상품을 우선순위로 추천하고 내림차순으로 보기<br>적금 상품 상세보기에서 마음에 드는 상품 찜 가능 및 유저의 적금 상품 보유 여부 표시<br>가입하려는 가계부 연동이 있는 경우 추천 상품 제공<br>적금 상품 상세보기에서 해당 상품의 페이지로 이동 가능 |
| **금융 AI 비서**    | 구매 결정 조언     | 금융 정보를 바탕으로 현재 소비자의 예산과 소비 금액 대비 합리적인 소비인지 분석                                                                          |
|                     | 금융 퀴즈          | 금융과 관련된 OX 퀴즈를 통해 포인트 획득 가능 / 획득한 포인트는 금융 AI 비서를 이용할 때 사용                                                               |

<br>

## 🛒 기술 스택

### Backend

![Django](https://img.shields.io/badge/Django-092E20.svg?style=for-the-badge&logo=django&logoColor=white)&nbsp;
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)&nbsp;
![sqlite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=nodedotjs&logoColor=white)&nbsp;

### Frontend

![Vue.js](https://img.shields.io/badge/vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)&nbsp;

### DevOps

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)&nbsp;
![Github](https://img.shields.io/badge/Github-000000?style=for-the-badge&logo=github&logoColor=white)&nbsp;

### Tools

![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white)&nbsp;
![VS code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)&nbsp;
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)&nbsp;
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)&nbsp;

<br />

## 🔧 개발 환경

**Backend**

- django 4.2.16


**Frontend**

- vue.js 3.3.4
