import { useState, useEffect, useCallback } from 'react';
import Hero from './components/home/Hero';
import Timeline from './components/home/Timeline';
import ChapterGrid from './components/home/ChapterGrid';
import FiguresGallery from './components/home/FiguresGallery';
import Navbar from './components/common/Navbar';
import Footer from './components/common/Footer';
import GiscusComments from './components/common/GiscusComments';
import useTheme from './hooks/useTheme';
import useReadingProgress from './hooks/useReadingProgress';

function getInitialLang() {
  // 1. URL param takes priority
  const params = new URLSearchParams(window.location.search);
  const urlLang = params.get('lang');
  if (urlLang === 'en' || urlLang === 'zh') return urlLang;

  // 2. localStorage
  const stored = localStorage.getItem('lang');
  if (stored === 'en' || stored === 'zh') return stored;

  // 3. Browser language detection
  const browserLang = navigator.language || navigator.userLanguage || '';
  if (browserLang.startsWith('zh')) return 'zh';
  if (browserLang.startsWith('en')) return 'en';

  return 'zh';
}

function App() {
  const [lang, setLangState] = useState(getInitialLang);
  const { theme, toggleTheme } = useTheme();
  const { markAsRead, isRead, readCount } = useReadingProgress();

  const setLang = useCallback((newLang) => {
    setLangState(newLang);
    localStorage.setItem('lang', newLang);

    // Update URL param without reload
    const url = new URL(window.location);
    url.searchParams.set('lang', newLang);
    window.history.replaceState({}, '', url);
  }, []);

  // Sync if URL changes externally (e.g. back/forward)
  useEffect(() => {
    const handlePopState = () => {
      const params = new URLSearchParams(window.location.search);
      const urlLang = params.get('lang');
      if (urlLang === 'en' || urlLang === 'zh') {
        setLangState(urlLang);
      }
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  return (
    <div className="min-h-screen">
      {/* Skip to content link for keyboard users */}
      <a href="#main-content" className="skip-link">
        {lang === 'zh' ? '跳转到主要内容' : 'Skip to main content'}
      </a>

      {/* Navigation */}
      <Navbar lang={lang} setLang={setLang} theme={theme} toggleTheme={toggleTheme} />

      <main id="main-content">
      {/* Hero Section */}
      <section id="hero">
        <Hero lang={lang} />
      </section>

      {/* Timeline Section */}
      <section id="timeline">
        <Timeline lang={lang} />
      </section>

      {/* Key Figures Gallery */}
      <section id="figures">
        <FiguresGallery lang={lang} />
      </section>

      {/* Chapters Grid */}
      <section id="chapters">
        <ChapterGrid lang={lang} markAsRead={markAsRead} isRead={isRead} readCount={readCount} />
      </section>

      {/* Discussion Section */}
      <GiscusComments lang={lang} theme={theme} />
      </main>

      {/* Footer */}
      <Footer lang={lang} />
    </div>
  );
}

export default App;
