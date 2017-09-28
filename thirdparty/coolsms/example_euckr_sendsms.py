# -*- coding: cp949 -*-

"""
 vi:set et ts=4 fenc=cp949:
 Copyright (C) 2008-2010 D&SOFT
 http://open.coolsms.co.kr
"""

import sys
import coolsms



def main():
    # 객체 생성
    cs = coolsms.sms()

    # 프로그램명과 버젼을 입력합니다. (생략가능)
    cs.appversion("TEST/1.0")

    # 한글인코딩 방식을 설정합니다.  (생략시 euckr로 설정)
    # 지원 인코딩: euckr, utf8
    cs.charset("euckr")

    # 아이디와 패스워드를 입력합니다.
    # 쿨에스엠에스에서 회원가입시 입력한 아이디/비밀번호를 입력합니다.
    cs.setuser("cova", "abc123")

    # add("받는사람 폰번호", "보내는사람 폰번호", "문자 내용", "예약전송시간")
    # "예약전송시간"을 생략 하거나 현재 시간보다 이전시간으로 설정하면 즉시 전송 됨
    # 예약전송 표기법 : YYYYMMDDhhmmss (YYYY=년, MM=월, DD=일, hh=시, mm=분, ss=초)
    # String 으로 표기하며 ss(초)는 생략 가능

    # 즉시 전송시
    cs.addsms("01028429981", "01028429981", "80바이트 이내로 문자내용을 입력하세요. 80바이트 이후의 내용은 자동으로 잘립니다.")
    # 예약 전송시
    #cs.addsms("01012341234", "0212341234", "80바이트 이내로 문자내용을 입력하세요. 80바이트 이후의 내용은 자동으로 잘립니다.", "YYYYMMDDhhmm")
    # cs.addsms 메소드를 계속 호출하여 메시지를 추가 할 수 있음.

    nsent = 0
    if cs.connect():
        # add 된 모든 메세지를 서버로 보냅니다.
        nsent = cs.send()
    else:
        # 오류처리
        print "서버에 접속할 수 없습니다. 네트워크 상태를 확인하세요."

    # 연결 해제
    cs.disconnect()

    # 결과를 출력합니다.
    print "%d 개를 전송한 결과입니다." % nsent
    cs.printr()
 
    # 메모리 초기화
    cs.emptyall()

if __name__ == "__main__":
    main()
    sys.exit(0)
