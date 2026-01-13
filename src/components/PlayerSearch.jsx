import React, { useState, useEffect } from 'react';
import { Search, Loader2 } from 'lucide-react';

const PlayerSearch = ({ onSelectPlayer }) => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const timer = setTimeout(async () => {
            if (query.length < 3) {
                setResults([]);
                return;
            }

            setLoading(true);
            try {
                const response = await fetch(`/api/search_players?name=${encodeURIComponent(query)}`);
                const data = await response.json();
                setResults(data);
            } catch (error) {
                console.error('Search failed:', error);
            } finally {
                setLoading(false);
            }
        }, 500);

        return () => clearTimeout(timer);
    }, [query]);

    return (
        <div className="relative w-full max-w-xl mx-auto">
            <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40 w-5 h-5" />
                <input
                    type="text"
                    placeholder="Search for an NBA player (e.g. Stephen Curry)..."
                    className="w-full pl-12 pr-4 h-14 text-lg glass-card"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                {loading && (
                    <Loader2 className="absolute right-4 top-1/2 -translate-y-1/2 text-primary w-5 h-5 animate-spin" />
                )}
            </div>

            {results.length > 0 && (
                <div className="absolute top-16 left-0 right-0 glass-card p-2 z-50 overflow-hidden glow">
                    {results.map((player) => (
                        <button
                            key={player.id}
                            className="w-full text-left p-4 hover:bg-white/10 rounded-xl transition-colors flex items-center justify-between"
                            onClick={() => {
                                onSelectPlayer(player);
                                setResults([]);
                                setQuery('');
                            }}
                        >
                            <span className="font-semibold text-lg">{player.full_name}</span>
                            <span className={`text-xs px-2 py-1 rounded-full ${player.is_active ? 'bg-green-500/20 text-green-400' : 'bg-white/10 text-white/40'}`}>
                                {player.is_active ? 'ACTIVE' : 'RETIRED'}
                            </span>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default PlayerSearch;
