// File: app/app.py
'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// A simple spinner component
const Spinner = () => (
  <svg className="animate-spin h-5 w-5 text-cyan" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>
);

// Main Page Component
export default function Home() {
  const [url, setUrl] = useState('');
  const [format, setFormat] = useState<'mp3' | 'mp4'>('mp3');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [videoInfo, setVideoInfo] = useState<any | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) {
      setError('Please enter a valid YouTube URL.');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setVideoInfo(null);

    try {
      const response = await fetch('https://co.wuk.sh/api/json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          url: url,
          isNoTT: true, // No Text-to-Speech watermark
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch video information. Please check the URL.');
      }

      const data = await response.json();
      
      if (data.status === 'error') {
        throw new Error(data.text || 'An unknown error occurred.');
      }

      setVideoInfo(data);

    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleFormat = () => {
    setFormat(current => (current === 'mp3' ? 'mp4' : 'mp3'));
  };
  
  const downloadUrl = videoInfo?.url;

  return (
    <div className="flex flex-col min-h-screen items-center justify-between p-4 md:p-8">
      {/* HEADER */}
      <header className="w-full max-w-4xl text-center">
        <motion.h1 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-4xl md:text-5xl font-bold text-cyan"
        >
          Mp3-Mate
        </motion.h1>
        <motion.p 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-light-slate mt-2"
        >
          A DEVIL LOOTS Project
        </motion.p>
      </header>

      {/* MAIN CONTENT */}
      <main className="w-full max-w-2xl flex-grow flex flex-col items-center justify-center">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="w-full bg-light-navy p-6 md:p-8 rounded-lg shadow-2xl"
        >
          <h2 className="text-2xl font-semibold text-lightest-slate mb-4">YouTube to {format.toUpperCase()} Converter</h2>
          <p className="text-slate mb-6">Paste your YouTube video link below to convert and download it for free.</p>
          
          <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row items-center gap-2">
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="youtube.com/watch?v=..."
              className="w-full px-4 py-3 bg-navy border-2 border-lightest-navy rounded-md focus:outline-none focus:border-cyan text-lightest-slate transition-colors duration-300"
            />
            <div className="flex gap-2 w-full sm:w-auto">
              <button 
                type="button" 
                onClick={toggleFormat}
                className="px-5 py-3 bg-lightest-navy text-cyan font-bold rounded-md hover:bg-slate transition-colors duration-300 w-1/2 sm:w-auto"
              >
                {format.toUpperCase()}
              </button>
              <button 
                type="submit" 
                disabled={isLoading}
                className="px-5 py-3 bg-cyan text-navy font-bold rounded-md hover:bg-opacity-80 transition-colors duration-300 flex items-center justify-center gap-2 w-1/2 sm:w-auto"
              >
                {isLoading ? <Spinner /> : 'Convert'}
              </button>
            </div>
          </form>
        </motion.div>
        
        {/* DYNAMIC CONTENT AREA */}
        <div className="w-full mt-8">
          <AnimatePresence>
            {error && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="bg-red-500/20 text-red-300 p-4 rounded-md text-center"
              >
                {error}
              </motion.div>
            )}

            {videoInfo && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4 }}
                className="bg-light-navy p-6 rounded-lg shadow-2xl flex flex-col md:flex-row items-center gap-6"
              >
                <img 
                  src={videoInfo.picker?.[0]?.thumb || videoInfo.thumb} 
                  alt="Video Thumbnail" 
                  className="w-full md:w-48 h-auto rounded-md object-cover"
                />
                <div className="flex flex-col items-center md:items-start text-center md:text-left">
                  <h3 className="text-xl font-bold text-lightest-slate">{videoInfo.title}</h3>
                  <p className="text-slate mt-2">Ready to download in your selected format!</p>
                  <a 
                    href={downloadUrl}
                    download
                    className="mt-4 px-6 py-3 bg-cyan text-navy font-bold rounded-md hover:bg-opacity-80 transition-colors duration-300 inline-block"
                  >
                    Download {format.toUpperCase()}
                  </a>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      {/* FOOTER */}
      <footer className="w-full max-w-4xl text-center text-slate text-sm mt-8">
        <p>&copy; {new Date().getFullYear()} Mp3-Mate.vercel.app. All Rights Reserved.</p>
        <p className="mt-1">
          Please respect copyright laws. This tool is for personal use only.
        </p>
      </footer>
    </div>
  );
}
}
