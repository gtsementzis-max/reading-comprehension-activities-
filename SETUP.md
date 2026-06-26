# Amara Reading — setup guide

You have 6 files in this folder:

- `index.html` — the home page (start here)
- `amara-marine-life-reading.html` — marine life project
- `amara-bees-reading.html` — bees project
- `amara-write-a-summary.html` — writing project
- `config.js` — **the only file you edit**
- `firebase-sync.js` — the cloud-sync code (leave it alone)

Keep all six in the SAME folder. The pages link to each other and share scores
only when they sit together at one web address.

---

## Part 1 — Put it online (about 5 minutes)

1. Go to https://app.netlify.com/drop
2. Drag this whole folder onto the drop zone.
3. You get a live link ending in `.netlify.app`. That link opens `index.html`.
4. IMPORTANT: anonymous sites are deleted after ~24 hours. Sign up for a free
   Netlify account and claim the site so it stays. You can rename the URL too.
5. To update later (new topics, fixes): drag the updated folder onto the same site.

If you host on your own site instead (e.g. S3 + CloudFront), upload all six files
into one folder there and point Amara to `index.html`.

Scores will save on the device even before you do Part 2 — Part 2 is only what makes
them follow her across devices.

---

## Part 2 — Turn on cross-device scores with Firebase (about 10 minutes)

### A. Create the database
1. Go to https://console.firebase.google.com and open your project.
2. In the left menu: Build → Firestore Database → Create database.
3. Choose a location (any nearby region) and "Production mode". Finish.

### B. Set the security rules
1. Still in Firestore Database, open the "Rules" tab.
2. Replace whatever is there with exactly this, then click Publish:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /readers/{readerId} {
      allow read, write: if true;
    }
  }
}
```

### C. Get your web config
1. Click the gear icon (top left) → Project settings.
2. Scroll to "Your apps". If there's no web app, click the web icon `</>` and
   register one (any nickname; you do NOT need Firebase Hosting).
3. Under "SDK setup and configuration" choose "Config". You'll see an object
   that looks like:

```
const firebaseConfig = {
  apiKey: "AIza................",
  authDomain: "yourproject.firebaseapp.com",
  projectId: "yourproject",
  storageBucket: "yourproject.firebasestorage.app",
  messagingSenderId: "000000000000",
  appId: "1:0000:web:abc123"
};
```

### D. Edit config.js
1. Open `config.js` in any text editor.
2. Replace the placeholder `firebaseConfig` with the one you just copied.
3. Set `READER_ID` to a private word only you know (e.g. "amara-bluefox-42").
   Use the SAME word everywhere — you only set it once here.
4. Save the file.

### E. Re-upload
Drag the folder onto your Netlify site again (or re-upload to your own host) so
the updated `config.js` goes live.

---

## Test it (do this before handing it to Amara)

1. Open the site on Device 1. Finish one activity (e.g. the bees match).
2. Open the SAME link on Device 2 (or a different browser).
3. On Device 2, the home page should show that score within a few seconds.

If it doesn't: open the page, press F12 (or right-click → Inspect) → Console tab,
and look for a red "Amara Reading: ..." message. Tell me what it says and I'll fix it.

---

## A note on privacy (please read)

This simple setup has no login. Anyone who had both your site address AND guessed
your secret `READER_ID` could read or change Amara's scores. The data is only quiz
scores and a practice summary — nothing sensitive — so for a family this is usually
fine, and the secret word keeps it private in practice. But it is "hard to guess",
not "locked". If you want real privacy (a proper family login with a password),
ask and I'll build that version instead.

## Resetting scores
The "Reset all progress" button on the home page clears scores on every device.
"Best" scores only ever go up otherwise — that's on purpose, so a retry never lowers
a previous best.
