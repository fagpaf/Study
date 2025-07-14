import requests
import urllib.parse
import pandas as pd

# Seu token
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijk5NWY3MGQxLTc5YjItNGQ5Zi04ZDZkLWZiZmMzMTA0M2E1YSIsImlhdCI6MTc1MjUwNTAxNiwic3ViIjoiZGV2ZWxvcGVyLzRmYjlmNGJlLWUzOTUtYWUzOS05MjMwLTA1OTMzYzE5MjUyNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxODYuMjQ3LjQwLjI0MSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.E4pBMHrpznJWyDmYGvqEnMOyjDlnUYD_ve0YYl1T4KuumR9uV3A08Nz47BV5bOENRJyx9j7WTs2FM3m33bIsbQ"

# Clan tag
clan_tag = "#9URLRJYG"
encoded_tag = urllib.parse.quote(clan_tag)

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

# ===============================
# Busca doações e troféus
# ===============================
url_clan = f"https://api.clashroyale.com/v1/clans/{encoded_tag}"
response_clan = requests.get(url_clan, headers=headers)

if response_clan.status_code != 200:
    print("Erro ao buscar membros:", response_clan.status_code, response_clan.text)
    exit()

clan_data = response_clan.json()

doacoes_por_nome = {}
trofeus_por_nome = {}

for m in clan_data["memberList"]:
    doacoes_por_nome[m["name"]] = m["donations"]
    trofeus_por_nome[m["name"]] = m["trophies"]

# ===============================
# Busca histórico das guerras
# ===============================
url_riverrace = f"https://api.clashroyale.com/v1/clans/{encoded_tag}/riverracelog"
response_river = requests.get(url_riverrace, headers=headers)

if response_river.status_code != 200:
    print("Erro ao buscar guerra:", response_river.status_code, response_river.text)
    exit()

data = response_river.json()
last_3_wars = data["items"][:3]

# ===============================
# Gerar DataFrames por guerra
# ===============================
sheets = {}

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
        nome = p["name"]
        medalhas = p["fame"]
        decks_usados = p["decksUsed"]
        doacoes = doacoes_por_nome.get(nome, 0)
        trofeus = trofeus_por_nome.get(nome, 0)
        rows.append({
            "Nome": nome,
            "Troféus": trofeus,             # Só como atributo
            "Medalhas": medalhas,
            "Decks Usados": decks_usados,
            "Doações": doacoes
        })

    df = pd.DataFrame(rows)

    # Ordenar apenas por Medalhas e Doações, não pelos Troféus
    df = df.sort_values(by=["Medalhas", "Doações"], ascending=False)

    sheets[f"Guerra {i}"] = df

# ===============================
# Exportar para Excel
# ===============================
with pd.ExcelWriter("clan_last_3_wars.xlsx", engine="openpyxl") as writer:
    for nome_aba, df in sheets.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)

print("✅ Arquivo 'clan_last_3_wars.xlsx' criado com sucesso!")