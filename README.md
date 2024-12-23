## 영화 예매 플랫폼 MovieGet

##  🔗 시연영상
> ### [MovieGet]
(https://youtu.be/u4rKml1W8B8?si=ehg0NeekxEHaKRS2)

---

## 프로젝트 기간
> ### 2024.10.10 - 2024.11.05

---

## 프로젝트 소개
> **MovieGet** </br>
> ### Megabox, 롯데시네마, CGV를 바탕으로 실제 영화 예매 시스템과 밀접하게 서비스를 구현하였습니다.
> 📌 TMDB의 영화 상영 데이터를 가공하여 데이터를 생성하였고</br>
> 📌 이를 통해 회원들이 실제와 같은 영화 예매를 경험할 수 있습니다.</br>
>

<p align="center">
<img width="428" src="https://github.com/user-attachments/assets/de957fc1-92a4-4a46-92f4-01e14c5c1247">
</p>
<p align="center">메인 페이지-상영 영화 TOP10, 상영 예정 영화</p>
<p align="center">
<img width="428" src="https://github.com/user-attachments/assets/7251124c-3eef-4030-95a9-9fcdf077ba39">
</p>
<p align="center">예매 페이지-좌석 선택</p>

<p align="center">
<img width="428" src="https://github.com/user-attachments/assets/cf67ba62-77db-441c-a473-8e74195d4cdd">
</p>
<p align="center">결제 페이지-tosspay 연동</p>

<br>

## ✅ 주요기능

### 1️⃣ TMDB -> 영화데이터
> 
> 영화 포스터, 예고편, 출연진 정보 등 다양한 정보를 제공합니다.</br>
> Open API를 활용해서 공신력 있는 데이터를 수급하였습니다.

### 2️⃣ 예매
>
> 사용자가 날짜를 선택하면 영화, 지역, 영화관, 상영시간 정보를 제공합니다. </br>
> 상영관 별 동적 좌석 데이터를 생성하여 상영관 별로 다른 좌석 데이터를 보유하고 있으며 실시간 좌석 선택이 가능합니다.</br>
> 영화 상영 시간, 인원 수, 좌석 데이터 선택 후 예매 데이터를 생성합니다.

### 3️⃣ 결제
>
> 결제 전 포인트 적립 및 포인트를 사용해 결제할 수 있습니다. </br>
> 결제 시스템으로 tosspay를 연동하였습니다.(사업자 등록 시에 다양한 테스트가 가능합니다.)

## ✅ 그 외 기능

### 1️⃣ 소셜로그인
>
> 사용자는 소셜로그인(카카오)을 통해 로그인을 할 수 있습니다. 

### 2️⃣ 마이페이지
>
> 개인정보 수정이 가능합니다.</br>
> 회원 본인의 예매 or 취소 내역을 당일/7일 이내/전체로 설정하여 볼 수 있습니다.
> 회원 본인의 포인트 이용 or 적립 내역을 당일/7일 이내/전체로 설정하여 볼 수 있습니다.
> 회원 본인의 리뷰 전체를 볼 수 있습니다.
> 찜한 영화 데이터 조회 및 예매페이지로 이동이 가능합니다.
> 회원 탈퇴시 회원의 정보가 데이터베이스에서 삭제됩니다.

### 3️⃣ 리뷰
>
> 영화를 예매한 회원의 경우 300자 이내의 Text와 사진을 첨부할 수 있습니다.
> 리뷰 작성 시 별점을 줄 수 있으며 이 별점은 평균 평점으로 작용됩니다.
> 리뷰 작성 시 30점의 포인트가 적립됩니다.

### 4️⃣ 포인트
>
> 영화 예매 시 100point, 리뷰 작성 시 20point가 적립됩니다.
> 예매 취소 or 리뷰 삭제 시 적립되었던 포인트가 삭제됩니다.
> 결제 시 적립되었던 포인트를 1000point부터 사용 가능합니다.

### 5️⃣ 별점
> 회원은 영화를 본 후 리뷰를 적을 때 1-5점 사이로 별점을 부여할 수 있습니다.
> 별점은 모든 페이지에 나오는 영화 데이터의 아래부분에 평균 별점으로 나타납니다.

### 6️⃣ 찜하기
> 회원/비회원 모두 맘에 드는 영화에 하트 모양을 눌러 찜하기를 할 수 있습니다.
> 찜하기는 간편 예매로 이동하기 위한 수단으로 마이페이지에서 찜한 영화들을 볼 수 있습니다.> 회원은 영화를 본 후 리뷰를 적을 때 1-5점 사이로 별점을 부여할 수 있습니다.
> 별점은 모든 페이지에 나오는 영화 데이터의 아래부분에 평균 별점으로 나타납니다.

<br></br>
## 1. 백엔드팀

| <a href="https://github.com/skwwnl"><img src="https://avatars.githubusercontent.com/u/57902567?v=4" width=450px/><br/><sub><b>skwwnl</b></sub></a> | <a href="https://github.com/hyo00000"><img src="https://avatars.githubusercontent.com/u/173426190?v=4" width=300px/><br/><sub><b>hyo00000</b></sub></a> | <a href="https://github.com/Gseungjin2"><img src="https://avatars.githubusercontent.com/u/173425102?v=4" width=270px/><br/><sub><b>Gseungjin2</b></sub></a> | <a href="https://github.com/woojin-an"><img src="https://avatars.githubusercontent.com/u/173426123?v=4" width=400px/><br/><sub><b>woogin-an</b></sub></a> | <a href="https://github.com/raphaehell"><img src="https://avatars.githubusercontent.com/u/173425827?v=4" width=300px/><br/><sub><b>raphaehell</b></sub></a> |
| :--------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------: |
| 김진원 | 김효영 | 강승진 | 안우진 | 정회인 |

<br></br>

## 2. 개발 환경

### Backend

> <img src="https://img.shields.io/badge/fastapi-009688?style=flat-square&logo=fastapi&logoColor=white"/>
> <img src="https://img.shields.io/badge/terraform-0986567?style=flat-square&logo=terraform&logoColor=white"/>
> <img src="https://img.shields.io/badge/redis-FF4438?style=flat-square&logo=redis&logoColor=white"/>
> <img src="https://img.shields.io/badge/mongodb-47A248?style=flat-square&logo=mongodb&logoColor=white"/>
> <img src="https://img.shields.io/badge/Mysql-4169E1?style=flat-square&logo=mysql&logoColor=white"/>
> <img src="https://img.shields.io/badge/fastapi-009688?style=flat-square&logo=fastapi&logoColor=white"/>

### Deployment
>
> <img src="https://img.shields.io/badge/github actions-2088FF?style=flat-square&logo=githubactions&logoColor=white"/>
> <img src="https://img.shields.io/badge/Amazon AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white"/>
</br>

### Environment
> <img src="https://img.shields.io/badge/github-181717?style=flat-square&logo=github&logoColor=white"/>
> <img src="https://img.shields.io/badge/git-F24E1E?style=flat-square&logo=git&logoColor=white"/>

### Communication
> <img src="https://img.shields.io/badge/figma-F24E1E?style=flat-square&logo=figma&logoColor=white"/>
> <img src="https://img.shields.io/badge/notion-181717?style=flat-square&logo=notion&logoColor=white"/>
> <img src="https://img.shields.io/badge/discord-5865F2?style=flat-square&logo=discord&logoColor=white"/></br>


<br> </br>

## 3. 시작 가이드

### 설치 전 요구 사항

- Python 3.12.3
- fastapi 0.115.2
- tortoise-orm 0.21.6
- Poetry 1.8.3

### 설치

``` bash
$ git clone https://github.com/movieget/backend.git
$ cd backend
$ poetry install
```

#### 실행

```bash
$ poetry shell
$ cd src
$ fastapi dev main.py
$ [or] python main.py
```

## 4. ERD, 시스템 아키텍처 및 프로젝트 구조

### ERD

<img width="6769" alt="MovieGet" src="https://github.com/user-attachments/assets/dfce7bfd-3314-431c-806b-547ce22a1d80" />

<br></br>

### 시스템 아키텍처

<img width="6769" alt="MovieGet" src="https://github.com/user-attachments/assets/0ec7b038-e6e7-48e6-9582-384aecb22422" />

<br></br>

### 프로젝트 구조
```
backend
├─ .dockerignore
├─ .git
├─ .github
│  └─ workflows
│     ├─ CD.yml 
│     └─ CI.yml
├─ .gitignore
├─ .gitmessage.txt
├─ Dockerfile
├─ infra
├─ poetry.lock
├─ pyproject.toml
├─ README.md
├─ scripts
├─ src
│  ├─ app
│  │  ├─ api
│  │  ├─ auth
│  │  └─ v1
│  │     ├─ alert
│  │     ├─ book
│  │     ├─ cinema
│  │     ├─ favorite
│  │     ├─ location
│  │     ├─ movie
│  │     ├─ payment
│  │     ├─ refund
│  │     ├─ review
│  │     ├─ screen
│  │     └─ user
│  ├─ common
│  ├─ core
│  └─ main.py
└─ terraform

```