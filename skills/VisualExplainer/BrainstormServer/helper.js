/**
 * BrainstormServer client-side WebSocket library
 *
 * Injected into every served page. Handles:
 * - WebSocket connection with auto-reconnect
 * - data-choice click handling and visual feedback
 * - Page reload on file changes
 * - Exposes window.brainstorm.send() and window.brainstorm.choice() APIs
 */
(function () {
  var ws = new WebSocket('ws://' + window.location.host);
  var queue = [];
  var connected = false;

  ws.onopen = function () {
    connected = true;
    queue.forEach(function (m) { ws.send(m); });
    queue.length = 0;
    var dot = document.getElementById('ws-status');
    if (dot) { dot.className = 'status-dot connected'; dot.title = 'Connected'; }
  };

  ws.onclose = function () {
    connected = false;
    var dot = document.getElementById('ws-status');
    if (dot) { dot.className = 'status-dot disconnected'; dot.title = 'Disconnected'; }
    setTimeout(function () { location.reload(); }, 1000);
  };

  ws.onmessage = function (e) {
    try {
      var msg = JSON.parse(e.data);
      if (msg.type === 'reload') location.reload();
    } catch (_) {}
  };

  function send(event) {
    var msg = JSON.stringify(event);
    if (connected) ws.send(msg); else queue.push(msg);
  }

  // Handle data-choice clicks
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-choice]');
    if (!el) return;
    var choice = el.dataset.choice;
    send({ type: 'choice', choice: choice, timestamp: new Date().toISOString() });

    // Visual feedback
    document.querySelectorAll('[data-choice]').forEach(function (c) {
      c.classList.remove('selected');
    });
    el.classList.add('selected');

    // Update indicator
    var indicator = document.getElementById('indicator');
    if (indicator) indicator.textContent = 'Choice sent: ' + choice;
  });

  window.brainstorm = {
    send: send,
    choice: function (c) { send({ type: 'choice', choice: c }); },
  };
})();
