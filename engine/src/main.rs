use axum::{
    extract::{State, Json},
    http::StatusCode,
    routing::{get, post},
    Router,
};
use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tracing::info;

// Data Structures

#[derive(Clone, Serialize, Deserialize, Debug)]
struct SubmitFlagRequest {
    team_name: String,
    flag: String,
}

#[derive(Serialize, Debug)]
struct ScoreEntry {
    team_name: String,
    score: u32,
    last_submit: String, // ISO timestamp
}

// The Game State
// Use DashMap for high-concurrency read/write without manual Mutex locking
struct GameState {
    // Map<FlagString, Points>
    challenges: DashMap<String, u32>,
    // Map<TeamName, Score>
    scores: DashMap<String, u32>,
}

// Logic

#[tokio::main]
async fn main() {
    // Initialize logging
    tracing_subscriber::fmt::init();

    info!("Initializing CyberArena Core...");

    // Setup initial state
    let state = Arc::new(GameState {
        challenges: DashMap::new(),
        scores: DashMap::new(),
    });

    // REGISTER FLAGS HERE
    // 1. Basic Flag
    state.challenges.insert("CTF{welcome_to_rust}".to_string(), 100);
    // 2. Binary Exploitation Flag (Phase 2)
    state.challenges.insert("CTF{buffer_overflow_ez}".to_string(), 300);
    // 3. Web/SQL Injection Flag (Phase 3)
    state.challenges.insert("CTF{sql_injection_master}".to_string(), 500);
    // 4. Crypto Challenges (Phase 4)
    state.challenges.insert("CTF{crypto_god_sha256}".to_string(), 800);

    // Initialize Teams
    state.scores.insert("RedTeam".to_string(), 0);
    state.scores.insert("BlueTeam".to_string(), 0);

    // Define Routes
    let app = Router::new()
        .route("/submit", post(submit_flag))
        .route("/scoreboard", get(get_scoreboard))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    info!("CyberArena Server listening on port 3000");
    axum::serve(listener, app).await.unwrap();
}

// Handler: Flag Submission
async fn submit_flag(
    State(state): State<Arc<GameState>>,
    Json(payload): Json<SubmitFlagRequest>,
) -> (StatusCode, String) {
    
    // 1. Check if flag exists in our challenges list
    if let Some(points) = state.challenges.get(&payload.flag) {
        // 2. Update Team Score
        if let Some(mut score) = state.scores.get_mut(&payload.team_name) {
            *score += *points;
            info!("Team {} scored {} points!", payload.team_name, *points);
            return (StatusCode::OK, format!("Correct! +{} points", *points));
        } else {
            // Register team on fly (Jeopardy style)
            state.scores.insert(payload.team_name.clone(), *points);
            return (StatusCode::OK, format!("Correct! Team Registered. +{} points", *points));
        }
    }

    info!("Team {} failed flag submission", payload.team_name);
    (StatusCode::BAD_REQUEST, "Invalid Flag".to_string())
}

// Handler: Scoreboard
async fn get_scoreboard(State(state): State<Arc<GameState>>) -> Json<Vec<ScoreEntry>> {
    let mut leaderboard: Vec<ScoreEntry> = state.scores
        .iter()
        .map(|entry| ScoreEntry {
            team_name: entry.key().clone(),
            score: *entry.value(),
            last_submit: chrono::Local::now().to_rfc3339(),
        })
        .collect();

    // Sort by score descending (Highest first)
    leaderboard.sort_by(|a, b| b.score.cmp(&a.score));
    
    Json(leaderboard)
}
