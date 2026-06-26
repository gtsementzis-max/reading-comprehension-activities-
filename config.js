// =====================================================================
//  AMARA READING — SETTINGS  (this is the ONLY file you need to edit)
// =====================================================================
//
//  STEP 1 — Paste your Firebase web config below.
//  Find it in: Firebase console -> Project settings (gear icon) ->
//  "Your apps" -> your Web app -> "SDK setup and configuration" ->
//  choose "Config". Copy the whole object and replace the one below.
//
export const firebaseConfig = {
  apiKey:            "PASTE_YOUR_API_KEY_HERE",
  authDomain:        "PASTE_YOUR_PROJECT.firebaseapp.com",
  projectId:         "PASTE_YOUR_PROJECT_ID",
  storageBucket:     "PASTE_YOUR_PROJECT.firebasestorage.app",
  messagingSenderId: "PASTE_YOUR_SENDER_ID",
  appId:             "PASTE_YOUR_APP_ID"
};

//  STEP 2 — Pick a private word for Amara's records.
//  It can be anything, but make it hard for a stranger to guess.
//  Use the SAME word on every device she uses.
//
export const READER_ID = "amara-pick-a-secret-word";
