# -*- coding: utf8 -*-

"""
 vi:set et ts=4 fenc=utf8:
 Copyright (C) 2008-2010 D&SOFT
 http://open.coolsms.co.kr
"""

import sys
import coolsms



def main():
    # 객체를 생성합니다.
    cs = coolsms.sms()

    # 프로그램명과 버젼을 입력합니다. (생략가능)
    cs.appversion("TEST/1.0")

    # 한글인코딩 방식을 설정합니다.  (생략시 euckr로 설정)
    # 지원 인코딩: euckr, utf8
    cs.charset("utf8")

    # 아이디와 패스워드를 입력합니다.
    cs.setuser("cs_id", "cs_passwd")

    # 서버에 접속합니다.
    if cs.connect():
        # 보유크레딧을 조회합니다.
        result = cs.remain();
    else:
        # 오류처리
        print "서버에 접속할 수 없습니다."

    # 연결을 끊습니다.
    cs.disconnect()

    # 결과를 출력합니다.
    if result["RESULT-CODE"] == "00":
        print "캐쉬:" + result["CASH"]
        print "포인트:" + result["POINT"]
        print "문자방울:" + result["DROP"]
        print "전체 SMS 건수:" + result["CREDITS"]
    else:
        print "Result Code: " + result["RESULT-CODE"]
        print "Result Message: " + result["RESULT-MESSAGE"]


if __name__ == "__main__":
    main()
    sys.exit(0)
