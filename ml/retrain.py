import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / 'src'))

from train_deployment_safe import train_deployment_safe_rf

data_path = r'C:\Users\ULTRAPC\Downloads\archive'
results = train_deployment_safe_rf(data_dir=data_path)
print("\n[OK] Models retrained successfully!")
