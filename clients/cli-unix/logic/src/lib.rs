use libc::c_char;
use serde::Deserialize;
use std::ffi::CString;

#[derive(Deserialize)]
struct ScoreEntry {
    team_name: String,
    score: u32,
    
    // FIX: We keep the name 'last_submit' to match the JSON from the server.
    // We add this attribute to stop the compiler from complaining it's unused.
    #[allow(dead_code)] 
    last_submit: String, 
}

#[no_mangle]
pub extern "C" fn fetch_scoreboard_data() -> *mut c_char {
    let url = "http://localhost:3000/scoreboard";
    
    // 1. HTTP Request
    let response_text = match ureq::get(url).call() {
        Ok(resp) => resp.into_string().unwrap_or_default(),
        Err(_) => return CString::new("\x1b[31m[!] SERVER OFFLINE\x1b[0m").unwrap().into_raw(),
    };

    // 2. Parse JSON
    // This was failing because of the field name mismatch
    let entries: Vec<ScoreEntry> = match serde_json::from_str(&response_text) {
        Ok(e) => e,
        Err(_) => return CString::new("\x1b[33m[!] DATA ERROR: JSON Mismatch\x1b[0m").unwrap().into_raw(),
    };

    // 3. Build String
    let mut output = String::new();
    // Clear screen code (ANSI) included at start of string
    output.push_str("\x1b[2J\x1b[1;1H"); 
    output.push_str("\x1b[1;32m=== CYBER_ARENA // UNIX_TERMINAL ===\x1b[0m\n\n");
    output.push_str(format!("{:<5} | {:<20} | {:<10}\n", "RANK", "OPERATOR", "SCORE").as_str());
    output.push_str("------------------------------------------\n");

    for (i, entry) in entries.iter().enumerate() {
        let rank = i + 1;
        let color = if rank == 1 { "\x1b[33m" } else { "\x1b[36m" };
        output.push_str(format!("{}{}     | {:<20} | {:<10}\x1b[0m\n", color, rank, entry.team_name, entry.score).as_str());
    }
    
    output.push_str("\n\x1b[90m[Updating via Rust Bridge...]\x1b[0m");

    let c_str = CString::new(output).unwrap();
    c_str.into_raw()
}

#[no_mangle]
pub extern "C" fn free_scoreboard_string(s: *mut c_char) {
    if s.is_null() { return; }
    unsafe {
        let _ = CString::from_raw(s);
    }
}
