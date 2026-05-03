<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Finalizar Compra – Mercado Liquida</title>
  <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700&display=swap" rel="stylesheet"/>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Lexend',sans-serif;background:#f0f0f0;color:#1a1a1a;min-height:100vh}

    /* NAV */
    .nav{background:#1a2744;color:#fff;padding:0 2rem;height:54px;display:flex;align-items:center;gap:10px}
    .nav-logo{font-size:16px;font-weight:600;display:flex;align-items:center;gap:8px}
    .nav-logo-icon{width:26px;height:26px;background:#fff;border-radius:5px;display:flex;align-items:center;justify-content:center}
    .nav-step{margin-left:auto;font-size:12px;color:#8a9bc0}

    /* LAYOUT */
    .wrap{max-width:860px;margin:2rem auto;padding:0 1rem;display:grid;grid-template-columns:1fr 300px;gap:1.5rem;align-items:start}
    @media(max-width:680px){.wrap{grid-template-columns:1fr}}

    /* FORM CARD */
    .card{background:#fff;border-radius:10px;padding:1.5rem}
    .card-title{font-size:15px;font-weight:600;margin-bottom:1.2rem;padding-bottom:0.8rem;border-bottom:1px solid #eee;color:#1a2744}

    .form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
    .form-row.full{grid-template-columns:1fr}
    label{display:block;font-size:12px;color:#666;margin-bottom:4px;font-weight:500}
    input{width:100%;height:42px;border:1.5px solid #ddd;border-radius:7px;padding:0 12px;font-size:14px;font-family:'Lexend',sans-serif;outline:none;transition:border-color .2s;color:#1a1a1a;background:#fff}
    input:focus{border-color:#1a2744}
    input::placeholder{color:#bbb}

    .qty-wrap{display:flex;align-items:center;gap:10px}
    .qty-btn{width:36px;height:36px;border:1.5px solid #ddd;border-radius:7px;background:#fff;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#444;transition:border-color .2s}
    .qty-btn:hover{border-color:#1a2744}
    .qty-val{font-size:15px;font-weight:600;min-width:24px;text-align:center}
    input[name="quantidade"]{display:none}

    .erro{background:#fef2f2;border:1px solid #fecaca;color:#dc2626;padding:10px 14px;border-radius:7px;font-size:13px;margin-bottom:14px}

    /* RESUMO */
    .resumo{background:#fff;border-radius:10px;padding:1.5rem;position:sticky;top:1.5rem}
    .resumo h3{font-size:14px;font-weight:600;color:#1a2744;margin-bottom:1rem;padding-bottom:0.8rem;border-bottom:1px solid #eee}
    .resumo-nome{font-size:13px;font-weight:500;line-height:1.4;margin-bottom:12px;color:#333}
    .resumo-linha{display:flex;justify-content:space-between;font-size:13px;color:#666;margin-bottom:6px}
    .resumo-linha.total{font-size:16px;font-weight:700;color:#1a1a1a;margin-top:10px;padding-top:10px;border-top:1px solid #eee}
    .resumo-desconto{color:#22c55e;font-size:12px;font-weight:600}
    .resumo-parcela{font-size:12px;color:#1a2744;margin-top:4px}

    /* BOTÃO */
    .btn-comprar{width:100%;height:50px;background:#1a2744;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer;font-family:'Lexend',sans-serif;margin-top:1rem;letter-spacing:0.3px;transition:background .2s;display:flex;align-items:center;justify-content:center;gap:8px}
    .btn-comprar:hover{background:#243560}
    .btn-comprar:active{transform:scale(.99)}

    /* SELOS */
    .selos{margin-top:14px;display:flex;flex-direction:column;gap:8px}
    .selo{display:flex;align-items:center;gap:7px;font-size:11px;color:#666}

    .frete-gratis{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:7px;padding:8px 12px;font-size:12px;color:#15803d;font-weight:600;display:flex;align-items:center;gap:6px;margin-bottom:12px}
  </style>
</head>
<body>

<nav class="nav">
  <div class="nav-logo">
    <div class="nav-logo-icon">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#1a2744" stroke-width="2.5">
        <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
        <line x1="3" y1="6" x2="21" y2="6"/>
        <path d="M16 10a4 4 0 01-8 0"/>
      </svg>
    </div>
    Mercado Liquida
  </div>
  <span class="nav-step">Checkout seguro 🔒</span>
</nav>

<div class="wrap">
  <!-- FORMULÁRIO -->
  <div>
    <div class="card">
      <p class="card-title">Seus dados de entrega</p>

      {% if erro %}
        <div class="erro">⚠️ {{ erro }}</div>
      {% endif %}

      <form method="POST" action="/checkout">
        <div class="form-row">
          <div>
            <label>Nome completo *</label>
            <input name="nome" type="text" placeholder="João Silva" required/>
          </div>
          <div>
            <label>CPF *</label>
            <input name="cpf" type="text" placeholder="000.000.000-00" id="cpf"/>
          </div>
        </div>
        <div class="form-row">
          <div>
            <label>E-mail *</label>
            <input name="email" type="email" placeholder="seu@email.com" required/>
          </div>
          <div>
            <label>Telefone / WhatsApp</label>
            <input name="telefone" type="tel" placeholder="(11) 99999-9999" id="tel"/>
          </div>
        </div>

        <div class="form-row full" style="margin-top:8px">
          <div>
            <label>Quantidade</label>
            <div class="qty-wrap">
              <button type="button" class="qty-btn" onclick="changeQty(-1)">−</button>
              <span class="qty-val" id="qty-display">{{ quantidade }}</span>
              <button type="button" class="qty-btn" onclick="changeQty(1)">+</button>
              <input type="hidden" name="quantidade" id="qty-input" value="{{ quantidade }}"/>
              <span style="font-size:13px;color:#888">(+50 disponíveis)</span>
            </div>
          </div>
        </div>

        <button type="submit" class="btn-comprar" id="btn-submit">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
          </svg>
          Ir para pagamento seguro
        </button>
      </form>
    </div>
  </div>

  <!-- RESUMO -->
  <div class="resumo">
    <h3>Resumo do pedido</h3>
    <p class="resumo-nome">{{ produto.nome }}</p>

    <div class="frete-gratis">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <rect x="1" y="3" width="15" height="13" rx="1"/><path d="M16 8h4l3 3v5h-7V8z"/>
        <circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>
      </svg>
      Frete Grátis — receba em até 5 dias úteis
    </div>

    <div class="resumo-linha">
      <span>Preço unitário</span>
      <span>R$ {{ "%.2f"|format(produto.preco) }}</span>
    </div>
    <div class="resumo-linha">
      <span>Quantidade</span>
      <span id="resumo-qtd">{{ quantidade }}x</span>
    </div>
    <div class="resumo-linha">
      <span>Desconto</span>
      <span class="resumo-desconto">{{ produto.desconto }}</span>
    </div>
    <div class="resumo-linha total">
      <span>Total</span>
      <span id="resumo-total">R$ {{ "%.2f"|format(produto.preco * quantidade) }}</span>
    </div>
    <p class="resumo-parcela" id="resumo-parcela">
      ou {{ produto.parcelas }}x de R$ {{ "%.2f"|format(produto.parcela_valor * quantidade) }} sem juros
    </p>

    <div class="selos">
      <div class="selo">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
        Compra 100% garantida
      </div>
      <div class="selo">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
          <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
        </svg>
        Pagamento criptografado
      </div>
      <div class="selo">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="2">
          <path d="M1 4v6h6"/><path d="M23 20v-6h-6"/>
          <path d="M20.49 9A9 9 0 005.64 5.64L1 10M23 14l-4.64 4.36A9 9 0 013.51 15"/>
        </svg>
        Devolução grátis em 30 dias
      </div>
    </div>
  </div>
</div>

<script>
  const PRECO_UNIT = {{ produto.preco }};
  const PARCELAS   = {{ produto.parcelas }};

  function changeQty(delta) {
    const input   = document.getElementById('qty-input');
    const display = document.getElementById('qty-display');
    let v = parseInt(input.value) + delta;
    if (v < 1) v = 1;
    if (v > 50) v = 50;
    input.value  = v;
    display.textContent = v;
    atualizarResumo(v);
  }

  function atualizarResumo(qtd) {
    const total   = (PRECO_UNIT * qtd).toFixed(2);
    const parcela = (PRECO_UNIT * qtd / PARCELAS).toFixed(2);
    document.getElementById('resumo-qtd').textContent   = qtd + 'x';
    document.getElementById('resumo-total').textContent = 'R$ ' + total;
    document.getElementById('resumo-parcela').textContent =
      'ou ' + PARCELAS + 'x de R$ ' + parcela + ' sem juros';
  }

  // Máscara CPF
  document.getElementById('cpf').addEventListener('input', function() {
    let v = this.value.replace(/\D/g,'').slice(0,11);
    v = v.replace(/(\d{3})(\d)/,'$1.$2')
         .replace(/(\d{3})(\d)/,'$1.$2')
         .replace(/(\d{3})(\d{1,2})$/,'$1-$2');
    this.value = v;
  });

  // Máscara Telefone
  document.getElementById('tel').addEventListener('input', function() {
    let v = this.value.replace(/\D/g,'').slice(0,11);
    if (v.length <= 10)
      v = v.replace(/(\d{2})(\d{4})(\d)/,'($1) $2-$3');
    else
      v = v.replace(/(\d{2})(\d{5})(\d)/,'($1) $2-$3');
    this.value = v;
  });

  // Loading no submit
  document.querySelector('form').addEventListener('submit', function() {
    const btn = document.getElementById('btn-submit');
    btn.textContent = 'Redirecionando…';
    btn.disabled = true;
  });
</script>
</body>
</html>
