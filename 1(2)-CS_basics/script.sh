#!/bin/bash
# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
if ! command -v conda &> /dev/null; then
    echo "[INFO] Conda가 설치되어 있지 않아 Miniconda를 설치합니다."

    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

    bash miniconda.sh -b -p "$HOME/miniconda3"

    source "$HOME/miniconda3/etc/profile.d/conda.sh"
else
    source "$(conda info --base)/etc/profile.d/conda.sh"
fi

# Conda 환셩 생성 및 활성화
if ! conda env list | grep -q "myenv"; then
    echo "[INFO] myenv 가상환경을 생성합니다."
    conda create -y -n myenv python=3.11
fi
conda activate myenv


## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
pip install mypy

mkdir -p output

# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    problem_num=$(echo "$file" | sed -E 's/^[0-9]_([0-9]+)\.py$/\1/')
    python "$file" < "../input/${problem_num}_input" > "../output/${problem_num}_output"

done

# mypy 테스트 실행 및 mypy_log.txt 저장
mypy *.py > ../mypy_log.txt 2>&1

# conda.yml 파일 생성
cd ..
conda env export > conda.yml

# 가상환경 비활성화
conda deactivate