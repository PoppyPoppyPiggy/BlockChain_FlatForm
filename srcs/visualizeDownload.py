import subprocess
import json
import time

# 수집 간격 (초)
interval = 3  # 1분마다 수집

def get_blockchain_info():
    """비트코인 노드의 블록체인 동기화 정보를 가져옵니다."""
    result = subprocess.run(['bitcoin-cli', 'getblockchaininfo'], stdout=subprocess.PIPE)
    return json.loads(result.stdout)

def get_network_totals():
    """비트코인 네트워크에서 송수신된 바이트 수를 가져옵니다."""
    result = subprocess.run(['bitcoin-cli', 'getnettotals'], stdout=subprocess.PIPE)
    return json.loads(result.stdout)

def get_mempool_info():
    """메모리풀 정보를 가져와 트랜잭션 수를 확인합니다."""
    result = subprocess.run(['bitcoin-cli', 'getmempoolinfo'], stdout=subprocess.PIPE)
    return json.loads(result.stdout)

def log_sync_status():
    """매 분마다 동기화 상태를 기록하고, 다운로드된 바이트와 트랜잭션 수를 로그로 출력합니다."""
    previous_bytes_recv = None
    previous_tx_count = None

    try:
        while True:
            # 블록체인 정보와 네트워크 통계 가져오기
            blockchain_info = get_blockchain_info()
            network_totals = get_network_totals()
            mempool_info = get_mempool_info()

            # 현재 다운로드된 블록, 총 수신된 바이트 정보
            current_block = blockchain_info['blocks']
            total_blocks = blockchain_info['headers']
            progress = blockchain_info['verificationprogress'] * 100  # %로 변환
            tx_count = mempool_info['size']  # 메모리풀에서 트랜잭션 수 확인
            bytes_recv = network_totals['totalbytesrecv']

            # 이전 데이터와 비교하여 지난 1분 동안 수신한 바이트 수와 트랜잭션 수 계산
            if previous_bytes_recv is not None:
                downloaded_bytes = bytes_recv - previous_bytes_recv
                new_tx = tx_count - previous_tx_count
            else:
                downloaded_bytes = 0
                new_tx = 0

            # 진행 상황과 다운로드된 바이트, 트랜잭션 수를 로그로 출력
            print(f"================= {time.strftime('%Y-%m-%d %H:%M:%S')} =================")
            print(f"현재 블록: {current_block}/{total_blocks}")
            print(f"진행 상황: {progress:.2f}%")
            print(f"지난 {interval}초간 다운로드된 데이터: {downloaded_bytes / 1024 / 1024:.2f} MB")
            print(f"지난 {interval}초간 처리된 트랜잭션 수: {new_tx}")
            print(f"노드가 풀노드가 될 때까지 남은 블록 수: {total_blocks - current_block}")
            print("=========================================================\n")

            # 현재 상태를 저장하여 다음 루프에서 비교
            previous_bytes_recv = bytes_recv
            previous_tx_count = tx_count

            # 1분 대기 후 다음 상태 체크
            time.sleep(interval)

    except KeyboardInterrupt:
        print("동기화 상태 로그 기록이 중단되었습니다.")

# 스크립트 실행
log_sync_status()
