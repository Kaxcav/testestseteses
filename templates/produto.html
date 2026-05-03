from flask import Flask, request, redirect, render_template, jsonify, url_for, session
from database import (init_db, salvar_pedido, listar_pedidos, atualizar_status_pedido,
    criar_usuario, buscar_usuario_por_email, buscar_usuario_por_id,
    buscar_usuario_por_google, verificar_senha, atualizar_google_id,
    listar_carrinho, adicionar_ao_carrinho, atualizar_quantidade_carrinho,
    remover_do_carrinho, limpar_carrinho, total_itens_carrinho)
import uuid, os, requests as req_lib

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")

# ─── CONFIG ───────────────────────────────────────────────────────────────────
# ── InvctusPay ────────────────────────────────────────────────────────────────
# Troque pela URL do seu produto de produção quando sair do modo teste
INVICTUS_CHECKOUT_URL = os.environ.get(
    "INVICTUS_CHECKOUT_URL",
    "https://go.invictuspay.app.br/m387smwrlf_mpzmtfsx5d"   # link de teste atual
)

# Google OAuth — configure no Google Cloud Console
GOOGLE_CLIENT_ID     = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI  = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5000/auth/google/callback")

PRODUTO = {
    "id":          "panelas-paris-10",
    "nome":        "Jogo De Panelas Paris 10 Peças Vermelho Tramontina",
    "preco":       54.95,
    "preco_antigo": 71.44,
    "desconto":    "23% OFF",
    "parcelas":    12,
    "parcela_valor": 4.58,
}
# ─────────────────────────────────────────────────────────────────────────────


def usuario_logado():
    uid = session.get("usuario_id")
    return buscar_usuario_por_id(uid) if uid else None


def login_obrigatorio(f):
    """Decorator — redireciona para /login se não estiver logado."""
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not usuario_logado():
            return redirect(url_for("login_page") + "?next=" + request.path)
        return f(*args, **kwargs)
    return wrapper


# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINAS
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    u = usuario_logado()
    cart_count = total_itens_carrinho(u["id"]) if u else 0
    return render_template("produto.html", produto=PRODUTO, usuario=u, cart_count=cart_count)


@app.route("/login")
def login_page():
    if usuario_logado():
        return redirect("/")
    return render_template("login.html", error=request.args.get("error"), success=request.args.get("success"))


@app.route("/carrinho")
def carrinho_page():
    u = usuario_logado()
    itens = listar_carrinho(u["id"]) if u else []
    return render_template("carrinho.html", usuario=u, itens=itens)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    u = usuario_logado()
    quantidade = request.args.get("qtd", 1, type=int)
    if request.method == "GET":
        return render_template("checkout.html", produto=PRODUTO, quantidade=quantidade)

    nome      = request.form.get("nome", "").strip()
    email     = request.form.get("email", "").strip()
    telefone  = request.form.get("telefone", "").strip()
    cpf       = request.form.get("cpf", "").strip()
    quantidade = request.form.get("quantidade", 1, type=int)

    if not nome or not email:
        return render_template("checkout.html", produto=PRODUTO, quantidade=quantidade,
                               erro="Preencha pelo menos nome e e-mail.")

    pedido_id = str(uuid.uuid4())[:8].upper()
    total = round(PRODUTO["preco"] * quantidade, 2)
    salvar_pedido({"id": pedido_id, "nome": nome, "email": email,
                   "telefone": telefone, "cpf": cpf, "quantidade": quantidade,
                   "total": total, "status": "aguardando_pagamento"})

    if u:
        limpar_carrinho(u["id"])

    from urllib.parse import urlencode, quote_plus
    params = urlencode({
        "name":     nome,
        "email":    email,
        "phone":    telefone,
        "cpf":      cpf,
        "order_id": pedido_id,
        "ref":      pedido_id,
        "quantity": quantidade,
    }, quote_via=quote_plus)
    return redirect(f"{INVICTUS_CHECKOUT_URL}?{params}")


@app.route("/obrigado")
def obrigado():
    return render_template("obrigado.html", pedido_id=request.args.get("ref", ""))


@app.route("/admin/pedidos")
def admin_pedidos():
    return render_template("admin.html", pedidos=listar_pedidos())


# ══════════════════════════════════════════════════════════════════════════════
#  AUTH — EMAIL/SENHA
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/auth/login", methods=["POST"])
def auth_login():
    data  = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    senha = data.get("senha", "")

    usuario = verificar_senha(email, senha)
    if not usuario:
        return jsonify({"ok": False, "error": "E-mail ou senha incorretos."})

    session["usuario_id"] = usuario["id"]
    session.permanent = True
    return jsonify({"ok": True, "redirect": "/"})


