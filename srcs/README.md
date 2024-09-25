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

## 프로젝트 사용
프로젝트를 실행하려면 위의 단계를 완료한 후, 관련 Python 파일을 실행하면 됩니다.

### 1. bitcoin github 다운로드 (https://github.com/bitcoin/bitcoin))
``` bash
git clone https://github.com/bitcoin/bitcoin.git
```

### 2