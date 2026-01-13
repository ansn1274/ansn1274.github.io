import React, { useState, useEffect } from 'react';
import PlayerSearch from './components/PlayerSearch';
import ShotChart from './components/ShotChart';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar } from 'recharts';
import { User, TrendingUp, Target, Award, Loader2 } from 'lucide-react';

function App() {
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [playerData, setPlayerData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedPlayer) {
      fetchPlayerData(selectedPlayer.id);
    }
  }, [selectedPlayer]);

  const fetchPlayerData = async (id) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/player_stats?player_id=${id}`);
      const data = await response.json();
      setPlayerData(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const currentStats = playerData?.stats?.length > 0 ? playerData.stats[playerData.stats.length - 1] : {};
  const statsForChart = (playerData?.stats || []).slice(-5);

  return (
    <div className="min-h-screen w-full p-4 md:p-8 flex flex-col items-center">
      <header className="w-full max-w-7xl flex flex-col md:flex-row justify-between items-center gap-6 mb-12">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-primary rounded-2xl shadow-lg glow">
            <Target className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight">NBA INSIGHTS</h1>
        </div>
        <PlayerSearch onSelectPlayer={setSelectedPlayer} />
      </header>

      {loading ? (
        <div className="flex-1 flex flex-col items-center justify-center gap-4">
          <Loader2 className="w-12 h-12 text-primary animate-spin" />
          <p className="text-white/40 animate-pulse">Fetching latest player data...</p>
        </div>
      ) : selectedPlayer && playerData ? (
        <main className="w-full max-w-7xl grid grid-cols-1 lg:grid-cols-3 gap-8 animate-fade-in">
          {/* Sidebar: Profile & Stats */}
          <div className="flex flex-col gap-8">
            <div className="glass-card p-8 flex flex-col items-center text-center">
              <div className="w-32 h-32 bg-white/5 rounded-full flex items-center justify-center mb-6 border border-white/10">
                <User className="w-16 h-16 text-white/20" />
              </div>
              <h2 className="text-3xl font-bold mb-1">{selectedPlayer.full_name}</h2>
              <p className="text-white/40 mb-6">{currentStats.TEAM_ABBREVIATION || 'N/A'} | {currentStats.SEASON_ID || 'Season Unknown'}</p>

              <div className="w-full grid grid-cols-3 gap-4 border-t border-white/5 pt-8">
                <div>
                  <div className="text-white/40 text-xs mb-1 uppercase tracking-wider">PTS</div>
                  <div className="text-2xl font-bold text-primary">{currentStats.PTS || 0}</div>
                </div>
                <div>
                  <div className="text-white/40 text-xs mb-1 uppercase tracking-wider">AST</div>
                  <div className="text-2xl font-bold text-accent">{currentStats.AST || 0}</div>
                </div>
                <div>
                  <div className="text-white/40 text-xs mb-1 uppercase tracking-wider">REB</div>
                  <div className="text-2xl font-bold text-white">{currentStats.REB || 0}</div>
                </div>
              </div>
            </div>

            <div className="glass-card p-6">
              <div className="flex items-center gap-3 mb-6">
                <TrendingUp className="text-primary w-5 h-5" />
                <h3 className="font-bold opacity-60">CAREER GROWTH</h3>
              </div>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={playerData.stats}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="SEASON_ID" hide />
                    <Tooltip
                      contentStyle={{ background: '#111', border: '1px solid #333', borderRadius: '8px' }}
                      itemStyle={{ color: '#3b82f6' }}
                    />
                    <Line type="monotone" dataKey="PTS" stroke="#3b82f6" strokeWidth={3} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Main: Shot Chart & Advanced */}
          <div className="lg:col-span-2 flex flex-col gap-8">
            <ShotChart shots={playerData.shots} />

            <div className="glass-card p-8">
              <div className="flex items-center gap-3 mb-8">
                <Award className="text-accent w-5 h-5" />
                <h3 className="font-bold opacity-60">SEASON PERFORMANCE</h3>
              </div>
              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={statsForChart}>
                    <XAxis dataKey="SEASON_ID" stroke="rgba(255,255,255,0.3)" fontSize={12} />
                    <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} />
                    <Tooltip
                      contentStyle={{ background: '#111', border: '1px solid #333', borderRadius: '8px' }}
                    />
                    <Bar dataKey="PTS" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="REB" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="AST" fill="#fff" radius={[4, 4, 0, 0]} opacity={0.5} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </main>
      ) : (
        <div className="flex-1 flex flex-col items-center justify-center max-w-2xl text-center">
          <div className="w-24 h-24 glass-card flex items-center justify-center mb-8 glow">
            <Target className="w-12 h-12 text-primary" />
          </div>
          <h2 className="text-4xl font-bold mb-4">Discover Player Insights</h2>
          <p className="text-xl text-white/40 leading-relaxed">
            Search for any NBA player above to analyze their shooting habits, career progression, and season performance in real-time.
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
