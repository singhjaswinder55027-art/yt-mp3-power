# File: app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

# Initialize the Flask app
app = Flask(__name__)
# Allow requests from your frontend
CORS(app)

# Create an API endpoint at /api/getVideoInfo
@app.route('/api/getVideoInfo', methods=['POST'])
def get_video_info():
    """
    Takes a YouTube URL, fetches video info using yt-dlp, and returns it.
    """
    url = request.json.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # yt-dlp options to get the best quality mp4
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best[ext=mp4]/best', 
        }

        # Extract info without downloading
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)

            # Get the best audio-only format for MP3
            audio_formats = [f for f in info_dict.get('formats', []) if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
            best_audio = sorted(audio_formats, key=lambda x: x.get('abr', 0), reverse=True)[0] if audio_formats else None

            video_info = {
                "title": info_dict.get('title', 'No Title'),
                "thumbnail": info_dict.get('thumbnail', ''),
                "download_url_mp4": info_dict.get('url', ''),
                "download_url_mp3": best_audio.get('url') if best_audio else info_dict.get('url', ''),
            }

            return jsonify(video_info)

    except Exception as e:
        return jsonify({"error": "Could not process the video. Please check the URL."}), 500

# To run this, use the command: flask --app app run --port=5001
if __name__ == '__main__':
    app.run(debug=True, port=5001)
red.');
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
