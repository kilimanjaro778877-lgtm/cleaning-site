import os, re

BASE = r"C:\Users\Admin\cleaning-site"

UPSELL_BLOCK = '''        <!-- UPSELL: Additional services -->
        <div class="mt-4">
          <button type="button" class="upsell-toggle flex items-center justify-between w-full px-4 py-3 rounded-xl bg-green-50 border border-green-200 text-left hover:bg-green-100 transition">
            <span class="text-sm font-bold text-green-800">+ Додати до замовлення</span>
            <svg class="upsell-arrow w-4 h-4 text-green-600 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="upsell-content hidden mt-2 p-4 bg-gray-50 border border-gray-200 rounded-xl">
            <p class="text-xs text-gray-500 mb-3">Оберіть — додамо до заявки та врахуємо при розрахунку</p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <label class="upsell-item flex items-center gap-3 p-3 rounded-xl border border-gray-200 bg-white cursor-pointer hover:border-green-400 transition">
                <input type="checkbox" data-extra="Миття вікон +80₴/м²" class="upsell-check w-4 h-4 accent-green-600">
                <div><div class="text-sm font-semibold text-gray-900">Миття вікон</div><div class="text-xs text-gray-500">+80₴/м²</div></div>
              </label>
              <label class="upsell-item flex items-center gap-3 p-3 rounded-xl border border-gray-200 bg-white cursor-pointer hover:border-green-400 transition">
                <input type="checkbox" data-extra="Духовка +600₴" class="upsell-check w-4 h-4 accent-green-600">
                <div><div class="text-sm font-semibold text-gray-900">Духовка</div><div class="text-xs text-gray-500">+600₴</div></div>
              </label>
              <label class="upsell-item flex items-center gap-3 p-3 rounded-xl border border-gray-200 bg-white cursor-pointer hover:border-green-400 transition">
                <input type="checkbox" data-extra="Холодильник +500₴" class="upsell-check w-4 h-4 accent-green-600">
                <div><div class="text-sm font-semibold text-gray-900">Холодильник</div><div class="text-xs text-gray-500">+500₴</div></div>
              </label>
              <label class="upsell-item flex items-center gap-3 p-3 rounded-xl border border-gray-200 bg-white cursor-pointer hover:border-green-400 transition">
                <input type="checkbox" data-extra="Витяжка +500₴" class="upsell-check w-4 h-4 accent-green-600">
                <div><div class="text-sm font-semibold text-gray-900">Витяжка</div><div class="text-xs text-gray-500">+500₴</div></div>
              </label>
              <label class="upsell-item flex items-center gap-3 p-3 rounded-xl border border-gray-200 bg-white cursor-pointer hover:border-green-400 transition">
                <input type="checkbox" data-extra="Хімчистка дивана +1100₴" class="upsell-check w-4 h-4 accent-green-600">
                <div><div class="text-sm font-semibold text-gray-900">Хімчистка дивана</div><div class="text-xs text-gray-500">+1100₴</div></div>
              </label>
              <label class="upsell-item flex items-center gap-3 p-3 rounded-xl border border-gray-200 bg-white cursor-pointer hover:border-green-400 transition">
                <input type="checkbox" data-extra="Хімчистка матраця +550₴" class="upsell-check w-4 h-4 accent-green-600">
                <div><div class="text-sm font-semibold text-gray-900">Хімчистка матраця</div><div class="text-xs text-gray-500">+550₴</div></div>
              </label>
            </div>
          </div>
        </div>
'''

UPSELL_JS = '''
    // Upsell toggle
    document.querySelectorAll('.upsell-toggle').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var content = this.parentElement.querySelector('.upsell-content');
        var arrow = this.querySelector('.upsell-arrow');
        content.classList.toggle('hidden');
        arrow.style.transform = content.classList.contains('hidden') ? '' : 'rotate(180deg)';
      });
    });
    // Upsell checkbox visual feedback
    document.querySelectorAll('.upsell-check').forEach(function(cb) {
      cb.addEventListener('change', function() {
        var label = this.closest('label');
        if (this.checked) {
          label.style.borderColor = '#22c55e';
          label.style.background = '#f0fdf4';
        } else {
          label.style.borderColor = '';
          label.style.background = '';
        }
      });
    });
'''

# Insert point: before submit button
BEFORE_SUBMIT = '<button type="submit" class="btn-3d mt-6 w-full'

def get_html_files():
    result = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'img', 'blog']]
        for f in files:
            if f.endswith('.html'):
                result.append(os.path.join(root, f))
    return result

total = 0
for path in get_html_files():
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if 'upsell-toggle' in html:
        print(f"SKIP (already has upsell): {os.path.basename(path)}")
        continue

    if BEFORE_SUBMIT not in html:
        print(f"no form: {os.path.basename(path)}")
        continue

    new = html.replace(BEFORE_SUBMIT, UPSELL_BLOCK + '        ' + BEFORE_SUBMIT[8:], 1)

    # Inject JS before </body>
    if UPSELL_JS.strip() not in new:
        new = new.replace('</body>', '<script>' + UPSELL_JS + '</script>\n</body>', 1)

    if new != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        total += 1
        print(f"UPDATED: {os.path.relpath(path, BASE)}")

print(f"\nDone — {total} files updated.")
