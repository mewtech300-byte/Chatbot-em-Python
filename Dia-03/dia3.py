    from pyngrok import ngrok

# Conectar a porta 8000 em um URL público
public_url = ngrok.connect(8000)

print("-" * 30)
print(f"O seu link público é: {public_url}")
print("-" * 30)

input("Pressione Enter para encerrar o túnel...")
