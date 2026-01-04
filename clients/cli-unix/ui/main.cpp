#include <iostream>
#include <thread>
#include <chrono>
#include <cstdlib>

// RUST INTERFACE
// We declare the functions that exist in the Rust library
extern "C" {
    char* fetch_scoreboard_data();
    void free_scoreboard_string(char* s);
}

// Helper to clear screen using ANSI codes
void clear_screen() {
    // \033[2J = Clear screen, \033[1;1H = Move cursor top-left
    std::cout << "\033[2J\033[1;1H";
}

int main() {
    std::cout << "Initializing Hybrid Client..." << std::endl;

    while (true) {
        // 1. Call Rust to get the data
        char* data = fetch_scoreboard_data();

        // 2. Clear Screen and Print
        clear_screen();
        if (data != nullptr) {
            std::cout << data << std::endl;
            
            // 3. IMPORTANT: Tell Rust to free the memory
            // If we don't do this, we get a memory leak!
            free_scoreboard_string(data);
        }

        // 4. Wait 2 seconds
        std::this_thread::sleep_for(std::chrono::seconds(2));
    }

    return 0;
}
