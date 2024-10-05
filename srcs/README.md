# 프로젝트 코드 설명서

이 프로젝트는 Python으로 작성된 코드로, 필요한 라이브러리와 환경 설정에 대한 설명을 포함합니다. 이 설명서는 프로젝트를 실행하기 위한 단계별 가이드를 제공합니다.

## 파일 설명

- **readme.txt**: 소스코드에 대한 설명서입니다.
- **requirements.txt**: 프로젝트에서 사용되는 파이썬 라이브러리 목록이 포함된 파일입니다.

## 프로젝트 설치 및 실행 가이드

### 1. 프로젝트 디렉터리로 이동
먼저, `requirements.txt` 파일이 있는 프로젝트 디렉터리로 이동합니다.

```bash
cd /path/to/your/project
```
### 2. 가상환경 설정 (선택 사항)

Python 프로젝트마다 의존성을 격리하여 관리하는 것이 좋습니다. 이를 위해 가상환경을 설정할 수 있습니다. 가상환경을 설정하지 않으려면 이 단계를 건너뛰어도 됩니다.

#### 가상환경 만들기:

```bash
python -m venv venv
```

- **Windows**
```bash
.\venv\Scripts\activate
```
- **macOS/Linux**
```bash
source venv/bin/activate
```

### 3. requriements.txt 설치
requirement.txt 파일에 명시된 파이썬 라이브러리를 설치하려면 다음 명령어를 사용하세요
```bash
pip install -r requirements.txt
```

#### 설치된 패키지 확인
```bash
pip freeze
```

### 4. 필수 패키지 설치
```bash
sudo apt-get update
### bitcoin autogen.sh위한 필수 라이브러리
sudo apt-get install autoconf libtool autotools-dev automake pkg-config bsdmainutils python3 libboost-all-dev
### g++, make 관련 빌드 도구
sudo apt-get install build-essential
```

## 프로젝트 사용
프로젝트를 실행하려면 위의 단계를 완료한 후, 관련 Python 파일을 실행하면 됩니다.

### 1. bitcoin github 다운로드 (https://github.com/bitcoin/bitcoin))
해당 버전은 v0.20.0 으로 진행합니다
``` bash
git clone https://github.com/bitcoin/bitcoin.git 
git checkout v.20.0
./autogen.sh

### 에러 해결
```bash
cd ~/db-5.3.28.NC/src/dbinc
sed -i 's/__atomic_compare_exchange/__atomic_compare_exchange_db/g' atomic.h

cd ~/db-5.3.28.NC/build_unix
make clean
../dist/configure --enable-cxx --disable-shared --with-pic --prefix=/usr/local
make
sudo make install
```

### configuration
```bash
./configure --with-incompatible-bdb --with-gui=no LDFLAGS="-L/usr/local/lib" CPPFLAGS="-I/usr/local/include"
```
주요 사항:

bitcoind, bitcoin-cli, bitcoin-tx, bitcoin-wallet 등의 실행 파일들이 /usr/local/bin 디렉토리에 설치되었습니다.
라이브러리 파일(libbitcoinconsensus)도 /usr/local/lib에 설치되었고, 관련 헤더 파일도 /usr/local/include에 설치되었습니다.
설치 중에 에러 메시지는 없었으며, 모든 과정이 정상적으로 진행되었습니다.
이제 설치된 프로그램을 사용할 준비가 된 상태입니다. bitcoind를 백그라운드에서 실행하고 싶다면, 아래 명령어로 실행할 수 있습니다:

### Download blocks
```bash
### background 에서 bitcoin 다운로드 시작
bitcoind -daemon
bitcoin-cli getblockhaininfo 
```
1. 블록체인 동기화 (블록 헤더 및 전체 블록 다운로드)
비트코인 노드를 처음 실행하면, 먼저 블록 헤더를 다운로드하여 전체 블록체인의 구조를 파악합니다.
이후 각 블록의 데이터를 다운로드하며 블록에 포함된 트랜잭션 데이터도 함께 받아옵니다.
즉, 블록을 받을 때 그 안에 포함된 트랜잭션도 함께 수집되기 때문에, 블록을 먼저 모두 받은 후에 트랜잭션을 따로 받는 방식이 아니라 블록과 트랜잭션이 함께 동기화됩니다.
2. 블록체인 검증 (Initial Block Download, IBD)
노드가 네트워크에 연결되고 나면, **Initial Block Download (IBD)**라는 과정이 시작됩니다.
IBD 동안, 노드는 제네시스 블록(첫 번째 블록)부터 시작하여 최신 블록까지 순차적으로 다운로드하고 검증합니다.
블록을 받을 때 그 안에 포함된 트랜잭션을 검증하면서 블록체인 데이터베이스에 저장합니다.
이 과정은 CPU 및 디스크 I/O에 부담이 많이 가는 작업입니다.
3. 메모리풀 트랜잭션 수집 (동기화 완료 후)
블록 동기화가 거의 완료된 후, 즉 현재 네트워크의 최신 블록까지 동기화가 완료되면, 노드는 네트워크의 다른 노드들로부터 미확정 트랜잭션을 메모리풀(Mempool)에 저장하기 시작합니다.
메모리풀에 있는 트랜잭션은 아직 블록에 포함되지 않은 트랜잭션입니다.
이 트랜잭션들은 다음 블록이 생성될 때 블록에 포함될 수 있으며, 노드는 이를 추적하고 업데이트합니다.

## 다운로드 시각화
`visualizeDownlads` 코드는 해당 `bitcoin-cli`를 활용하여 다운로드를 시각화 할수 있게하는 코드, 로그로 찍혀서 진행상황을 파악할 수 있게합니다

## 비트코인 관련 API

### 1. 지갑 명령어
```bash
#getbalance: 지갑의 잔액을 확인합니다.
bitcoin-cli getbalance

