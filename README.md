## Установка

# Windows
```bash
git clone https://github.com/Whyrenot/BND_LLC_test_task.git
cd BND_LLC_test_task
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```
# Linux / MacOS
```bash
git clone https://github.com/Whyrenot/BND_LLC_test_task.git
cd BND_LLC_test_task

python -m venv venv || python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python src/main.py
```
