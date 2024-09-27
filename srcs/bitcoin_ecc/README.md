#bitcoin_ecc

## Preface
비트코인 public key, private key 생성을 하는 타원곡선 알고리즘 구현 디렉토리입니다
학습 코드는 `https://github.com/jimmysong/programmingbitcoin`의 원본 코드를 공부합니다

## SetUp
**Linux Ubuntu 22.04.3 LTS** 사용합니다
```bash
# 파이썬3 설치
$ python3 get-pip.py

# 해당 교재의 소스 코드를 clone 합니다
$ git clone https://github.com/jimmysong/programmingbitcoin
$ cd programmingbitcoin

# 가상환경 
$ pip install virtualenv --user
$ virtualenv -p python3 .venv
$ . .venv/bin/activate
(.venv) $ pip install -r requirements.txt
(.venv) $ jupyter notebook

```