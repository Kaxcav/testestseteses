// visitor-tracker.js — Mercado de Ofertas
class VisitorTracker {
  constructor() {
    this.sessionId   = this.getOrCreateSessionId();
    this.visitorId   = this.getOrCreateVisitorId();
    this.firstVisit  = this.checkFirstVisit();
    this.visitCount  = this.getVisitCount();
  }

  getOrCreateSessionId() {
    let id = sessionStorage.getItem('sessionId');
    if (!id) {
      id = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      sessionStorage.setItem('sessionId', id);
    }
    return id;
  }

  getOrCreateVisitorId() {
    let id = localStorage.getItem('visitorId');
    if (!id) {
      id = 'visitor_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('visitorId', id);
    }
    return id;
  }

  checkFirstVisit() {
    if (!localStorage.getItem('firstVisit')) {
      localStorage.setItem('firstVisit', new Date().toISOString());
      return true;
    }
    return false;
  }

  getVisitCount() {
    let count = parseInt(localStorage.getItem('visitCount') || '0');
    count++;
    localStorage.setItem('visitCount', count.toString());
    return count;
  }

  getBrowserInfo() {
    return {
      userAgent:        navigator.userAgent,
      language:         navigator.language,
      platform:         navigator.platform,
      screenResolution: screen.width + 'x' + screen.height,
      timezone:         Intl.DateTimeFormat().resolvedOptions().timeZone,
      referrer:         document.referrer || 'direct',
      landingPage:      window.location.href
    };
  }

  async saveVisitorData() {
    // Só envia se o usuário aceitou cookies
    if (localStorage.getItem('cookie_consent') !== 'accepted') return;

    const data = {
      visitorId:  this.visitorId,
      sessionId:  this.sessionId,
      firstVisit: this.firstVisit,
      visitCount: this.visitCount,
      timestamp:  new Date().toISOString(),
      ...this.getBrowserInfo()
    };

    try {
      await fetch('/api/visitor-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
    } catch (e) {}
  }

  trackAction(action, details = {}) {
    if (localStorage.getItem('cookie_consent') !== 'accepted') return;

    fetch('/api/user-action', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        visitorId: this.visitorId,
        sessionId: this.sessionId,
        action,
        details,
        timestamp: new Date().toISOString(),
        page: window.location.pathname
      })
    }).catch(() => {});
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.visitorTracker = new VisitorTracker();
  window.visitorTracker.saveVisitorData();
  window.visitorTracker.trackAction('page_view');

  // Cliques em links
  document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      window.visitorTracker.trackAction('link_click', {
        url: link.href, text: link.textContent.trim().slice(0, 60)
      });
    });
  });

  // Botão carrinho
  const btnCart = document.getElementById('btnCart');
  if (btnCart) btnCart.addEventListener('click', () =>
    window.visitorTracker.trackAction('add_to_cart'));

  // Botão comprar
  const btnBuy = document.getElementById('btnBuy');
  if (btnBuy) btnBuy.addEventListener('click', () =>
    window.visitorTracker.trackAction('begin_checkout'));
});
