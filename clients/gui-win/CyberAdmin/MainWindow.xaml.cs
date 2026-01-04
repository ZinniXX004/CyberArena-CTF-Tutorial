using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Threading;

namespace CyberAdmin
{
    public class ScoreEntry
    {
        // 'string?' means this variable is ALLOWED to be null
        public string? Rank { get; set; }

        [JsonPropertyName("team_name")]
        public string? TeamName { get; set; }

        [JsonPropertyName("score")]
        public int Score { get; set; }

        [JsonPropertyName("last_submit")]
        public string? LastSubmit { get; set; }
    }

    public partial class MainWindow : Window
    {
        private readonly HttpClient _client = new HttpClient();
        private readonly DispatcherTimer _refreshTimer = new DispatcherTimer();
        private readonly DispatcherTimer _clockTimer = new DispatcherTimer();
        private const string API_URL = "http://localhost:3000/scoreboard";

        public MainWindow()
        {
            InitializeComponent();
            
            // 1. Data Refresh Timer (Fast polling)
            _refreshTimer.Interval = TimeSpan.FromSeconds(2);
            _refreshTimer.Tick += async (s, e) => await FetchData();
            _refreshTimer.Start();

            // 2. UI Clock Timer
            _clockTimer.Interval = TimeSpan.FromSeconds(1);
            _clockTimer.Tick += (s, e) => ClockText.Text = DateTime.Now.ToString("HH:mm:ss");
            _clockTimer.Start();

            _ = FetchData();
        }

        // CUSTOM WINDOW CONTROLS

        private void Window_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ChangedButton == MouseButton.Left)
                this.DragMove();
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e) => Close();

        private void MinimizeButton_Click(object sender, RoutedEventArgs e) => WindowState = WindowState.Minimized;

        // DATA LOGIC

        private async Task FetchData()
        {
            try
            {
                string json = await _client.GetStringAsync(API_URL);
                
                // Assume the API always returns a valid list, but '?' makes the compiler happy
                var rawData = JsonSerializer.Deserialize<List<ScoreEntry>>(json);
                
                // Safety check: If rawData is null, stop here
                if (rawData is null) return;

                // Process Data (Add Rankings)
                int rank = 1;
                foreach(var entry in rawData)
                {
                    entry.Rank = rank <= 3 ? $"#{rank}" : $"{rank}";
                    rank++;
                }
                
                ScoreGrid.ItemsSource = rawData;
                
                StatusText.Text = "ONLINE [SECURE]";
                StatusText.Foreground = System.Windows.Media.Brushes.LimeGreen;
            }
            catch (Exception)
            {
                StatusText.Text = "CONNECTION LOST [RETRYING...]";
                StatusText.Foreground = System.Windows.Media.Brushes.Red;
            }
        }
    }
}