@app.route("/auth/register", methods=["POST"])
def auth_register():
    data  = request.get_json(silent=True) or {}
    nome  = data.get("nome", "").strip()
    email = data.get("email", "").strip().lower()
    senha = data.get("senha", "")

    if not nome or not email or not senha:
        return jsonify({"ok": False, "error": "Preencha todos os campos."})
    if len(senha) < 6:
        return jsonify({"ok": False, "error": "A senha deve ter no mínimo 6 caracteres."})

    usuario = criar_usuario(nome, email, senha)
    if not usuario:
        return jsonify({"ok": False, "error": "Este e-mail já está cadastrado."})

    session["usuario_id"] = usuario["id"]
    session.permanent = True
    return jsonify({"ok": True, "redirect": "/"})


@app.route("/auth/logout")
def auth_logout():
    session.clear()
    return redirect("/login?success=Você saiu da sua conta.")


# ══════════════════════════════════════════════════════════════════════════════
#  AUTH — GOOGLE OAUTH 2.0
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/auth/google")
def auth_google():
    if not GOOGLE_CLIENT_ID:
        return redirect("/login?error=Google OAuth não configurado. Adicione GOOGLE_CLIENT_ID nas variáveis de ambiente.")
    params = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&prompt=select_account"
    )
    return redirect(params)


@app.route("/auth/google/callback")
def auth_google_callback():
    code  = request.args.get("code")
    error = request.args.get("error")

    if error or not code:
        return redirect("/login?error=Login com Google cancelado.")

    # Troca code por access_token
    try:
        token_resp = req_lib.post("https://oauth2.googleapis.com/token", data={
            "code":          code,
            "client_id":     GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri":  GOOGLE_REDIRECT_URI,
            "grant_type":    "authorization_code",
        }, timeout=10).json()

        access_token = token_resp.get("access_token")
        if not access_token:
            raise ValueError("Sem access_token")

        # Busca dados do usuário
        info = req_lib.get("https://www.googleapis.com/oauth2/v2/userinfo",
                           headers={"Authorization": f"Bearer {access_token}"}, timeout=10).json()

        google_id  = info.get("id")
        email      = info.get("email", "").lower()
        nome       = info.get("name", email.split("@")[0])
        avatar_url = info.get("picture")

        # Verifica se já existe
        usuario = buscar_usuario_por_google(google_id)
        if not usuario:
            usuario = buscar_usuario_por_email(email)
            if usuario:
                atualizar_google_id(usuario["id"], google_id, avatar_url)
                usuario = buscar_usuario_por_id(usuario["id"])
            else:
                usuario = criar_usuario(nome, email, google_id=google_id, avatar_url=avatar_url)

        session["usuario_id"] = usuario["id"]
        session.permanent = True
        return redirect("/")

    except Exception as e:
        print("Google OAuth error:", e)
        return redirect("/login?error=Erro ao autenticar com Google. Tente novamente.")


# ══════════════════════════════════════════════════════════════════════════════
#  CARRINHO — API JSON
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/carrinho/adicionar", methods=["POST"])
def api_carrinho_add():
    u = usuario_logado()
    if not u:
        return jsonify({"ok": False, "redirect": "/login"})

    data = request.get_json(silent=True) or {}
    qtd  = max(1, int(data.get("quantidade", 1)))
    adicionar_ao_carrinho(
        uid=u["id"],
        produto_id=PRODUTO["id"],
        nome=PRODUTO["nome"],
        preco=PRODUTO["preco"],
        preco_antigo=PRODUTO["preco_antigo"],
        quantidade=qtd
    )
    total = total_itens_carrinho(u["id"])
    return jsonify({"ok": True, "cart_count": total})


@app.route("/carrinho/atualizar", methods=["POST"])
@login_obrigatorio
def api_carrinho_update():
    u    = usuario_logado()
    data = request.get_json(silent=True) or {}
    atualizar_quantidade_carrinho(u["id"], data.get("item_id"), data.get("quantidade", 1))
    return jsonify({"ok": True})


@app.route("/carrinho/remover", methods=["POST"])
@login_obrigatorio
def api_carrinho_remove():
    u    = usuario_logado()
    data = request.get_json(silent=True) or {}
    remover_do_carrinho(u["id"], data.get("item_id"))
    return jsonify({"ok": True, "cart_count": total_itens_carrinho(u["id"])})


# ══════════════════════════════════════════════════════════════════════════════
#  WEBHOOK
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/webhook/invictuspay", methods=["POST"])
def webhook_invictuspay():
    data = request.get_json(silent=True) or {}
    pedido_id    = data.get("ref") or data.get("external_id") or data.get("order_id")
    status_gw    = data.get("status", "")
    mapa = {"paid":"pago","approved":"pago","pending":"aguardando_pagamento",
            "refused":"recusado","refunded":"reembolsado","cancelled":"cancelado"}
    if pedido_id:
        atualizar_status_pedido(pedido_id, mapa.get(status_gw, status_gw))
    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
