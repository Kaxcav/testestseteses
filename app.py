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



def admin_obrigatorio(f):
    """Protege rotas admin com usuário e senha via HTTP Basic Auth."""
    from functools import wraps
    from flask import Response
    @wraps(f)
    def wrapper(*args, **kwargs):
        ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
        ADMIN_PASS = os.environ.get("ADMIN_PASS", "troque123")
        auth = request.authorization
        if not auth or auth.username != ADMIN_USER or auth.password != ADMIN_PASS:
            return Response(
                "Acesso restrito. Digite usuário e senha de administrador.",
                401,
                {"WWW-Authenticate": 'Basic realm="Admin Mercado de Ofertas"'}
            )
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
    import re as _re
    def _clean(s): return _re.sub(r'[\r\n\t]', ' ', str(s)).strip()
    params = urlencode({
        "name":     _clean(nome),
        "email":    _clean(email),
        "phone":    _clean(telefone),
        "cpf":      _clean(cpf),
        "order_id": _clean(pedido_id),
        "ref":      _clean(pedido_id),
        "quantity": quantidade,
    }, quote_via=quote_plus)
    return redirect(f"{INVICTUS_CHECKOUT_URL}?{params}")


@app.route("/obrigado")
def obrigado():
    return render_template("obrigado.html", pedido_id=request.args.get("ref", ""))


@app.route("/admin/pedidos")
@admin_obrigatorio
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




# ══════════════════════════════════════════════════════════════════════════════
#  RASTREAMENTO DE VISITANTES
# ══════════════════════════════════════════════════════════════════════════════

def init_visitor_tables():
    import sqlite3 as _sq
    db = os.environ.get("DB_PATH", "/data/pedidos.db")
    os.makedirs(os.path.dirname(db), exist_ok=True)
    conn = _sq.connect(db)
    conn.execute("""CREATE TABLE IF NOT EXISTS visitantes (
        id TEXT PRIMARY KEY, session_id TEXT, first_visit INTEGER,
        visit_count INTEGER, user_agent TEXT, language TEXT, platform TEXT,
        screen_resolution TEXT, timezone TEXT, referrer TEXT,
        landing_page TEXT, created_at TEXT, last_visit TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS acoes_usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT, visitor_id TEXT,
        session_id TEXT, action TEXT, details TEXT, page TEXT, created_at TEXT)""")
    conn.commit(); conn.close()

init_visitor_tables()


@app.route("/api/visitor-data", methods=["POST"])
def api_visitor_data():
    try:
        d = request.get_json(silent=True) or {}
        import sqlite3 as _sq
        db = os.environ.get("DB_PATH", "/data/pedidos.db")
        conn = _sq.connect(db); conn.row_factory = _sq.Row
        now = __import__('datetime').datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ex = conn.execute("SELECT id FROM visitantes WHERE id=?", (d.get("visitorId",""),)).fetchone()
        if ex:
            conn.execute("UPDATE visitantes SET session_id=?,visit_count=?,last_visit=? WHERE id=?",
                (d.get("sessionId"), d.get("visitCount"), now, d.get("visitorId")))
        else:
            conn.execute("""INSERT INTO visitantes
                (id,session_id,first_visit,visit_count,user_agent,language,platform,
                 screen_resolution,timezone,referrer,landing_page,created_at,last_visit)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                d.get("visitorId",""), d.get("sessionId",""), int(d.get("firstVisit",0)),
                d.get("visitCount",1), d.get("userAgent",""), d.get("language",""),
                d.get("platform",""), d.get("screenResolution",""), d.get("timezone",""),
                d.get("referrer",""), d.get("landingPage",""), now, now))
        conn.commit(); conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False}), 500


@app.route("/api/user-action", methods=["POST"])
def api_user_action():
    try:
        d = request.get_json(silent=True) or {}
        import sqlite3 as _sq
        db = os.environ.get("DB_PATH", "/data/pedidos.db")
        conn = _sq.connect(db)
        now = __import__('datetime').datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        conn.execute("""INSERT INTO acoes_usuario
            (visitor_id,session_id,action,details,page,created_at)
            VALUES (?,?,?,?,?,?)""", (
            d.get("visitorId",""), d.get("sessionId",""),
            d.get("action",""), str(d.get("details",{})),
            d.get("page",""), now))
        conn.commit(); conn.close()
        return jsonify({"ok": True})
    except Exception:
        return jsonify({"ok": False}), 500


@app.route("/admin/visitantes")
@admin_obrigatorio
def admin_visitantes():
    import sqlite3 as _sq
    db = os.environ.get("DB_PATH", "/data/pedidos.db")
    conn = _sq.connect(db); conn.row_factory = _sq.Row
    visitantes = [dict(r) for r in conn.execute(
        "SELECT * FROM visitantes ORDER BY last_visit DESC").fetchall()]
    acoes = [dict(r) for r in conn.execute(
        "SELECT * FROM acoes_usuario ORDER BY created_at DESC LIMIT 100").fetchall()]
    conn.close()
    return render_template("admin_visitantes.html", visitantes=visitantes, acoes=acoes)

# Inicializa o banco sempre — funciona com gunicorn e em desenvolvimento
init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
