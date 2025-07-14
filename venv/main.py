# import requests
# import urllib.parse
# import pandas as pd

# # Seu token
# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijk5NWY3MGQxLTc5YjItNGQ5Zi04ZDZkLWZiZmMzMTA0M2E1YSIsImlhdCI6MTc1MjUwNTAxNiwic3ViIjoiZGV2ZWxvcGVyLzRmYjlmNGJlLWUzOTUtYWUzOS05MjMwLTA1OTMzYzE5MjUyNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxODYuMjQ3LjQwLjI0MSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.E4pBMHrpznJWyDmYGvqEnMOyjDlnUYD_ve0YYl1T4KuumR9uV3A08Nz47BV5bOENRJyx9j7WTs2FM3m33bIsbQ"

# # Tag do seu clã
# clan_tag = "#9URLRJYG"
# encoded_tag = urllib.parse.quote(clan_tag)

# # Cabeçalhos da requisição
# headers = {
#     "Accept": "application/json",
#     "Authorization": token
# }

# # Endpoint do histórico de guerras fluviais
# url = f"https://api.clashroyale.com/v1/clans/{encoded_tag}/riverracelog"

# response = requests.get(url, headers=headers)

# # Verificação de erro
# if response.status_code != 200:
#     print("Erro:", response.status_code, response.text)
#     exit()

# # Dados da resposta
# data = response.json()

# # Pega as últimas 3 guerras
# last_3_wars = data["items"][:3]

# # Criar um dicionário para armazenar DataFrames por guerra
# sheets = {}

# # Processar cada guerra
# for i, war in enumerate(last_3_wars, start=1):
#     meu_cla = None

#     # Procurar o clã correto na guerra (garantia em guerras multiclãs)
#     for tag_atual, info in war["clans"].items():
#         if info["tag"].upper() == clan_tag.upper():
#             meu_cla = info
#             break

#     if not meu_cla:
#         print(f"⚠️ Clã {clan_tag} não encontrado na Guerra {i}")
#         continue

#     participants = meu_cla.get("participants", [])
#     rows = []
#     for p in participants:
#         rows.append({
#             "Nome": p["name"],
#             "Medalhas": p["fame"],
#             "Decks Usados": p["decksUsed"]
#         })

#     df = pd.DataFrame(rows)
#     df = df.sort_values(by="Medalhas", ascending=False)
#     sheets[f"Guerra {i}"] = df

# # Exporta para Excel com múltiplas abas
# with pd.ExcelWriter("clan_last_3_wars.xlsx", engine="openpyxl") as writer:
#     for nome_aba, df in sheets.items():
#         df.to_excel(writer, sheet_name=nome_aba, index=False)

# print("✅ Arquivo 'clan_last_3_wars.xlsx' criado com sucesso!")


import requests
import urllib.parse
import pandas as pd
import json

# Seu token
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijk5NWY3MGQxLTc5YjItNGQ5Zi04ZDZkLWZiZmMzMTA0M2E1YSIsImlhdCI6MTc1MjUwNTAxNiwic3ViIjoiZGV2ZWxvcGVyLzRmYjlmNGJlLWUzOTUtYWUzOS05MjMwLTA1OTMzYzE5MjUyNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxODYuMjQ3LjQwLjI0MSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.E4pBMHrpznJWyDmYGvqEnMOyjDlnUYD_ve0YYl1T4KuumR9uV3A08Nz47BV5bOENRJyx9j7WTs2FM3m33bIsbQ"

# Clan tag
clan_tag = "#9URLRJYG"

encoded_tag = urllib.parse.quote(clan_tag)

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

# URL do histórico das guerras
url = f"https://api.clashroyale.com/v1/clans/{encoded_tag}/riverracelog"

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Erro:", response.status_code, response.text)
    exit()

data = response.json()
texto_formatado = json.dumps(data, indent=4, ensure_ascii=False)
# Salva no arquivo
with open('dados_jogador.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write(texto_formatado)
print("Dados salvos com sucesso em 'dados_jogador.txt' ✅")

last_3_wars = data["items"][:3]

# Criar um dicionário de DataFrames
sheets = {}

# Processar cada guerra
for i, war in enumerate(last_3_wars, start=1):
    meu_cla = None

    for standing in war["standings"]:
        clan_info = standing["clan"]
        if clan_info["tag"].upper() == clan_tag.upper():
            meu_cla = clan_info
            break

    if not meu_cla:
        print(f"⚠️ Clã {clan_tag} não encontrado na Guerra {i}")
        continue

    participants = meu_cla.get("participants", [])
    rows = []
    for p in participants:
        rows.append({
            "Nome": p["name"],
            "Medalhas": p["fame"],
            "Decks Usados": p["decksUsed"]
        })

    df = pd.DataFrame(rows)
    df = df.sort_values(by="Medalhas", ascending=False)
    sheets[f"Guerra {i}"] = df

# Exporta para Excel com múltiplas abas
with pd.ExcelWriter("clan_last_3_wars.xlsx", engine="openpyxl") as writer:
    for nome_aba, df in sheets.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)

print("✅ Arquivo 'clan_last_3_wars.xlsx' criado com sucesso!")

# Falta mesclar com as doações o ranking e tá pronto
