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
    cs.setuser("cs_id", "cs_passwd")

    if cs.connect():
        # 전송상태를 읽어옵니다.
        # keygen() 으로 생성한 로컬 메시지ID(또는 그룹ID) 혹은
        # 서버에서 생성된 메시지ID(또는 그룹ID)를 입력합니다.

        #- 메시지ID로 예약 취소시
        result = cs.cancel("20101021133888234878558637");

        #- 그룹ID로 예약 취소시
        result = cs.groupcancel("20101021133888234878558637");
    else:
        # 오류처리
        print "서버에 연결할 수 없습니다."

    # 연결 해제
    cs.disconnect()

    # 결과를 출력합니다.
    print "Result Code: " + result["RESULT-CODE"]
    print "Result Message: " + result["RESULT-MESSAGE"]

    # 메모리 초기화
    cs.emptyall()


if __name__ == "__main__":
    main()
    sys.exit(0)
