from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# (Opcional) Token de acesso fixo
TOKEN_FIXO = "ntlsstudiosDev"

def get_instagram_data(username):
    headers = {
        "User-Agent": "Instagram 155.0.0.37.107",
        "X-IG-App-ID": "936619743392459"
    }

    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "data" in data and "user" in data["data"]:
            user = data["data"]["user"]
            return {
                "username": user["username"],
                "full_name": user["full_name"],
                "followers": user["edge_followed_by"]["count"],
                "following": user["edge_follow"]["count"],
                "posts": user["edge_owner_to_timeline_media"]["count"],
                "bio": user["biography"],
                "profile_pic_url": user.get("profile_pic_url_hd") or user.get("profile_pic_url"),
                "profile_url": f"https://instagram.com/{user['username']}"
            }
        else:
            return {"error": "Usuário não encontrado ou bloqueado."}

    except Exception as e:
        return {"error": str(e)}

@app.route("/api", methods=["GET"])
def api():
    username = request.args.get("username", "").strip().lstrip("@")
    token = request.args.get("token", None)

    if not username:
        return jsonify({"error": "Parâmetro 'username' é obrigatório"}), 400

    # Verifica o token se for necessário
    if token and token != TOKEN_FIXO:
        return jsonify({"error": "Token inválido"}), 401

    resultado = get_instagram_data(username)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
      
