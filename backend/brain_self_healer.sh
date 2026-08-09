#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="self_healer_$(date +%Y%m%d_%H%M%S).log"

echo "=== AI SELF HEALER START ===" | tee -a $LOG

echo "=== PYTHON COMPILE SCAN ===" | tee -a $LOG

python -m compileall app -q

if [ $? -eq 0 ]
then
    echo "PYTHON CODE: OK" | tee -a $LOG
else
    echo "PYTHON ERRORS FOUND" | tee -a $LOG
fi


echo "=== IMPORT DEEP SCAN ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import os, importlib

failed=[]

for root,dirs,files in os.walk("app"):
    for f in files:
        if f.endswith(".py"):
            path=os.path.join(root,f)
            mod=path.replace("/",".").replace(".py","")
            if mod.endswith("__init__"):
                continue
            try:
                importlib.import_module(mod)
            except Exception as e:
                failed.append((mod,str(e)))

print("FAILED MODULES:")

if failed:
    for x in failed:
        print(x)
else:
    print("NONE")

PY


echo "=== HEALTH CHECK ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG


echo "=== MEMORY CHECK ===" | tee -a $LOG

find app -name "*.json" | while read f
do
python - <<PY
import json
try:
 json.load(open("$f"))
except:
 print("BROKEN JSON: $f")
PY
done | tee -a $LOG


echo "REPORT:"
echo $LOG

