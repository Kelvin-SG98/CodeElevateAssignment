import sqlite3

conn = sqlite3.connect("iot_dados.db")
cursor = conn.cursor()

query = "SELECT localizacao,count(*) FROM sensores GROUP BY localizacao ORDER BY count(*) DESC LIMIT 10"
cursor.execute(query)

# Obter cabeçalhos (nomes das colunas)
col_names = [desc[0] for desc in cursor.description]

# Obter os dados
rows = cursor.fetchall()

# Exibir cabeçalho
print("\t".join(col_names))

# Exibir dados
for row in rows:
    print("\t".join(str(item) for item in row))

conn.close()
