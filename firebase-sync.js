// Amara Reading — cloud sync (Firestore). Shared by all four pages.
// You should not need to edit this file; edit config.js instead.
import { initializeApp } from 'https://www.gstatic.com/firebasejs/12.15.0/firebase-app.js';
import { getFirestore, doc, getDoc, setDoc } from 'https://www.gstatic.com/firebasejs/12.15.0/firebase-firestore-lite.js';
import { firebaseConfig, READER_ID } from './config.js';

const SCORES = 'amaraReading';
const WRITING = 'amaraWriting';

let db = null, ready = false;
try {
  if (firebaseConfig.apiKey && firebaseConfig.apiKey.indexOf('PASTE') !== 0) {
    db = getFirestore(initializeApp(firebaseConfig));
    ready = true;
  } else {
    console.info('Amara Reading: no Firebase config yet — saving on this device only.');
  }
} catch (e) {
  console.warn('Amara Reading: Firebase failed to start, using this device only.', e);
}

const lj = (k) => { try { return JSON.parse(localStorage.getItem(k) || '{}'); } catch (e) { return {}; } };
const sj = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };

function mergeScores(a, b) {
  const o = Object.assign({}, a);
  for (const k in b) {
    const x = o[k] || {}, y = b[k] || {};
    o[k] = {
      best: Math.max(x.best || 0, y.best || 0),
      total: y.total || x.total,
      attempts: Math.max(x.attempts || 0, y.attempts || 0),
      last: (y.last != null ? y.last : x.last),
      date: y.date || x.date
    };
  }
  return o;
}
function newerWriting(a, b) {
  if (!a || !a.date) return b || {};
  if (!b || !b.date) return a || {};
  return (new Date(b.date) > new Date(a.date)) ? b : a;
}
async function getCloud() {
  const snap = await getDoc(doc(db, 'readers', READER_ID));
  return snap.exists() ? snap.data() : {};
}

async function pull() {
  if (!ready) return;
  try {
    const c = await getCloud();
    sj(SCORES, mergeScores(lj(SCORES), c.scores || {}));
    sj(WRITING, newerWriting(lj(WRITING), c.writing || {}));
    window.dispatchEvent(new Event('amara-scores-updated'));
    window.dispatchEvent(new Event('amara-writing-updated'));
  } catch (e) { console.warn('Amara Reading: pull failed', e); }
}
async function push() {
  if (!ready) return;
  try {
    const c = await getCloud();
    const scores = mergeScores(c.scores || {}, lj(SCORES));
    const writing = newerWriting(c.writing || {}, lj(WRITING));
    sj(SCORES, scores); sj(WRITING, writing);
    await setDoc(doc(db, 'readers', READER_ID),
      { scores, writing, updated: new Date().toISOString() }, { merge: true });
  } catch (e) { console.warn('Amara Reading: push failed', e); }
}

async function reset() {
  try { localStorage.removeItem(SCORES); } catch (e) {}
  if (!ready) return;
  try {
    const c = await getCloud();
    await setDoc(doc(db, 'readers', READER_ID),
      { scores: {}, writing: c.writing || {}, updated: new Date().toISOString() });
  } catch (e) { console.warn('Amara Reading: reset failed', e); }
}

window.amaraCloud = { pull, push, reset, ready: () => ready };
pull();
