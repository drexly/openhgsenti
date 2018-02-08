# openhgsenti
공개 한국어 감성 검색 엔진

## OSS World Challenge 2017 제 11회 공개SW개발자대회 결선작

## 응용 SW 부문 팀 김주현 - 김주현

http://project.oss.kr/board/noticeView.do?board_seq=826

![http://openhg.ml](/finalround.png?raw=true "최종결선")

## 소프트웨어 소개

한국어 문장 혹은 단어를 입력하면 단어나 문장이 가지는 감정 정도(긍정-부정)와 매칭 되는 영화 장르(28가지) 순을 시각화 하고 그에 따른 근거 또한 통계적 그래프로 시각화 해서 보여준다.  집단 감성 정도를 수치로 산출하기 위해 1천만 건에 가까운 인터넷 영화 평점들 마다 각 해당 영화에서 차지하는 신뢰도를 전체 공감-비 공감 수 기준 소프트맥스 함수를 통해 정량적으로 계측 하여 반영한다. 반영의 근거가 되는 인터넷 영화 평점들은 주기적으로 업데이트 하기 때문에 한국어 감성 검색 엔진은 시대에 따라 집단 지성 및 감성을 기계 학습한다. 현재 대한민국에 공개된 한국어 감성 사전이 없고 과거에 있었다 하더라도 한국어 단어의 긍정-부정 수치를 신뢰도 없이 객관식의 의도적인 설문조사를 통해서만 결정하였으며, 본 엔진처럼 다방면(28가지 매칭 장르)에서 한국어 감성 댓글 작성자들의 자발적이고 주관적인 평가 댓글 작성에 대한 통계 분석과, 각 댓글에 대한 다른 사용자들의 공감-비공감 평가가 반영되지 않아 감성 분석 신뢰도 측면에서 부족한 면이 있었다. 무엇보다 해당 서비스가 중지 (http://openhangul.com/restrict) 되었기에 이를 해결하고자 개발하였으며, 웹 어플리케이션뿐만 아니라 JSON Open API를 통해 회원가입만 하면 누구나 오픈 한국어 감성 사전을 사용할 수 있게 설계하여 한글 자연어 처리 연구 및 현재 걸음마 단계에 있는 인공지능의 한글 자연어 감성 분석 성능 향상에 공공적으로 기여한다.

## 논문 Korea Software Congress 2017 Accepted AI Paper with Award in Paper Contest

학부생논문-인공지능: 리뷰 데이터의 신뢰도를 반영한 한국어 감성사전

https://www.eiric.or.kr/community/post2.php?m=view&gubun=201710&num=12855

KSC2017 학부생/주니어논문경진대회 입상자 명단 - 장려상 수상 NO.432

http://www.kiise.or.kr/academy/board/academyNewsView.fa?MENU_ID=080100&NUM=1644

## 실 사용 예 Actual API Usage

![http://openhg.ml](/pptimg/use.png?raw=true "실례")


## 사이트: http://openhg.ml

접속 안될 경우: http://175.123.137.223:6969


## 동영상: https://youtu.be/3lgYaszL1Pg
[![클릭하세요](http://i3.ytimg.com/vi/3lgYaszL1Pg/hqdefault.jpg)](https://youtu.be/3lgYaszL1Pg)

위 사진을 클릭하시고 720p 이상으로 보세요
* * *
## Python3 Django web framework 기반 (elasticsearch database server는 용량 관계상 생략. Raw contents: https://github.com/drexly/movie140reviewcorpus)

### other dependencies

pip3 install django-bootstrap-themes

pip3 install django-ipware

pip3 install elasticsearch

pip3 install json

### run web application

python manage.py runserver 0.0.0.0:5959

* * *
## Final Round Presentation

![http://openhg.ml](/pptimg/ppt_1.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_2.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_3.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_4.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_5.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_6.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_7.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_8.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_9.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_10.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_11.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_12.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_13.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_14.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_15.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_16.png?raw=true "최종심사ppt")
![http://openhg.ml](/pptimg/ppt_17.png?raw=true "최종심사ppt")