#listtransactions: 지갑의 최근 트랜잭션 내역을 확인합니다.
bitcoin-cli listtransactions

#sendtoaddress: 지정한 주소로 비트코인을 전송합니다.
bitcoin-cli sendtoaddress <address> <amount>

#getnewaddress: 새로운 비트코인 주소를 생성합니다.
bitcoin-cli getnewaddress

#listunspent: 지갑에서 사용되지 않은 트랜잭션 출력(UTXO)을 조회합니다.
bitcoin-cli listunspent
```

2. 트랜잭션 명령어
```bash
#createrawtransaction: 새로운 트랜잭션을 생성합니다. 이는 트랜잭션을 생성하되 서명하지 않은 상태입니다.
bitcoin-cli createrawtransaction '[{ "txid": "id", "vout": n }]' '{ "address": amount }'

#signrawtransaction: 서명되지 않은 트랜잭션에 서명합니다.
bitcoin-cli signrawtransaction <hexstring>

#sendrawtransaction: 서명된 트랜잭션을 비트코인 네트워크에 전송합니다.
bitcoin-cli sendrawtransaction <signed_hexstring>
```

3. 블록체인 정보
```bash
#getblockchaininfo: 현재 비트코인 블록체인에 대한 정보를 제공합니다.
bitcoin-cli getblockchaininfo

#getblock: 특정 블록의 정보를 조회합니다.
bitcoin-cli getblock <blockhash>

#getblockcount: 현재 블록체인의 블록 높이를 조회합니다.
bitcoin-cli getblockcount

#getblockhash: 특정 블록 높이에 대한 블록 해시를 반환합니다.
bitcoin-cli getblockhash <block_height>

#getrawtransaction: 트랜잭션 해시로 원시 트랜잭션 데이터를 조회합니다.
bitcoin-cli getrawtransaction <txid>
```

4. 노드 제어
```bash
#getnetworkinfo: 네트워크 상태 및 설정에 대한 정보를 제공합니다.
bitcoin-cli getnetworkinfo

#addnode: 새로운 노드를 네트워크에 추가합니다.
bitcoin-cli addnode <node_ip> add

#getpeerinfo: 현재 연결된 피어의 정보를 반환합니다.
bitcoin-cli getpeerinfo
```

### 5. 마이닝 및 블록 생성
```bash
# getmininginfo: 채굴 관련 정보를 조회합니다.
bitcoin-cli getmininginfo

#generatetoaddress: 특정 주소로 비트코인을 보내는 블록을 생성합니다. 테스트넷에서만 사용할 수 있습니다.
bitcoin-cli generatetoaddress <nblocks> <address> 
```

### 6. 기타 유용한 명령어
```bash
#getmempoolinfo: 메모리풀(트랜잭션 대기열)에 있는 트랜잭션 정보를 조회합니다.
bitcoin-cli getmempoolinfo

#gettxout: 특정 트랜잭션 출력 정보를 확인합니다.
bitcoin-cli gettxout <txid> <n>

#estimatefee: 다음 블록에 포함되기 위한 예상 수수료를 계산합니다.
bitcoin-cli estimatefee <nblocks>
```