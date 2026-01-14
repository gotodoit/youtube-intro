import { useEffect, useState } from 'react';
import { Loader2, FileText, Youtube, BookOpen, Clock, Download } from 'lucide-react';

interface SummaryResult {
  status: string;
  video_info: {
    title: string;
    channel: string;
    duration: number;
    thumbnail: string;
  };
  summary: {
    full_summary: string;
    key_points: Array<{ title: string; content: string }>;
    chapters: Array<{ title: string; summary: string; timestamp: string }>;
    terminology: Record<string, string>;
  };
}

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<string>('Checking...');
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SummaryResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/health')
      .then(res => res.json())
      .then(data => setBackendStatus(`Connected: ${data.status} (v${data.version})`))
      .catch(err => setBackendStatus('Backend Disconnected (Check console)'));
  }, []);

  const handleAnalyze = async () => {
    if (!url) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch('/api/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      const data = await res.json();
      
      if (data.status === 'success') {
        setResult(data);
      } else {
        setError(data.message || 'Analysis failed');
      }
    } catch (err) {
      setError('Network error or backend unavailable');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!result) return;

    const { video_info, summary } = result;
    const date = new Date().toLocaleDateString();
    
    let mdContent = `# ${video_info.title}\n\n`;
    // Metadata block
    mdContent += `> **Channel:** ${video_info.channel} | **Duration:** ${Math.floor(video_info.duration / 60)} mins | **Date:** ${date}\n\n`;
    
    // Thumbnail with link to video
    mdContent += `[![Thumbnail](${video_info.thumbnail})](${url})\n\n`;
    
    mdContent += `## 📝 Executive Summary\n${summary.full_summary}\n\n`;
    
    mdContent += `## 🔑 Key Points\n`;
    summary.key_points.forEach(point => {
      mdContent += `- **${point.title}**: ${point.content}\n`;
    });
    mdContent += `\n`;

    if (summary.chapters && summary.chapters.length > 0) {
      mdContent += `## 📑 Chapters\n`;
      summary.chapters.forEach(chapter => {
        // Only show timestamp if it's valid and not just 00:00 (unless it's the first one)
        const showTimestamp = chapter.timestamp && chapter.timestamp !== '00:00';
        const timestampStr = showTimestamp ? `**${chapter.timestamp}** - ` : '';
        mdContent += `- ${timestampStr}**${chapter.title}**: ${chapter.summary}\n`;
      });
      mdContent += `\n`;
    }

    if (summary.terminology && Object.keys(summary.terminology).length > 0) {
      mdContent += `## 📖 Terminology\n`;
      Object.entries(summary.terminology).forEach(([term, def]) => {
        mdContent += `- **${term}**: ${def}\n`;
      });
    }

    const blob = new Blob([mdContent], { type: 'text/markdown' });
    const downloadUrl = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    // Optimize filename: "Video Title.md" -> "Video_Title.md", keep Chinese characters, remove special chars
    const safeTitle = video_info.title
      .replace(/[\\/:*?"<>|]/g, '') // Remove invalid filesystem characters
      .replace(/\s+/g, '_');         // Replace spaces with underscores
    
    a.download = `${safeTitle}_summary.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(downloadUrl);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-8">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-10">
           <h1 className="text-4xl font-bold mb-2 text-indigo-600 flex items-center justify-center gap-3">
             <Youtube className="w-10 h-10" /> YouTube AI Summary
           </h1>
           <p className="text-gray-600">Get concise summaries of long YouTube videos in seconds.</p>
        </div>
      
        <div className="bg-white p-8 rounded-xl shadow-lg mb-8">
          <label className="block text-sm font-medium text-gray-700 mb-2">Video URL</label>
          <div className="flex gap-2">
            <input 
              type="text" 
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://youtube.com/watch?v=..." 
              className="flex-1 border border-gray-300 p-3 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none transition"
            />
            <button 
              onClick={handleAnalyze}
              disabled={loading || !url}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? <Loader2 className="animate-spin w-5 h-5" /> : 'Analyze'}
            </button>
          </div>
          {error && <div className="mt-4 p-3 bg-red-50 text-red-600 rounded-lg text-sm">{error}</div>}
        </div>

        {result && (
          <div className="space-y-6 animate-fade-in">
            {/* Actions Bar */}
            <div className="flex justify-end">
              <button 
                onClick={handleDownload}
                className="flex items-center gap-2 bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 hover:text-indigo-600 transition shadow-sm"
              >
                <Download className="w-4 h-4" /> Download Markdown
              </button>
            </div>

            {/* Video Info Card */}
            <div className="bg-white p-6 rounded-xl shadow-md flex gap-6 items-start">
              <img src={result.video_info.thumbnail} alt="Thumbnail" className="w-48 rounded-lg shadow-sm" />
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-2">{result.video_info.title}</h2>
                <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                  <span className="flex items-center gap-1"><Youtube className="w-4 h-4" /> {result.video_info.channel}</span>
                  <span className="flex items-center gap-1"><Clock className="w-4 h-4" /> {Math.floor(result.video_info.duration / 60)} mins</span>
                </div>
              </div>
            </div>

            {/* Summary Content */}
            <div className="bg-white p-8 rounded-xl shadow-md">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5 text-indigo-600" /> Executive Summary
              </h3>
              <p className="text-gray-700 leading-relaxed mb-8">{result.summary.full_summary}</p>

              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-indigo-600" /> Key Points
              </h3>
              <div className="grid md:grid-cols-2 gap-4">
                {result.summary.key_points.map((point, idx) => (
                  <div key={idx} className="p-4 bg-indigo-50 rounded-lg border border-indigo-100">
                    <h4 className="font-semibold text-indigo-900 mb-2">{point.title}</h4>
                    <p className="text-sm text-indigo-800">{point.content}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="mt-12 text-center text-sm text-gray-400">
          Backend Status: <span className={`font-mono ${backendStatus.includes('Connected') ? 'text-green-600' : 'text-red-500'}`}>{backendStatus}</span>
        </div>
      </div>
    </div>
  );
}
