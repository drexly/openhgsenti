# -*- coding: utf8 -*-

"""
 vi:set et ts=4 fenc=utf8:
 Copyright (C) 2008-2010 D&SOFT
 http://open.coolsms.co.kr
"""

import sys
import coolsms



def main():
    # 객체생성
    cs = coolsms.sms()

    # 프로그램명과 버젼을 입력합니다. (생략가능)
    cs.appversion("TEST/1.0")

    # 한글인코딩 방식을 설정합니다.  (생략시 euckr로 설정)
    # 지원 인코딩: euckr, utf8
    cs.charset("utf8")

    # 아이디와 패스워드를 입력합니다.
    # 쿨에스엠에스에서 회원가입시 입력한 아이디/비밀번호를 입력합니다.
    cs.setuser("cs_id", "cs_passwd")

    # Local 메시지ID를 생성합니다.
    localkey = cs.keygen()

    # local 메시지ID 로 메시지를 전송합니다.
    # (msgid 를 입력하지 않는 경우 서버에서 메시지ID를 생성해서 리턴합니다.)
    cs.addsms("01012341234", "0212341234", "Local Message ID 테스트", msgid=localkey)

    if cs.connect():
        # add 된 모든 메세지를 서버로 보냅니다.
        cs.send()
    else:
        # 오류처리
        print "서버에 연결할 수 없습니다."

    # 연결 해제
    cs.disconnect()

    # 접수결과를 가져옵니다.
    result = cs.getr()

    # 결과를 출력합니다.
    for i in range(len(result)):
        x = result[i]
        print "Called Number: " + x["CALLED-NUMBER"]
        print "Message ID: " + x["MESSAGE-ID"]
        print "Result Code: " + x["RESULT-CODE"]
        print "Result Message: " + x["RESULT-MESSAGE"]

    # 메모리 초기화
    cs.emptyall()

if __name__ == "__main__":
    main()
    sys.exit(0)
