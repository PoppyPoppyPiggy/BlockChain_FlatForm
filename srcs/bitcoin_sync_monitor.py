import requests
import json
import subprocess
import time

def get_blockchain_info():
    result = subprocess.run(['bitcoin-cli', 'getblockchaininfo'], stdout=subprocess.PIPE)
    return json.loads(result.stdout)

def get_network_totals():
    result = subprocess.run(['bitcoin-cli', 'getnettotals'], stdout=subprocess.PIPE)
    return json.loads(result.stdout)

def log_sync_status():
    previous_bytes_recv = None
    previous_block = None
    total_downloaded_bytes = 0
    total_added_blocks = 0
    start_time = time.time()

    while True:
        blockchain_info = get_blockchain_info()
        network_totals = get_network_totals()

        current_block = blockchain_info['blocks']
        total_blocks = blockchain_info['headers']
        progress = blockchain_info['verificationprogress'] * 100

        bytes_recv = network_totals['totalbytesrecv']

        if previous_bytes_recv is not None:
            downloaded_bytes = bytes_recv - previous_bytes_recv
            added_blocks = current_block - previous_block
            total_downloaded_bytes += downloaded_bytes
            total_added_blocks += added_blocks
        else:
            downloaded_bytes = 0
            added_blocks = 0

        # 시간 경과에 따른 평균 블록 속도 및 데이터 속도 계산
        elapsed_time = time.time() - start_time
        avg_blocks_per_second = total_added_blocks / elapsed_time if elapsed_time > 0 else 0

        # 남은 블록 수 및 ETA 계산
        remaining_blocks = total_blocks - current_block
        if avg_blocks_per_second > 0:
            estimated_time_remaining = remaining_blocks / avg_blocks_per_second
        else:
            estimated_time_remaining = float('inf')

        # ETA 시간 계산
        if estimated_time_remaining != float('inf'):
            hours, rem = divmod(estimated_time_remaining, 3600)
            minutes, seconds = divmod(rem, 60)
            eta = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        else:
            eta = "N/A"

        data = {
            'currentBlock': current_block,
            'totalBlocks': total_blocks,
            'progress': progress,
            'addedBlocks': added_blocks,
            'addedData': downloaded_bytes / 1024 / 1024,
            'speed': downloaded_bytes / 1024 / 1024 / 3,  # 3초당 MB/s
            'transactions': 0,  # 업데이트 필요시 수정
            'eta': eta  # ETA 추가
        }

        # 서버에 상태 전송
        try:
            response = requests.post('http://localhost:5000/update', json=data)
            print(f"Sync status updated: {data}")
        except Exception as e:
            print(f"Failed to send sync status: {e}")

        previous_bytes_recv = bytes_recv
        previous_block = current_block

        time.sleep(3)

# 스크립트 실행
log_sync_status()
