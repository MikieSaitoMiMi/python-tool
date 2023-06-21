import subprocess
from pathlib import Path
import pandas as pd
import csv
import os
import random

### cognito一括パスワード変更

## 前提
# cognitoのユーザープール→ユーザーをインポート→インポートジョブを作成→CSVをアップロード欄にあるtemplate.csvを元にユーザーを登録
# コンソール上から登録した場合は必要部分にユーザー情報を入力してCSVを使用
# 当ファイルが存在するフォルダにCSVを格納しておく

# CSVデータを取得
parent = Path(__file__).resolve().parent
CSV = pd.read_csv(f'{parent}/template.csv', low_memory=False)

# ランダムパスワード作成

# 特殊記号
punctuation = '!#$%&'
# 大文字
ascii_lowercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# 小文字
ascii_uppercase = 'abcdefghijklnmopqrstuvwxyz'
# 数字
digits = '0123456789'

def get_random_password():
    random_source = ascii_lowercase + ascii_uppercase + digits + punctuation
    password = random.choice(ascii_lowercase)
    password += random.choice(ascii_uppercase)
    password += random.choice(digits)
    password += random.choice(punctuation)

    password += ''.join(random.choices(random_source, k=12))
    return password

# 任意のプールidを以下変数に文字列として格納
userpoolid = ""

# 出力結果を格納する配列(CSV書き出しに使用)
usernameList = []
passwordList = []

# AWS CLIコマンドを実行する関数
def run_aws_command(command):
  subprocess.run(command, shell=True)

# CSVからユーザーネームを取得(cognito:username)
for username in CSV['cognito:username']:
  password = get_random_password()
  password = str(password)
  # コマンド実行
  run_aws_command(f"aws cognito-idp admin-set-user-password --user-pool-id {userpoolid} --username {username} --password '{password}' --permanent")
  print(f"--username {username} --password {password}")
  usernameList.append(username)
  passwordList.append(password)

# usernameとpasswordをcsvとして出力する
def write_arrays_to_csv(usernameList, passwordList):
    output_path = os.path.join(f'{parent}/result', 'result.csv')
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['username', 'password'])
        # ヘッダー行を書き込む
        writer.writerows(zip(usernameList, passwordList))

# 配列をCSVファイルに書き込む
write_arrays_to_csv(usernameList, passwordList)