import subprocess
import json
import time

# 수집 간격 (초)
interval = 3  # 3초마다 수집

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
    """동기화 상태를 기록하고, 다운로드된 바이트와 트랜잭션 수를 로그 형식으로 출력합니다."""
    previous_bytes_recv = None
    previous_tx_count = None
    previous_block = None
    start_time = time.time()  # 스크립트 시작 시간
    total_downloaded_bytes = 0  # 총 다운로드된 바이트
    total_added_blocks = 0  # 총 추가된 블록 수

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

            # 이전 데이터와 비교하여 다운로드된 바이트 수와 트랜잭션 수 계산
            if previous_bytes_recv is not None:
                downloaded_bytes = bytes_recv - previous_bytes_recv
                new_tx = tx_count - previous_tx_count
                added_blocks = current_block - previous_block
                total_downloaded_bytes += downloaded_bytes
                total_added_blocks += added_blocks
            else:
                downloaded_bytes = 0
                new_tx = 0
                added_blocks = 0

            # 전체 평균 초당 다운로드 속도 및 블록 처리 속도 계산
            elapsed_time = time.time() - start_time  # 시작 후 경과 시간
            avg_bytes_per_second = total_downloaded_bytes / elapsed_time if elapsed_time > 0 else 0
            avg_blocks_per_second = total_added_blocks / elapsed_time if elapsed_time > 0 else 0

            # 남은 블록 수와 초당 블록 처리량을 기준으로 남은 시간 예상
            remaining_blocks = total_blocks - current_block
            if avg_blocks_per_second > 0:
                estimated_time_remaining = remaining_blocks / avg_blocks_per_second
            else:
                estimated_time_remaining = float('inf')

            # 남은 시간을 시간, 분, 초로 변환
            if estimated_time_remaining != float('inf'):
                hours, rem = divmod(estimated_time_remaining, 3600)
                minutes, seconds = divmod(rem, 60)
                eta = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
            else:
                eta = "N/A"

            # 로그 형식 출력
            print(f"================= {time.strftime('%Y-%m-%d %H:%M:%S')} =================")
            print(f"Current block: {current_block}/{total_blocks} (Progress: {progress:.2f}%)")
            print(f"Added blocks: +{added_blocks} | Remaining blocks: {remaining_blocks}")
            print(f"Added data: +{downloaded_bytes / 1024 / 1024:.2f} MB | Speed: {avg_bytes_per_second / 1024 / 1024:.2f} MB/s")
            print(f"Transactions: +{new_tx} | ETA: {eta}")
            print("=========================================================\n")

            # 현재 상태를 저장하여 다음 루프에서 비교
            previous_bytes_recv = bytes_recv
            previous_tx_count = tx_count
            previous_block = current_block

            # 3초 대기 후 다음 상태 체크
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Sync log stopped.")

# 스크립트 실행
log_sync_status()
