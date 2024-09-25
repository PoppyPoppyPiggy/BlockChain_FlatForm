from flask import Flask, jsonify
import subprocess
import json
import time

app = Flask(__name__)

# 현재 동기화 상태를 저장하는 변수
sync_status = {
    'currentBlock': 0,
    'totalBlocks': 0,
    'progress': 0,
    'addedBlocks': 0,
    'addedData': 0,
    'speed': 0,
    'transactions': 0,
    'eta': "N/A"
}

@app.route('/status', methods=['GET'])
def get_status():
    """현재 동기화 상태를 반환"""
    return jsonify(sync_status)

def update_sync_status(current_block, total_blocks, progress, added_blocks, added_data, speed, transactions, eta):
    """동기화 상태 업데이트"""
    sync_status['currentBlock'] = current_block
    sync_status['totalBlocks'] = total_blocks
    sync_status['progress'] = progress
    sync_status['addedBlocks'] = added_blocks
    sync_status['addedData'] = added_data
    sync_status['speed'] = speed
    sync_status['transactions'] = transactions
    sync_status['eta'] = eta

if __name__ == '__main__':
    app.run(port=5000)
