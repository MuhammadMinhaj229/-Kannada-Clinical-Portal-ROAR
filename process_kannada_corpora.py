import pandas as pd
import json

# 1. Read Real Words
df_real = pd.read_csv(r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/realwords.csv')
print(f"Loaded {len(df_real)} real words")

# 2. Read Nonwords
nonwords_path = r'C:/Users/User/.gemini/antigravity/brain/384e9f2d-2c0d-4f84-a3bf-138e1df437bd/.user_uploaded/media_1794754075883_6d51365a.xlsm'
df_pseudo = pd.read_excel(nonwords_path, sheet_name=0)
print(f"Loaded {len(df_pseudo)} pseudo words")

# Print samples
print("\nSample Real Words:")
for idx, r in df_real.head(10).iterrows():
    print(f"  {r['word']} ({r['transcription']}) - {r['meaning']}")

print("\nSample Non-Real Words:")
for idx, r in df_pseudo.head(10).iterrows():
    print(f"  {r['nonword']} (id: {r['nonword_id']}, method: {r['method']})")
