#!/bin/bash

# .txt ファイルを見つけて、それぞれに dos2unix を実行します
find . -type f -iname "*.txt" -exec dos2unix {} \;

echo "すべての .txt ファイルの改行コードを LF に変換しました。"
