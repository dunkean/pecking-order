// Render every option as ordinary DOM: no native popup or virtualized rows.
(() => {
  const normalize = text => text.normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase();
  let opened;
  for (const select of document.querySelectorAll('select')) {
    const wrapper = document.createElement('div'); wrapper.className = 'combo';
    select.before(wrapper); wrapper.append(select);
    select.classList.add('combo-source'); select.tabIndex = -1; select.setAttribute('aria-hidden', 'true');
    const trigger = document.createElement('button'); trigger.type = 'button'; trigger.className = 'combo-trigger';
    trigger.id = `${select.id}-trigger`; trigger.setAttribute('role', 'combobox');
    trigger.setAttribute('aria-expanded', 'false'); trigger.setAttribute('aria-haspopup', 'listbox');
    const panel = document.createElement('div'); panel.className = 'combo-panel'; panel.hidden = true;
    const search = document.createElement('input'); search.type = 'search'; search.autocomplete = 'off';
    const status = document.createElement('div'); status.className = 'combo-status'; status.setAttribute('role', 'status');
    const list = document.createElement('div'); list.className = 'combo-list'; list.id = `${select.id}-options`;
    list.setAttribute('role', 'listbox'); trigger.setAttribute('aria-controls', list.id);
    panel.append(search, status, list); wrapper.append(trigger, panel);
    let active = -1, rows = [];
    function sync() {
      const label = select.closest('label')?.querySelector('span')?.textContent || select.id;
      trigger.textContent = select.selectedOptions[0]?.textContent || '—';
      trigger.setAttribute('aria-label', `${label} : ${trigger.textContent}`);
      trigger.disabled = select.disabled; search.setAttribute('aria-label', label);
      const fr = document.documentElement.lang !== 'en';
      search.placeholder = fr ? 'Rechercher dans la liste…' : 'Search this list…';
      list.setAttribute('aria-label', label);
      if (!panel.hidden) render();
    }
    function render() {
      const needle = normalize(search.value);
      rows = Array.from(select.options).filter(option => !option.hidden && !option.disabled && normalize(`${option.textContent} ${option.value}`).includes(needle));
      list.replaceChildren(...rows.map((option, i) => {
        const row = document.createElement('div'); row.className = 'combo-option'; row.id = `${select.id}-option-${i}`;
        row.setAttribute('role', 'option'); row.setAttribute('aria-selected', String(option.selected));
        row.textContent = option.textContent; row.addEventListener('click', event => { event.preventDefault(); choose(i); });
        return row;
      }));
      status.textContent = `${rows.length} / ${Array.from(select.options).filter(o => !o.hidden && !o.disabled).length}`;
      active = rows.findIndex(option => option.selected); highlight(false);
    }
    function highlight(scroll = true) {
      Array.from(list.children).forEach((row, i) => row.classList.toggle('combo-active', i === active));
      if (active >= 0) {
        search.setAttribute('aria-activedescendant', list.children[active].id);
        if (scroll) list.children[active].scrollIntoView({block: 'nearest'});
      } else search.removeAttribute('aria-activedescendant');
    }
    function close(focus = false) {
      panel.hidden = true; trigger.setAttribute('aria-expanded', 'false');
      if (opened === close) opened = undefined;
      if (focus) trigger.focus();
    }
    function choose(i) {
      if (!rows[i]) return;
      select.value = rows[i].value; close(true); sync();
      select.dispatchEvent(new Event('input', {bubbles: true}));
      select.dispatchEvent(new Event('change', {bubbles: true}));
    }
    function open() {
      if (select.disabled) return;
      opened?.(); opened = close; panel.hidden = false; trigger.setAttribute('aria-expanded', 'true');
      search.value = ''; sync();
      const box = trigger.getBoundingClientRect();
      const width = Math.min(Math.max(box.width, 300), innerWidth - 24);
      const below = innerHeight - box.bottom - 12, above = box.top - 12;
      const up = below < 240 && above > below;
      const height = Math.max(100, Math.min(360, up ? above : below));
      Object.assign(panel.style, {position:'fixed', width:`${width}px`, maxHeight:`${height}px`, left:`${Math.max(12, Math.min(box.left, innerWidth-width-12))}px`, top:up?'auto':`${box.bottom+4}px`, bottom:up?`${innerHeight-box.top+4}px`:'auto'});
      list.scrollTop = 0; search.focus();
    }
    trigger.addEventListener('click', event => { event.preventDefault(); panel.hidden ? open() : close(); });
    trigger.addEventListener('keydown', event => {
      if (['ArrowDown','ArrowUp','Home','End'].includes(event.key)) { event.preventDefault(); open(); if(event.key==='End'){active=rows.length-1;highlight();} }
    });
    search.addEventListener('input', render);
    search.addEventListener('keydown', event => {
      if (event.key === 'Escape') { event.preventDefault(); close(true); }
      else if (event.key === 'Enter') { event.preventDefault(); choose(active < 0 ? 0 : active); }
      else if (['ArrowDown','ArrowUp','Home','End'].includes(event.key)) {
        event.preventDefault(); active = event.key === 'Home' ? 0 : event.key === 'End' ? rows.length-1 : Math.max(0, Math.min(rows.length-1, active+(event.key==='ArrowDown'?1:-1))); highlight();
      }
    });
    wrapper.addEventListener('focusout', () => queueMicrotask(() => { if (!wrapper.contains(document.activeElement)) close(); }));
    document.addEventListener('pointerdown', event => { if (!wrapper.contains(event.target)) close(); });
    select.addEventListener('change', sync);
    new MutationObserver(sync).observe(select, {subtree:true, childList:true, characterData:true, attributes:true, attributeFilter:['disabled','selected','hidden']});
    window.addEventListener('resize', () => close());
    window.addEventListener('scroll', event => { if (!panel.contains(event.target)) close(); }, true);
    sync();
  }
})();
