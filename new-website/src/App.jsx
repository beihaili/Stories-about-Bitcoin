import { useState } from 'react';
import Hero from './components/home/Hero';
import Timeline from './components/home/Timeline';
import ChapterGrid from './components/home/ChapterGrid';
import FiguresGallery from './components/home/FiguresGallery';
import LanguageSwitcher from './components/common/LanguageSwitcher';

function App() {
  const [lang, setLang] = useState('zh');

  return (
    <div className="min-h-screen">
      {/* Language Switcher */}
      <LanguageSwitcher lang={lang} setLang={setLang} />

      {/* Hero Section */}
      <Hero lang={lang} />

      {/* Timeline Section */}
      <Timeline lang={lang} />

      {/* Key Figures Gallery */}
      <FiguresGallery lang={lang} />

      {/* Chapters Grid */}
      <ChapterGrid lang={lang} />

      {/* Footer */}
      <footer className="bg-historical-sepia text-bitcoin-lightGold py-12">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <p className="text-2xl font-bold mb-4">
            {lang === 'zh' ? '比特币那些事儿' : 'Stories about Bitcoin'}
          </p>
          <p className="text-sm opacity-75 mb-6">
            {lang === 'zh'
              ? '以网文笔法讲比特币的故事 · 开源项目'
              : 'Bitcoin Stories in Web Novel Style · Open Source'}
          </p>
          <div className="flex justify-center gap-6 text-sm">
            <a
              href="https://github.com/beihaili/Stories-about-Bitcoin"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-bitcoin-orange transition-colors"
            >
              GitHub
            </a>
            <a
              href="https://twitter.com/bhbtc1337"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-bitcoin-orange transition-colors"
            >
              Twitter
            </a>
            <span className="opacity-50">MIT License</span>
          </div>
          <p className="mt-6 text-xs opacity-50">
            © 2024 Stories about Bitcoin · Made with ❤️ and React
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
