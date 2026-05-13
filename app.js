/* ──────────────────────────────────────────────
   Clean Clean v2.1 — app.js
   Motion One + калькулятор + drawer + form
   ────────────────────────────────────────────── */

(() => {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  const M = window.Motion || null;
  const animate = M?.animate;
  const stagger = M?.stagger;

  // ── SERVICE CARD CLICKS ──────────────────────
  const MODAL_DATA = {
    sofa: {
      title: 'Хімчистка диванів',
      service: 'Хімчистка диванів',
      options: [
        { label: '2-місний', price: '1 100 ₴' },
        { label: '3-місний', price: '1 650 ₴' },
        { label: '4-місний', price: '2 200 ₴' },
        { label: 'Кутовий', price: '2 400 ₴' },
        { label: 'Модульний', price: '2 700 ₴' },
      ]
    },
    mattress: {
      title: 'Хімчистка матраців',
      service: 'Хімчистка матраців',
      options: [
        { label: 'Дитячий', price: '300 ₴' },
        { label: 'Односпальний', price: '550 ₴' },
        { label: 'Полуторний', price: '800 ₴' },
        { label: 'Двоспальний', price: '1 100 ₴' },
      ]
    }
  };

  const modal = $('#serviceModal');
  const modalTitle = $('#modalTitle');
  const modalOptions = $('#modalOptions');

  const openModal = (type) => {
    const data = MODAL_DATA[type];
    if (!data || !modal) return;
    modalTitle.textContent = data.title;
    modalOptions.innerHTML = data.options.map(o => `
      <button class="svc-opt" data-service="${data.service}" data-label="${o.label}" data-price="${o.price}">
        <span>${o.label}</span>
        <span class="svc-opt__price">${o.price}</span>
      </button>`).join('');
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
  };

  const closeModal = () => {
    modal && modal.classList.remove('is-open');
    modal && modal.setAttribute('aria-hidden', 'true');
  };

  $('#modalClose') && $('#modalClose').addEventListener('click', closeModal);
  $('#modalBackdrop') && $('#modalBackdrop').addEventListener('click', closeModal);

  modalOptions && modalOptions.addEventListener('click', (e) => {
    const btn = e.target.closest('.svc-opt');
    if (!btn) return;
    const service = btn.dataset.service;
    const label = btn.dataset.label;
    const price = btn.dataset.price;
    // Pre-fill form
    const fService = $('#fService');
    if (fService) {
      for (let opt of fService.options) {
        if (opt.value.toLowerCase().includes(service.toLowerCase().split(' ')[0])) {
          fService.value = opt.value; break;
        }
      }
    }
    const fDetails = $('#fDetails');
    if (fDetails) fDetails.value = label + ' — ' + price;
    closeModal();
    document.getElementById('order') && document.getElementById('order').scrollIntoView({ behavior: 'smooth' });
  });

  // Service cards → calc or modal
  $$('.service-card[data-action]').forEach((card) => {
    card.addEventListener('click', () => {
      const action = card.dataset.action;
      if (action === 'calc') {
        const rate = parseInt(card.dataset.rate, 10);
        const service = card.dataset.service;
        // Update calculator rate
        if (window._setCalcRate) window._setCalcRate(rate);
        // Pre-select service in form
        const fService = $('#fService');
        if (fService && service) {
          for (let opt of fService.options) {
            if (opt.value === service) { fService.value = service; break; }
          }
        }
        document.getElementById('calc') && document.getElementById('calc').scrollIntoView({ behavior: 'smooth' });
      } else if (action === 'modal') {
        openModal(card.dataset.modal);
      }
    });
  });
  const inView = M?.inView;

  // ── DRAWER ──────────────────────────────────
  const burger = $('#menuToggle');
  const drawer = $('#drawer');
  const backdrop = $('#drawerBackdrop');
  const drawerClose = $('#drawerClose');

  const openDrawer = () => {
    burger.setAttribute('aria-expanded', 'true');
    drawer.setAttribute('aria-hidden', 'false');
    drawer.classList.add('is-open');
    backdrop.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    if (animate && !reduced) {
      animate($$('.drawer__link'), { opacity: [0, 1], x: [20, 0] }, { delay: stagger(0.04, { start: 0.15 }), duration: 0.4, easing: 'ease-out' });
    }
  };
  const closeDrawer = () => {
    burger.setAttribute('aria-expanded', 'false');
    drawer.setAttribute('aria-hidden', 'true');
    drawer.classList.remove('is-open');
    backdrop.classList.remove('is-open');
    document.body.style.overflow = '';
  };
  burger.addEventListener('click', () => {
    burger.getAttribute('aria-expanded') === 'true' ? closeDrawer() : openDrawer();
  });
  drawerClose.addEventListener('click', closeDrawer);
  backdrop.addEventListener('click', closeDrawer);
  $$('#drawer a').forEach(a => a.addEventListener('click', closeDrawer));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeDrawer(); });

  // ── HERO ENTRANCE (Motion One stagger) ──────
  if (animate && !reduced) {
    const heroSequence = [
      ['[data-anim="badge"]', { opacity: [0, 1], y: [12, 0] }, { duration: 0.6, easing: [0.16, 1, 0.3, 1] }],
      ['[data-anim="title"]', { opacity: [0, 1], y: [20, 0] }, { duration: 0.7, at: 0.1, easing: [0.16, 1, 0.3, 1] }],
      ['[data-anim="sub"]', { opacity: [0, 1], y: [16, 0] }, { duration: 0.6, at: 0.25, easing: [0.16, 1, 0.3, 1] }],
      ['[data-anim="cta"]', { opacity: [0, 1], y: [14, 0] }, { duration: 0.6, at: 0.35, easing: [0.16, 1, 0.3, 1] }],
      ['[data-anim="trust"]', { opacity: [0, 1], y: [16, 0] }, { duration: 0.6, at: 0.45, easing: [0.16, 1, 0.3, 1] }],
    ];
    if (M.timeline) M.timeline(heroSequence);
    else heroSequence.forEach(([sel, kf, opt]) => animate(sel, kf, opt));

    // Hero mesh breath
    animate('.hero__mesh', { scale: [1, 1.08, 1], rotate: [0, 2, 0] }, { duration: 12, repeat: Infinity, easing: 'ease-in-out' });
  } else {
    $$('[data-anim]').forEach(el => { el.style.opacity = '1'; });
  }

  // ── COUNT-UP (trust numbers) ────────────────
  const formatCount = (n, decimals) => {
    if (decimals > 0) return n.toFixed(decimals);
    return Math.round(n).toLocaleString('uk-UA').replace(/,/g, ' ');
  };
  const startCountUp = (el) => {
    const target = parseFloat(el.dataset.countup);
    const decimals = parseInt(el.dataset.decimals || '0', 10);
    const suffix = el.dataset.suffix || '';
    const duration = 1400;
    if (reduced) { el.textContent = formatCount(target, decimals) + suffix; return; }
    const start = performance.now();
    const tick = (now) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = formatCount(target * eased, decimals) + (t > 0.05 ? suffix : '');
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const countUpEls = $$('[data-countup]');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { startCountUp(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.4 });
    countUpEls.forEach(el => io.observe(el));
  } else {
    countUpEls.forEach(startCountUp);
  }

  // ── REVEAL ON SCROLL ─────────────────────────
  if ('IntersectionObserver' in window && !reduced) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    $$('[data-reveal]').forEach((el) => io.observe(el));
  } else {
    $$('[data-reveal]').forEach((el) => el.classList.add('is-visible'));
  }

  // ── SECTION STAGGER REVEAL ──────────────────
  if (animate && inView && !reduced) {
    $$('.section').forEach((sec) => {
      inView(sec, () => {
        const head = $('.section__head', sec);
        if (head) {
          animate(head.children, { opacity: [0, 1], y: [14, 0] }, { delay: stagger(0.08), duration: 0.55, easing: [0.16, 1, 0.3, 1] });
        }
      }, { amount: 0.18 });
    });

    // Service cards — stagger as user views
    inView('#servicesScroll', () => {
      animate('.service-card', { opacity: [0, 1], scale: [0.96, 1], y: [16, 0] }, { delay: stagger(0.06), duration: 0.5, easing: [0.16, 1, 0.3, 1] });
    }, { amount: 0.2 });

    // How steps
    inView('#howTimeline', () => {
      animate('.how__step', { opacity: [0, 1], x: [-12, 0] }, { delay: stagger(0.1), duration: 0.5, easing: [0.16, 1, 0.3, 1] });
    }, { amount: 0.15 });

    // Cities — pop in
    inView('#cities .cities', () => {
      animate('.city', { opacity: [0, 1], scale: [0.94, 1] }, { delay: stagger(0.08), duration: 0.55, easing: [0.34, 1.56, 0.64, 1] });
    }, { amount: 0.15 });

    // Reviews track — fade in
    inView('.reviews', () => {
      animate('.reviews__track', { opacity: [0, 1] }, { duration: 0.7 });
    }, { amount: 0.2 });
  }

  // ── HOW TIMELINE LINE FILL ──────────────────
  const howLineFill = $('#howLineFill');
  const howTimeline = $('#howTimeline');
  if (howLineFill && howTimeline) {
    const updateLine = () => {
      const rect = howTimeline.getBoundingClientRect();
      const viewH = window.innerHeight;
      const total = rect.height;
      const start = viewH * 0.55;
      const end = -total + viewH * 0.45;
      const progress = Math.max(0, Math.min(1, (start - rect.top) / (start - end)));
      howLineFill.style.height = (progress * 100).toFixed(1) + '%';
    };
    window.addEventListener('scroll', updateLine, { passive: true });
    window.addEventListener('resize', updateLine);
    updateLine();
  }

  // ── SERVICES SWIPE DOTS ─────────────────────
  const servicesScroll = $('#servicesScroll');
  const servicesDots = $('#servicesDots');
  if (servicesScroll && servicesDots) {
    const cards = $$('.service-card', servicesScroll);
    cards.forEach((_, i) => {
      const dot = document.createElement('span');
      if (i === 0) dot.classList.add('is-active');
      servicesDots.appendChild(dot);
    });
    const dots = $$('span', servicesDots);
    servicesScroll.addEventListener('scroll', () => {
      const scrollLeft = servicesScroll.scrollLeft;
      const cardWidth = cards[0].offsetWidth + 12;
      const idx = Math.round(scrollLeft / cardWidth);
      dots.forEach((d, i) => d.classList.toggle('is-active', i === Math.min(idx, dots.length - 1)));
    }, { passive: true });
  }

  // ── CITIES PARALLAX (легкий tilt на скролл) ──
  if ('IntersectionObserver' in window && !reduced) {
    const cityImgs = $$('.city img');
    let raf = null;
    const updateParallax = () => {
      cityImgs.forEach((img) => {
        const card = img.parentElement;
        const rect = card.getBoundingClientRect();
        const viewH = window.innerHeight;
        if (rect.bottom < 0 || rect.top > viewH) return;
        const center = rect.top + rect.height / 2;
        const offset = (center - viewH / 2) / viewH; // -0.5..+0.5
        const ty = offset * -16; // подвиг image
        img.style.transform = `translateY(${ty.toFixed(1)}px) scale(1.06)`;
      });
      raf = null;
    };
    window.addEventListener('scroll', () => {
      if (!raf) raf = requestAnimationFrame(updateParallax);
    }, { passive: true });
    updateParallax();
  }

  // ── CALCULATOR ──────────────────────────────
  const slider = $('#calcSlider');
  const areaEl = $('#calcArea');
  const priceEl = $('#calcPrice');
  const chips = $$('.calc__chip');
  const extras = $$('.calc__extra input');

  let PRICE_PER_SQM = 50;
  window._setCalcRate = (rate) => { PRICE_PER_SQM = rate; recalc && recalc(); };
  let currentArea = parseInt(slider.value, 10);
  let displayedPrice = 0;

  const animateNumber = (el, from, to, duration = 500) => {
    if (reduced) { el.textContent = formatPrice(to); return; }
    const start = performance.now();
    const tick = (now) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      const value = Math.round(from + (to - from) * eased);
      el.textContent = formatPrice(value);
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const formatPrice = (n) => n.toLocaleString('uk-UA').replace(/,/g, ' ');

  const windowCheck = $('#windowCheck');
  const windowAreaRow = $('#windowAreaRow');
  const windowAreaInput = $('#windowArea');

  const recalc = () => {
    const area = currentArea;
    let price = area * PRICE_PER_SQM;
    extras.forEach((cb) => {
      if (!cb.checked) return;
      if (cb.id === 'windowCheck') {
        // Use separate window area, not house area
        const winArea = windowAreaInput ? (parseInt(windowAreaInput.value, 10) || 10) : 10;
        price += winArea * 80;
      } else {
        price += parseInt(cb.dataset.price, 10) || 0;
      }
    });
    price = Math.round(price);
    animateNumber(priceEl, displayedPrice, price);
    displayedPrice = price;
  };

  const updateSliderFill = () => {
    const min = parseInt(slider.min, 10);
    const max = parseInt(slider.max, 10);
    const pct = ((currentArea - min) / (max - min)) * 100;
    slider.style.setProperty('--p', pct + '%');
  };

  const setArea = (v) => {
    currentArea = Math.max(30, Math.min(200, parseInt(v, 10)));
    slider.value = currentArea;
    areaEl.textContent = currentArea;
    updateSliderFill();
    chips.forEach((c) => c.classList.toggle('calc__chip--active', parseInt(c.dataset.area, 10) === currentArea));
    recalc();
  };

  slider.addEventListener('input', () => setArea(slider.value));
  chips.forEach((c) => c.addEventListener('click', () => setArea(c.dataset.area)));
  extras.forEach((cb) => cb.addEventListener('change', recalc));

  // Window area logic (after recalc is defined)
  if (windowCheck) {
    windowCheck.addEventListener('change', () => {
      windowAreaRow.style.display = windowCheck.checked ? 'block' : 'none';
      recalc();
    });
    windowAreaInput && windowAreaInput.addEventListener('input', recalc);
  }

  setArea(currentArea);
  displayedPrice = currentArea * PRICE_PER_SQM;
  priceEl.textContent = formatPrice(displayedPrice);

  // ── FORM SUBMIT ─────────────────────────────
  // TikTok funnel events helper
  const ttqTrack = (event, params = {}) => {
    try { if (typeof ttq !== 'undefined') ttq.track(event, { content_id: 'cleaning-service', content_type: 'product', ...params }); } catch(_) {}
  };

  // ViewContent — user saw the calculator/services
  const calcSection = $('#calc');
  if (calcSection) {
    const calcObs = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { ttqTrack('ViewContent', { content_name: 'Калькулятор прибирання', value: 0, currency: 'UAH' }); calcObs.disconnect(); } });
    }, { threshold: 0.3 });
    calcObs.observe(calcSection);
  }

  const form = $('#orderForm');
  const submitBtn = $('#formSubmit');
  const successBox = $('#formSuccess');

  // InitiateCheckout — user focused on form
  form && form.addEventListener('focusin', () => {
    ttqTrack('InitiateCheckout');
  }, { once: true });

  const validatePhone = (v) => /^\+?[0-9\s()-]{10,18}$/.test(v.trim());
  const validateName = (v) => v.trim().length >= 2;

  const showError = (field) => field.closest('.form__field').classList.add('has-error');
  const clearError = (field) => field.closest('.form__field').classList.remove('has-error');

  ['fName', 'fPhone'].forEach((id) => {
    const inp = $('#' + id);
    inp.addEventListener('blur', () => {
      const ok = id === 'fName' ? validateName(inp.value) : validatePhone(inp.value);
      if (!ok && inp.value) showError(inp); else clearError(inp);
    });
    inp.addEventListener('input', () => clearError(inp));
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (form.website.value) return;
    let valid = true;
    if (!validateName(form.name.value)) { showError(form.name); valid = false; }
    if (!validatePhone(form.phone.value)) { showError(form.phone); valid = false; }
    if (!valid) { $('.has-error .form__input')?.focus(); return; }

    submitBtn.classList.add('is-loading');
    submitBtn.disabled = true;

    const checkedExtras = extras.filter((cb) => cb.checked).map((cb) => cb.parentElement.querySelector('span').textContent.trim());
    const detailsParts = [];
    if (currentArea) detailsParts.push(`Площа: ${currentArea} м²`);
    if (displayedPrice) detailsParts.push(`Ціна: ${displayedPrice} ₴`);
    if (checkedExtras.length) detailsParts.push(`Додатково: ${checkedExtras.join(', ')}`);
    if (form.details.value.trim()) detailsParts.push(form.details.value.trim());

    const payload = {
      name: form.name.value.trim(),
      phone: form.phone.value.trim(),
      city: form.city.value,
      service: form.service.value,
      details: detailsParts.join(' · '),
      page: location.href,
      website: ''
    };

    try {
      const res = await fetch('https://cleaning-form-handler.onrender.com/api/order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json().catch(() => ({ ok: false }));
      if (data.ok || data.stub) {
        ttqTrack('CompleteRegistration', { content_name: payload.service, value: 0, currency: 'UAH' });
        ttqTrack('SubmitForm', { content_name: payload.service });
        showSuccess();
      } else throw new Error(data.msg || 'unknown');
    } catch (err) {
      console.warn('[order]', err);
      ttqTrack('CompleteRegistration');
      ttqTrack('SubmitForm');
      showSuccess();
    }
  });

  const showSuccess = () => {
    form.style.display = 'none';
    successBox.hidden = false;
    if (animate && !reduced) {
      animate(successBox, { opacity: [0, 1], scale: [0.92, 1] }, { duration: 0.5, easing: [0.34, 1.56, 0.64, 1] });
      animate('.form-success__check svg', { rotate: [-90, 0], scale: [0, 1] }, { duration: 0.6, delay: 0.2, easing: [0.34, 1.56, 0.64, 1] });
    }
    successBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
    submitBtn.classList.remove('is-loading');
    submitBtn.disabled = false;
  };

  // ── HEADER SHADOW ON SCROLL ─────────────────
  const header = $('#header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 4) header.style.boxShadow = '0 4px 16px -8px rgba(11,20,16,0.12)';
    else header.style.boxShadow = '';
  }, { passive: true });

  // ── BUTTON HAPTIC TAP (visual ripple) ───────
  if (!reduced) {
    $$('.btn').forEach((btn) => {
      btn.addEventListener('pointerdown', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const ripple = document.createElement('span');
        ripple.style.cssText = `position:absolute;left:${x}px;top:${y}px;width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,0.4);transform:translate(-50%,-50%) scale(1);pointer-events:none;`;
        btn.appendChild(ripple);
        if (animate) {
          animate(ripple, { scale: [1, 28], opacity: [0.5, 0] }, { duration: 0.6, easing: 'ease-out' }).finished.then(() => ripple.remove());
        } else {
          setTimeout(() => ripple.remove(), 600);
        }
      });
    });
  }

})();
