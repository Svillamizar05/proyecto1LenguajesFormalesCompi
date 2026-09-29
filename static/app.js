'use strict';
const byId = id => document.getElementById(id);
const official = {
  dfaStates: [0, 1, 2, 3, 4, 5], alphabet: ['a', 'b'], initialState: 0,
  acceptingStates: [1, 4, 5],
  transitions: [[1, 2], [3, 4], [4, 3], [5, 5], [5, 5], [5, 5]].flatMap(
    (row, state) => row.map((to, i) => ({from: state, symbol: ['a', 'b'][i], to})))
};
const nfaExample = {states: [0, 1, 2, 3], alphabet: ['a', 'b'], initial: 0, accepting: [3],
  transitions: [{from: 0, symbol: 'a', to: 1}, {from: 0, symbol: 'a', to: 2},
    {from: 1, symbol: 'b', to: 3}, {from: 2, symbol: 'b', to: 3}]};
let tableStates = [], tableAlphabet = [];
function node(tag, text, className) {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = text;
  if (className) el.className = className;
  return el;
}
function parse(id) {
  try { return JSON.parse(byId(id).value); }
  catch (_) { throw new Error(`Invalid JSON in ${byId(id).closest('label').firstChild.textContent.trim()}.`); }
}
function resultBody(id) { return byId(id).querySelector('.result-body'); }
function showError(id, error) { resultBody(id).replaceChildren(node('p', error.message, 'error')); }
function rawResult(container, data) {
  const details = node('details'); details.append(node('summary', 'View API response'), node('pre', JSON.stringify(data, null, 2))); container.append(details);
}
function showTab(id) {
  document.querySelectorAll('.tool').forEach(section => { section.hidden = section.id !== id; });
  document.querySelectorAll('nav button').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.panel === id)));
}
document.querySelectorAll('nav button').forEach(button => button.addEventListener('click', () => showTab(button.dataset.panel)));
function buildTable(transitions = []) {
  const states = parse('min-states'), alphabet = parse('min-alphabet');
  if (!Array.isArray(states) || !Array.isArray(alphabet)) throw new Error('States and alphabet must be JSON arrays.');
  tableStates = states; tableAlphabet = alphabet;
  const table = node('table'), head = node('thead'), header = node('tr');
  header.append(node('th', 'State')); alphabet.forEach(symbol => header.append(node('th', String(symbol)))); head.append(header); table.append(head);
  const body = node('tbody');
  states.forEach((state, i) => {
    const row = node('tr'); const heading = node('th', String(state)); heading.scope = 'row'; row.append(heading);
    alphabet.forEach((symbol, j) => {
      const cell = node('td'), input = node('input'); input.type = 'text'; input.dataset.row = i; input.dataset.col = j;
      input.setAttribute('aria-label', `From ${state} with ${symbol}`);
      const transition = transitions.find(t => t.from === state && t.symbol === symbol);
      input.value = transition ? JSON.stringify(transition.to) : ''; input.placeholder = '—'; cell.append(input); row.append(cell);
    }); body.append(row);
  }); table.append(body); byId('transition-table').replaceChildren(table);
}
function tableTransitions() {
  return [...byId('transition-table').querySelectorAll('input')].filter(input => input.value.trim() !== '').map(input => {
    let to; try { to = JSON.parse(input.value); } catch (_) { throw new Error(`Invalid destination for ${input.getAttribute('aria-label')}. Use a number or quoted string.`); }
    return {from: tableStates[Number(input.dataset.row)], symbol: tableAlphabet[Number(input.dataset.col)], to};
  });
}
function loadMinimize() {
  for (const [id, key] of [['min-states','dfaStates'],['min-alphabet','alphabet'],['min-initial','initialState'],['min-accepting','acceptingStates']]) byId(id).value = JSON.stringify(official[key]);
  buildTable(official.transitions); resultBody('min-result').replaceChildren(node('p', 'Example loaded. Find the equivalent states to see the server result.', 'empty'));
}
byId('load-minimize').addEventListener('click', loadMinimize);
byId('build-table').addEventListener('click', () => { try { buildTable(tableTransitions()); resultBody('min-result').replaceChildren(node('p', 'Table updated. Submit to see the server result.', 'empty')); } catch (error) { showError('min-result', error); } });
function loadNfa() {
  for (const key of ['states', 'alphabet', 'initial', 'accepting', 'transitions']) byId(`nfa-${key}`).value = JSON.stringify(nfaExample[key], null, key === 'transitions' ? 2 : 0);
  resultBody('convert-result').replaceChildren(node('p', 'Example loaded. Convert to see the server result.', 'empty'));
}
byId('load-convert').addEventListener('click', loadNfa);
byId('load-simulate').addEventListener('click', () => { byId('sim-dfa').value = JSON.stringify(official, null, 2); byId('sim-input').value = 'a'; resultBody('sim-result').replaceChildren(node('p', 'Example loaded. Simulate to see the server result.', 'empty')); });
async function submit(form, endpoint, output, payload, render) {
  const button = form.querySelector('[type=submit]'); button.disabled = true;
  const container = resultBody(output); container.replaceChildren(node('p', 'Waiting for the server…', 'empty')); container.setAttribute('aria-busy', 'true');
  try {
    const data = payload();
    const response = await fetch(endpoint, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || `Request failed (HTTP ${response.status}).`);
    container.replaceChildren(); render(container, result); rawResult(container, result);
  } catch (error) { showError(output, error); }
  finally { button.disabled = false; container.setAttribute('aria-busy', 'false'); }
}
byId('minimize-form').addEventListener('submit', event => {
  event.preventDefault(); submit(event.currentTarget, '/minimize', 'min-result', () => {
    const states = parse('min-states'), alphabet = parse('min-alphabet');
    if (JSON.stringify(states) !== JSON.stringify(tableStates) || JSON.stringify(alphabet) !== JSON.stringify(tableAlphabet)) throw new Error('States or alphabet changed. Click Update table before submitting.');
    return {dfaStates: states, alphabet, initialState: parse('min-initial'), acceptingStates: parse('min-accepting'), transitions: tableTransitions()};
  }, (container, result) => {
    const pairs = node('div', undefined, 'pair-list');
    result.equivalentPairs.forEach(pair => pairs.append(node('div', `{${pair.join(', ')}}`, 'pair')));
    container.append(result.equivalentPairs.length ? pairs : node('p', 'No equivalent pairs of distinct states.', 'detail'));
    container.append(node('p', 'Pairs returned by the server · Kozen Lecture 14', 'detail'));
  });
});
byId('convert-form').addEventListener('submit', event => {
  event.preventDefault(); submit(event.currentTarget, '/convert', 'convert-result', () => Object.fromEntries(['states','alphabet','initial','accepting','transitions'].map(key => [key, parse(`nfa-${key}`)])), (container, result) => {
    container.append(node('p', `DFA states: ${JSON.stringify(result.dfaStates)}`, 'detail'), node('p', `Initial state: ${result.initialState}`, 'detail'), node('p', `Accepting states: ${JSON.stringify(result.acceptingStates)}`, 'detail'));
    const wrapper = node('div', undefined, 'table-scroll'), table = node('table'), head = node('thead'), row = node('tr'); ['From','Symbol','To'].forEach(value => row.append(node('th', value))); head.append(row); table.append(head);
    const body = node('tbody'); result.transitions.forEach(transition => { const tr = node('tr'); ['from','symbol','to'].forEach(key => tr.append(node('td', transition[key]))); body.append(tr); }); table.append(body); wrapper.append(table); container.append(wrapper);
    const button = node('button', 'Use in Simulation', 'secondary'); button.type = 'button'; button.addEventListener('click', () => { byId('sim-dfa').value = JSON.stringify(result, null, 2); resultBody('sim-result').replaceChildren(node('p', 'Converted DFA loaded. Enter a string and simulate.', 'empty')); showTab('simulate'); }); container.append(button);
  });
});
byId('simulate-form').addEventListener('submit', event => {
  event.preventDefault(); submit(event.currentTarget, '/simulate', 'sim-result', () => ({dfa: parse('sim-dfa'), input: byId('sim-input').value}), (container, result) => {
    container.append(node('div', result.accepted ? 'Accepted' : 'Rejected', `status ${result.accepted ? 'accepted' : 'rejected'}`), node('p', `accepted: ${result.accepted}`, 'detail'), node('h4', 'Traversal path'), node('p', result.path.join(' → '), 'path'));
  });
});
loadNfa(); buildTable(); byId('sim-dfa').value = JSON.stringify(official, null, 2);
