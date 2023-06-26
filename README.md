# aws_mfa
aws_mfa를 사용하면 Access Key에 대한 MFA 인증을 간소화 할 수 있습니다.

대화형으로 만들어진 aws_mfa는, 실행하는 서버의 `~/.aws/credentials` 경로에 존재하는 모든 profile list를 가져와서 사용자가 원하는 profile을 선택할 수 있도록 합니다. 선택한 profile이 mfa 디바이스 등록이 되어있는 유효한 profile이라면, aws_mfa가 중간 과정을 대신 수행하고 사용자는 알맞은 mfa code만 입력하면 됩니다.

## Installation:
```
1. Clone this repo
2. Run below command

# chmod +x aws_mfa/aws_mfa.py
# cp aws_mfa/aws_mfa.py /usr/local/bin/aws_mfa.py
# sudo mv aws_mfa/aws_mfa.py /usr/local/bin/aws_mfa

3. Let's use aws_mfa
```

## Prerequsite
aws_mfa를 사용하기 위해서는 mfa 디바이스 등록이 완료된 User의 Access Key가 credential file에 등록되어 있어야합니다.

aws credential은 대괄호(`[]`)로 표시된 섹션으로 저장되고 구분됩니다.<br>`[]`를 기준으로 다중 profile을 관리하고 사용할 수 있습니다.<br>
설정된 profile이 없다면 기본적으로 `default`라는 profile이 사용됩니다.

credentails 파일의 예시는 다음과 같습니다.
```
[example]
aws_access_key_id = AAAAAAAAAAAAAAAAAAA
aws_secret_access_key = aaaaaaaaaaaaaaaaaaaa

[foobar]
aws_access_key_id = BBBBBBBBBBBBBBBBBBB
aws_secret_access_key = bbbbbbbbbbbbbbbbbbbb
```

aws-mfa로 `foobar` profile의 mfa인증을 수행하면 다음과 같이 변경됩니다.<br>
(인증 완료 후에 `foobar-mfa`라는 이름으로 profile이 자동 생성됩니다. 이미 존재하는 profile은 업데이트 됩니다.)
```
[example]
aws_access_key_id = AAAAAAAAAAAAAAAAAAA
aws_secret_access_key = aaaaaaaaaaaaaaaaaaaa

[foobar]
aws_access_key_id = BBBBBBBBBBBBBBBBBBB
aws_secret_access_key = bbbbbbbbbbbbbbbbbbbb

[foobar-mfa] #이 섹션이 추가됨
aws_access_key_id = CCCCCCCCCCCCCCCCCCC
aws_secret_access_key = cccccccccccccccccccc
aws_session_token = cccccccccccccccccccc
```