import { useState, useEffect, useCallback, lazy, Suspense } from 'react';
import { Helmet } from 'react-helmet-async';
import Hero from './components/home/Hero';
import Navbar from './components/common/Navbar';
import Footer from './components/common/Footer';
import BackToTop from './components/common/BackToTop';
import AchievementToast from './components/common/AchievementToast';
import ErrorBoundary from './components/common/ErrorBoundary';
import useTheme from './hooks/useTheme';
import useReadingProgress from './hooks/useReadingProgress';
import useAchievements from './hooks/useAchievements';
import useBookmarks from './hooks/useBookmarks';

const Timeline = lazy(() => import('./components/home/Timeline'));
const FiguresGallery = lazy(() => import('./components/home/FiguresGallery'));
const ChapterGrid = lazy(() => import('./components/home/ChapterGrid'));
const GiscusComments = lazy(() => import('./components/common/GiscusComments'));

const LoadingSpinner = () => (
  <div className="flex justify-center items-center py-20">
    <div className="w-10 h-10 border-4 border-bitcoin-orange border-t-transparent rounded-full animate-spin" />
  </div>
);

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
  const { readChapters, markAsRead, isRead, readCount } = useReadingProgress();
  const { unlockedCount, totalCount, newAchievement, dismissAchievement, isPeriodComplete, onChapterRead } = useAchievements(readChapters);
  const { toggleBookmark, isBookmarked } = useBookmarks();

  const handleMarkAsRead = useCallback((chapterId) => {
    markAsRead(chapterId);
    onChapterRead();
  }, [markAsRead, onChapterRead]);

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
      {/* Dynamic meta tags — override static index.html values based on language */}
      <Helmet>
        <html lang={lang === 'zh' ? 'zh-CN' : 'en'} />
        <title>
          {lang === 'zh'
            ? '比特币那些事儿 — 用文学风格讲述比特币历史'
            : 'Stories about Bitcoin — Bitcoin History in Literary Style'}
        </title>
        <meta property="og:title" content={lang === 'zh'
          ? '比特币那些事儿 — 用文学风格讲述比特币历史'
          : 'Stories about Bitcoin — Bitcoin History in Literary Style'} />
        <meta property="og:description" content={lang === 'zh'
          ? '36章开源双语电子书，覆盖1976-2025年比特币历史'
          : '36-chapter open-source bilingual ebook covering Bitcoin history from 1976 to 2025'} />
        <meta property="og:locale" content={lang === 'zh' ? 'zh_CN' : 'en_US'} />
        <meta name="twitter:title" content={lang === 'zh'
          ? '比特币那些事儿 — 用文学风格讲述比特币历史'
          : 'Stories about Bitcoin — Bitcoin History in Literary Style'} />
        <meta name="twitter:description" content={lang === 'zh'
          ? '36章开源双语电子书，覆盖1976-2025年比特币历史'
          : '36-chapter open-source bilingual ebook covering Bitcoin history from 1976 to 2025'} />
      </Helmet>

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
        <Suspense fallback={<LoadingSpinner />}>
          <Timeline lang={lang} />
        </Suspense>
      </section>

      {/* Key Figures Gallery */}
      <section id="figures">
        <Suspense fallback={<LoadingSpinner />}>
          <FiguresGallery lang={lang} />
        </Suspense>
      </section>

      {/* Chapters Grid */}
      <section id="chapters">
        <Suspense fallback={<LoadingSpinner />}>
          <ChapterGrid
            lang={lang}
            markAsRead={handleMarkAsRead}
            isRead={isRead}
            readCount={readCount}
            unlockedCount={unlockedCount}
            totalAchievements={totalCount}
            isPeriodComplete={isPeriodComplete}
            isBookmarked={isBookmarked}
            toggleBookmark={toggleBookmark}
          />
        </Suspense>
      </section>

      {/* Discussion Section */}
      <ErrorBoundary lang={lang}>
        <Suspense fallback={<LoadingSpinner />}>
          <GiscusComments lang={lang} theme={theme} />
        </Suspense>
      </ErrorBoundary>
      </main>

      {/* Footer */}
      <Footer lang={lang} />

      {/* Back to Top */}
      <BackToTop lang={lang} />

      {/* Achievement Toast */}
      <AchievementToast
        achievement={newAchievement}
        lang={lang}
        onDismiss={dismissAchievement}
      />
    </div>
  );
}

export default App;
